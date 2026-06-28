# 文档解析模块使用指南

## 一、依赖安装

### 1. Python 依赖安装

```powershell
# 创建虚拟环境（推荐）
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 或者手动安装核心包
pip install unstructured[paddleocr,pdf,docx,pptx]
pip install paddlepaddle paddleocr
pip install loguru chardet
```

### 2. 系统依赖安装（LibreOffice）

LibreOffice 用于解析 DOCX/PPTX 格式：

```powershell
# Windows（使用 Chocolatey）
choco install libreoffice

# macOS（使用 Homebrew）
brew install libreoffice

# Linux（Ubuntu/Debian）
sudo apt update
sudo apt install libreoffice

# 或者下载安装包：
# https://www.libreoffice.org/download/download-libreoffice/
```

### 3. 其他可选依赖

```powershell
# PDF 图像提取（用于扫描版 PDF OCR）
pip install PyMuPDF pdf2image

# Windows 需要安装 poppler
# 下载：https://github.com/osber/poppler-windows/releases
# 解压后将 bin 目录添加到 PATH
```

## 二、快速开始

### 1. 单文件解析

```python
from doc_parser import extract_full_text

# 解析 PDF
text = extract_full_text("raw/产品优化部门/广告基础系列.pdf")
print(f"提取了 {len(text)} 字符")

# 解析 Word 文档
text = extract_full_text("raw/产品优化部门/01广告说明书2023年版.docx")
print(text[:500])  # 预览前500字符

# 解析 PowerPoint
text = extract_full_text("raw/产品优化部门/市场分析 李国庆.pptx")
print(text)
```

### 2. 批量文件夹解析

```python
from doc_parser import batch_load_docs, get_document_stats

# 批量解析所有文档
docs = batch_load_docs("raw/")

# 获取统计信息
stats = get_document_stats(docs)
print(f"总共解析 {stats['total_files']} 个文件")
print(f"总字符数: {stats['total_chars']}")

# 遍历所有文档
for file_path, content in docs.items():
    print(f"\n文件: {file_path}")
    print(f"内容长度: {len(content)} 字符")
    print(f"内容预览: {content[:200]}...")
```

### 3. 命令行快速测试

```powershell
# 运行内置示例
python doc_parser.py
```

## 三、接入原有知识库的改造步骤

### 步骤 1：安装依赖

```powershell
pip install -r requirements.txt
```

### 步骤 2：验证模块可用

```python
# 测试导入
from doc_parser import extract_full_text, batch_load_docs

# 测试单文件
text = extract_full_text("raw/example.txt")
print(f"模块工作正常: {len(text)} 字符")
```

### 步骤 3：替换原有 txt 读取逻辑

**原有代码（假设）：**
```python
# 旧方式：直接读取 txt
def load_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**新代码（使用解析模块）：**
```python
# 新方式：支持所有格式
from doc_parser import extract_full_text

def load_document(file_path):
    return extract_full_text(file_path)
```

### 步骤 4：集成到批量处理流程

```python
from doc_parser import batch_load_docs

# 替换原有的文件遍历逻辑
def process_knowledge_base(raw_dir="raw/"):
    # 新方式：自动处理所有格式
    docs = batch_load_docs(raw_dir)
    
    for file_path, content in docs.items():
        # 后续处理：分块、向量化等
        print(f"处理: {file_path}")
        # chunks = split_text(content)
        # embeddings = vectorize(chunks)
        # ...
```

## 四、函数接口说明

### extract_full_text(file_path: str) -> str

**功能**：提取单个文件的完整文本

**参数**：
- `file_path`: 文件绝对路径或相对路径

**返回**：
- 清洗后的完整文本字符串

**支持格式**：
- `.txt` - 纯文本（自动检测编码）
- `.docx` - Word 文档
- `.pdf` - PDF 文档（含扫描版 OCR）
- `.pptx` - PowerPoint 演示文稿

**示例**：
```python
text = extract_full_text("raw/document.pdf")
```

### batch_load_docs(folder_path: str) -> Dict[str, str]

**功能**：批量加载文件夹中的所有文档

**参数**：
- `folder_path`: 文件夹路径

**返回**：
- `{文件绝对路径: 文本内容}` 字典

**示例**：
```python
docs = batch_load_docs("raw/")
for path, content in docs.items():
    print(f"{path}: {len(content)} 字符")
```

### get_document_stats(docs: Dict[str, str]) -> dict

**功能**：获取文档统计信息

**参数**：
- `docs`: batch_load_docs 返回的字典

**返回**：
- 统计信息字典

**示例**：
```python
stats = get_document_stats(docs)
print(f"总文件数: {stats['total_files']}")
```

## 五、常见问题排查清单

### 1. 中文乱码问题

**症状**：提取的文本出现乱码或特殊字符

**解决方案**：
```python
# 模块已内置多编码检测，通常无需额外处理
# 如果仍有问题，可手动指定编码
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read()
    result = chardet.detect(raw)
    return result['encoding']

# 使用检测到的编码
encoding = detect_encoding("document.txt")
with open("document.txt", 'r', encoding=encoding) as f:
    text = f.read()
```

### 2. PaddleOCR 模型下载失败

**症状**：首次运行时提示模型下载失败

**解决方案**：
```powershell
# 方案 1：设置国内镜像源
set PADDLEOCR_HOME=https://paddleocr.bj.bcebos.com

# 方案 2：手动下载模型
# 下载地址：https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/en/models_list_en.md
# 放置到：~/.paddleocr/ 目录

# 方案 3：使用代理
set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890
```

### 3. LibreOffice 缺失问题

**症状**：DOCX/PPTX 解析失败，提示 LibreOffice 未安装

**解决方案**：
```powershell
# Windows
choco install libreoffice

# 或者手动下载安装
# https://www.libreoffice.org/download/download-libreoffice/

# 验证安装
soffice --version
```

### 4. 扫描件识别效果差

**症状**：扫描版 PDF 识别准确率低

**解决方案**：
```python
# 1. 确保使用 hi_res 模式
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="scanned.pdf",
    strategy="hi_res",
    ocr_languages=["chi_sim", "eng"]
)

# 2. 调整图像 DPI（提高分辨率）
import fitz
doc = fitz.open("scanned.pdf")
page = doc[0]
pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI

# 3. 预处理图像（去噪、增强对比度）
from PIL import Image, ImageEnhance
img = Image.open("page.png")
img = img.convert('L')  # 转灰度
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2.0)  # 增强对比度
```

### 5. 内存不足问题

**症状**：处理大文件时内存溢出

**解决方案**：
```python
# 1. 分页处理 PDF
import fitz
doc = fitz.open("large.pdf")
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    # 逐页处理...

# 2. 使用生成器
def process_large_pdf(file_path):
    import fitz
    doc = fitz.open(file_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 处理单页...
        yield page_text
    doc.close()

# 3. 增加系统虚拟内存
```

### 6. 特殊格式表格提取

**症状**：复杂表格无法正确提取

**解决方案**：
```python
# 使用 Unstructured 的表格提取功能
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",
    infer_table_structure=True  # 启用表格结构推断
)

# 提取表格内容
for element in elements:
    if element.category == "Table":
        print(f"表格内容: {element.text}")
        # 表格元数据
        if hasattr(element.metadata, 'text_as_html'):
            print(f"HTML 格式: {element.metadata.text_as_html}")
```

### 7. 图片中的文字提取

**症状**：文档中的图片内容无法提取

**解决方案**：
```python
# Unstructured 会自动提取图片并进行 OCR
# 确保启用了图片提取选项
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="document.pdf",
    strategy="hi_res",
    extract_images_in_pdf=True  # 启用图片提取
)

# 查看提取的图片
for element in elements:
    if hasattr(element.metadata, 'image_path'):
        print(f"图片路径: {element.metadata.image_path}")
        print(f"OCR 结果: {element.text}")
```

### 8. 编码问题（Windows）

**症状**：Windows 系统下出现编码错误

**解决方案**：
```powershell
# 设置环境变量
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

# 或者在 Python 文件开头添加
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 六、性能优化建议

1. **并行处理**：对大量文件可使用多进程
2. **缓存结果**：避免重复解析同一文件
3. **按需 OCR**：仅对扫描件启用 OCR
4. **降低 DPI**：非关键文档可使用 150 DPI

## 七、扩展开发

### 添加新格式支持

```python
def extract_custom_format(file_path: str) -> str:
    """添加自定义格式解析"""
    # 实现解析逻辑...
    pass

# 在 extract_full_text 中添加判断
if file_type == '.custom':
    raw_text = extract_custom_format(file_path)
```

### 自定义文本清洗

```python
def custom_clean_text(text: str) -> str:
    """自定义文本清洗规则"""
    # 添加特殊字符处理...
    return text
```

## 八、技术支持

- **Unstructured 文档**：https://docs.unstructured.io
- **PaddleOCR 文档**：https://paddleocr.ai
- **项目仓库**：https://github.com/Unstructured-IO/unstructured