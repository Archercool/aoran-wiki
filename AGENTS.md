# 知识库 Schema

## 目录结构
- `raw/`: 原始资料（论文、网页、笔记等）。只增不改，是唯一的真实来源。
- `wiki/`: LLM编写的概念文章。每个概念一个 `.md` 文件，相互链接。
- `outputs/`: 查询结果和报告。

## 处理新资料（当 `raw/` 中有新文件时）
1. 运行文档解析：`python doc_parser.py` 或调用 `batch_load_docs("raw/")`
2. 解析后的文本内容可直接用于向量化和分块
3. 读取 `wiki/INDEX.md` 了解现有文章。
4. 识别资料中的新概念，检查是否已在 `wiki/` 中存在。
5. 为每个新概念创建文章，或更新现有文章。
6. 在相关文章间添加反向链接。
7. 更新 `wiki/INDEX.md`。

## 文档解析（自动化流程）
- **解析模块**：`doc_parser.py`
- **支持格式**：`.docx` / `.pdf` / `.pptx` / `.txt`
- **OCR 引擎**：PaddleOCR（中英双语）
- **使用方法**：
  ```python
  from doc_parser import extract_full_text, batch_load_docs
  
  # 单文件解析
  text = extract_full_text("raw/document.pdf")
  
  # 批量文件夹解析
  docs = batch_load_docs("raw/")
  for path, content in docs.items():
      print(f"{path}: {len(content)} 字符")
  ```

## INDEX.md 格式
每行一条：`[文章标题](文件名.md) - 一句话摘要`

## 回答查询时
1. 读取 `wiki/INDEX.md`。
2. 找到相关文章并阅读。
3. 将答案写入 `outputs/YYYY-MM-DD-查询摘要.md`。

## Linting 检查（定期运行）
1. 读取所有 `wiki/` 文章。
2. 检查矛盾、缺失的反向链接、有提及但无文章的概念。
3. 为缺失概念创建草稿。

## 注意事项
- 文章使用 Markdown 格式。
- 保持文章简洁，每篇文章聚焦一个概念。
- 链接使用标准 Markdown 格式 `[文本](文件.md)`，而非 Obsidian 双链 `[[文件]]`。
- 人类的主要编辑角色是完善此 schema 文件，而不是直接写文章。