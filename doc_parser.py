#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档解析与加载模块
基于 Karpathy 极简本地 RAG 知识库架构

功能：
1. 支持 .docx / .pdf / .pptx / .txt 格式文档解析
2. 内置 PaddleOCR 中英双语识别（chi_sim + eng）
3. 自动提取内嵌图片、截图、扫描页文字
4. 文本清洗与标准化处理
5. 批量文件夹遍历处理

使用方法：
    from doc_parser import extract_full_text, batch_load_docs
    
    # 单文件解析
    text = extract_full_text("document.pdf")
    
    # 批量文件夹解析
    docs = batch_load_docs("raw/")
"""

import os
import sys
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 支持的文件格式
SUPPORTED_FORMATS = {'.txt', '.docx', '.pdf', '.pptx'}


@dataclass
class DocumentContent:
    """文档内容数据类"""
    file_path: str
    file_name: str
    file_type: str
    content: str
    metadata: dict
    success: bool
    error_message: Optional[str] = None


def clean_text(text: str) -> str:
    """
    文本清洗与标准化
    
    功能：
    1. 去除多余空行和空白字符
    2. 统一 UTF-8 编码
    3. 合并重复空白与换行
    4. 去除不可见特殊字符
    
    参数：
        text: 原始文本
    
    返回：
        清洗后的文本
    """
    if not text:
        return ""
    
    # 统一换行符
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # 去除不可见特殊字符（保留中文、英文、数字、常用标点）
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # 合并连续空行（最多保留2个换行）
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 合并连续空格（保留单个空格）
    text = re.sub(r'[^\S\n]{2,}', ' ', text)
    
    # 去除每行首尾空白
    lines = [line.strip() for line in text.split('\n')]
    
    # 去除空行（保留段落间的单个空行）
    cleaned_lines = []
    prev_was_empty = False
    
    for line in lines:
        if not line:
            if not prev_was_empty:
                cleaned_lines.append('')
            prev_was_empty = True
        else:
            cleaned_lines.append(line)
            prev_was_empty = False
    
    # 去除开头和结尾的空行
    while cleaned_lines and not cleaned_lines[0]:
        cleaned_lines.pop(0)
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()
    
    return '\n'.join(cleaned_lines)


def detect_file_type(file_path: str) -> str:
    """
    检测文件类型
    
    参数：
        file_path: 文件路径
    
    返回：
        文件类型后缀（小写）
    """
    return Path(file_path).suffix.lower()


def is_supported_format(file_path: str) -> bool:
    """
    检查文件是否为支持的格式
    
    参数：
        file_path: 文件路径
    
    返回：
        是否支持
    """
    return detect_file_type(file_path) in SUPPORTED_FORMATS


def extract_txt(file_path: str) -> str:
    """
    提取纯文本文件内容
    
    参数：
        file_path: 文件路径
    
    返回：
        文本内容
    """
    # 尝试多种编码读取
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # 如果所有编码都失败，使用二进制读取并忽略错误
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore')


def extract_with_unstructured(file_path: str) -> str:
    """
    使用 Unstructured 库解析文档
    
    支持格式：.docx, .pdf, .pptx
    
    参数：
        file_path: 文件路径
    
    返回：
        提取的文本内容
    """
    try:
        from unstructured.partition.auto import partition
        from unstructured.partition.pdf import partition_pdf
        from unstructured.partition.docx import partition_docx
        from unstructured.partition.pptx import partition_pptx
        
        file_type = detect_file_type(file_path)
        
        # 根据文件类型选择解析方法
        if file_type == '.pdf':
            # PDF 使用 hi_res 模式，启用 OCR
            elements = partition_pdf(
                filename=file_path,
                strategy="hi_res",
                ocr_languages=["chi_sim", "eng"],
                extract_images_in_pdf=True,
                infer_table_structure=True
            )
        elif file_type == '.docx':
            elements = partition_docx(filename=file_path)
        elif file_type == '.pptx':
            elements = partition_pptx(filename=file_path)
        else:
            elements = partition(filename=file_path)
        
        # 提取所有元素的文本
        text_parts = []
        for element in elements:
            if hasattr(element, 'text'):
                text_parts.append(element.text)
            elif hasattr(element, 'metadata'):
                # 处理图片 OCR 结果
                if hasattr(element.metadata, 'image_path'):
                    text_parts.append(f"[图片内容: {element.text}]")
                else:
                    text_parts.append(str(element))
            else:
                text_parts.append(str(element))
        
        return '\n\n'.join(text_parts)
        
    except Exception as e:
        logger.warning(f"Unstructured 解析失败: {e}")
        # 降级到 PaddleOCR 直接解析
        return extract_with_paddleocr(file_path)


def extract_with_paddleocr(file_path: str) -> str:
    """
    使用 PaddleOCR 直接解析文档
    
    适用于扫描版 PDF、全图片 PPT 等场景
    
    参数：
        file_path: 文件路径
    
    返回：
        OCR 识别的文本内容
    """
    try:
        from paddleocr import PaddleOCR
        
        # 初始化 PaddleOCR
        ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            use_gpu=False
        )
        
        file_type = detect_file_type(file_path)
        
        # 对于 PDF，需要先转换为图片
        if file_type == '.pdf':
            return _ocr_pdf(file_path, ocr)
        elif file_type in ['.docx', '.pptx']:
            return _ocr_office(file_path, ocr)
        else:
            # 直接对文件进行 OCR
            result = ocr.ocr(file_path, cls=True)
            return _extract_ocr_text(result)
            
    except Exception as e:
        logger.error(f"PaddleOCR 解析失败: {e}")
        return ""


def _ocr_pdf(file_path: str, ocr) -> str:
    """
    对 PDF 文件进行 OCR 处理
    
    参数：
        file_path: PDF 文件路径
        ocr: PaddleOCR 实例
    
    返回：
        OCR 识别的文本
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(file_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # 将页面转换为图片
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img_bytes = pix.tobytes("png")
            
            # OCR 识别
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp.write(img_bytes)
                tmp_path = tmp.name
            
            try:
                result = ocr.ocr(tmp_path, cls=True)
                page_text = _extract_ocr_text(result)
                if page_text.strip():
                    text_parts.append(f"[第 {page_num + 1} 页]\n{page_text}")
            finally:
                os.unlink(tmp_path)
        
        doc.close()
        return '\n\n'.join(text_parts)
        
    except ImportError:
        logger.warning("PyMuPDF 未安装，尝试使用 pdf2image")
        return _ocr_pdf_with_pdf2image(file_path, ocr)


def _ocr_pdf_with_pdf2image(file_path: str, ocr) -> str:
    """
    使用 pdf2image 对 PDF 进行 OCR
    
    参数：
        file_path: PDF 文件路径
        ocr: PaddleOCR 实例
    
    返回：
        OCR 识别的文本
    """
    try:
        from pdf2image import convert_from_path
        
        images = convert_from_path(file_path, dpi=300)
        text_parts = []
        
        for i, img in enumerate(images):
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                img.save(tmp.name, 'PNG')
                tmp_path = tmp.name
            
            try:
                result = ocr.ocr(tmp_path, cls=True)
                page_text = _extract_ocr_text(result)
                if page_text.strip():
                    text_parts.append(f"[第 {i + 1} 页]\n{page_text}")
            finally:
                os.unlink(tmp_path)
        
        return '\n\n'.join(text_parts)
        
    except Exception as e:
        logger.error(f"pdf2image OCR 失败: {e}")
        return ""


def _ocr_office(file_path: str, ocr) -> str:
    """
    对 Office 文档（DOCX/PPTX）进行 OCR
    
    参数：
        file_path: 文件路径
        ocr: PaddleOCR 实例
    
    返回：
        OCR 识别的文本
    """
    try:
        # 先使用 Unstructured 提取文本
        from unstructured.partition.auto import partition
        
        elements = partition(filename=file_path)
        text_parts = []
        
        for element in elements:
            if hasattr(element, 'text'):
                text_parts.append(element.text)
        
        return '\n\n'.join(text_parts)
        
    except Exception as e:
        logger.error(f"Office OCR 失败: {e}")
        return ""


def _extract_ocr_text(result) -> str:
    """
    从 PaddleOCR 结果中提取文本
    
    参数：
        result: OCR 识别结果
    
    返回：
        提取的文本
    """
    if not result or not result[0]:
        return ""
    
    text_parts = []
    for line in result[0]:
        if line and len(line) >= 2:
            # line[1] 是识别结果，包含 (text, confidence)
            text_tuple = line[1]
            if isinstance(text_tuple, tuple) and len(text_tuple) >= 1:
                text_parts.append(text_tuple[0])
    
    return '\n'.join(text_parts)


def extract_full_text(file_path: str) -> str:
    """
    提取单个文件的完整文本
    
    这是主要的公开接口，支持所有格式
    
    参数：
        file_path: 文件绝对路径或相对路径
    
    返回：
        清洗后的完整文本字符串
    
    使用示例：
        text = extract_full_text("raw/document.pdf")
        print(text)
    """
    file_path = str(Path(file_path).resolve())
    
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return ""
    
    file_name = os.path.basename(file_path)
    file_type = detect_file_type(file_path)
    
    logger.info(f"解析文件: {file_name} ({file_type})")
    
    try:
        # 根据文件类型选择解析方法
        if file_type == '.txt':
            raw_text = extract_txt(file_path)
        elif file_type in ['.docx', '.pdf', '.pptx']:
            raw_text = extract_with_unstructured(file_path)
        else:
            logger.warning(f"不支持的文件格式: {file_type}")
            return ""
        
        # 文本清洗
        cleaned_text = clean_text(raw_text)
        
        logger.info(f"解析完成: {file_name} ({len(cleaned_text)} 字符)")
        return cleaned_text
        
    except Exception as e:
        logger.error(f"解析文件失败 {file_name}: {e}")
        return ""


def batch_load_docs(folder_path: str) -> Dict[str, str]:
    """
    批量加载文件夹中的所有文档
    
    参数：
        folder_path: 文件夹路径
    
    返回：
        {文件绝对路径: 文本内容} 字典
    
    使用示例：
        docs = batch_load_docs("raw/")
        for path, content in docs.items():
            print(f"{path}: {len(content)} 字符")
    """
    folder_path = Path(folder_path).resolve()
    
    if not folder_path.exists():
        logger.error(f"文件夹不存在: {folder_path}")
        return {}
    
    if not folder_path.is_dir():
        logger.error(f"路径不是文件夹: {folder_path}")
        return {}
    
    results = {}
    total_files = 0
    success_files = 0
    failed_files = 0
    
    logger.info(f"开始扫描文件夹: {folder_path}")
    
    # 遍历所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = Path(root) / file_name
            
            # 检查是否为支持的格式
            if not is_supported_format(str(file_path)):
                continue
            
            total_files += 1
            
            try:
                content = extract_full_text(str(file_path))
                
                if content:
                    results[str(file_path)] = content
                    success_files += 1
                    logger.info(f"✓ 成功: {file_name}")
                else:
                    failed_files += 1
                    logger.warning(f"✗ 内容为空: {file_name}")
                    
            except Exception as e:
                failed_files += 1
                logger.error(f"✗ 解析失败 {file_name}: {e}")
                # 单个文件失败不中断全局流程
                continue
    
    # 输出统计信息
    logger.info(f"\n{'='*50}")
    logger.info(f"批量解析完成")
    logger.info(f"总文件数: {total_files}")
    logger.info(f"成功: {success_files}")
    logger.info(f"失败: {failed_files}")
    logger.info(f"{'='*50}\n")
    
    return results


def get_document_stats(docs: Dict[str, str]) -> dict:
    """
    获取文档统计信息
    
    参数：
        docs: batch_load_docs 返回的字典
    
    返回：
        统计信息字典
    """
    stats = {
        "total_files": len(docs),
        "total_chars": sum(len(content) for content in docs.values()),
        "files_by_type": {},
        "avg_chars_per_file": 0
    }
    
    for file_path, content in docs.items():
        file_type = detect_file_type(file_path)
        if file_type not in stats["files_by_type"]:
            stats["files_by_type"][file_type] = {"count": 0, "chars": 0}
        stats["files_by_type"][file_type]["count"] += 1
        stats["files_by_type"][file_type]["chars"] += len(content)
    
    if stats["total_files"] > 0:
        stats["avg_chars_per_file"] = stats["total_chars"] // stats["total_files"]
    
    return stats


# ==================== 快速使用示例 ====================

if __name__ == "__main__":
    """
    快速使用示例
    """
    import sys
    
    print("=" * 60)
    print("文档解析与加载模块 - Karpathy 知识库架构")
    print("=" * 60)
    
    # 示例 1: 单文件解析
    print("\n【示例 1】单文件解析")
    print("-" * 40)
    
    test_file = "raw/example.txt"
    if os.path.exists(test_file):
        text = extract_full_text(test_file)
        print(f"文件: {test_file}")
        print(f"内容长度: {len(text)} 字符")
        print(f"内容预览: {text[:200]}...")
    else:
        print(f"测试文件不存在: {test_file}")
    
    # 示例 2: 批量文件夹解析
    print("\n【示例 2】批量文件夹解析")
    print("-" * 40)
    
    docs = batch_load_docs("raw/")
    
    if docs:
        stats = get_document_stats(docs)
        print(f"解析文件数: {stats['total_files']}")
        print(f"总字符数: {stats['total_chars']}")
        print(f"平均每文件: {stats['avg_chars_per_file']} 字符")
        print(f"\n文件类型分布:")
        for file_type, info in stats['files_by_type'].items():
            print(f"  {file_type}: {info['count']} 个文件, {info['chars']} 字符")
    else:
        print("未找到可解析的文件")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)