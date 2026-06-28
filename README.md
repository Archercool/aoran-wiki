# 我的 Karpathy 知识库

基于 Andrej Karpathy 的 LLM 知识库架构搭建。

## 目录结构
- `raw/`: 放入原始资料（PDF、网页、笔记等）
- `wiki/`: LLM 自动生成的概念文章
- `outputs/`: 查询结果和报告
- `AGENTS.md`: 知识库的 schema 文件，定义 LLM 的工作规则

## 如何使用
1. 将源文件放入 `raw/` 目录。
2. 使用 LLM 代理（如 Claude Code、Cursor 等）打开本目录。
3. 让 LLM 代理读取 `AGENTS.md`，然后处理 `raw/` 中的新文件。
4. LLM 会自动在 `wiki/` 中创建文章，并更新 `wiki/INDEX.md`。
5. 你可以向 LLM 提问，答案会保存在 `outputs/` 中。

## 使用 opencode（当前环境）
1. 将源文件放入 `raw/` 目录。
2. 在 opencode 中，直接输入指令，例如：
   - “请处理 raw 目录中的新文件，按照 AGENTS.md 的规则”
   - “检查 wiki 的一致性，运行 linting 检查”
   - “回答问题：……”
3. opencode 会读取 `AGENTS.md`，自动处理并更新 `wiki/` 和 `outputs/`。

## 定期维护
让 LLM 代理运行 linting 检查，确保文章一致性和完整性。