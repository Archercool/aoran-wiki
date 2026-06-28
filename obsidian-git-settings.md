# Obsidian Git 插件配置指南

## 安装步骤
1. 打开 Obsidian → 设置 → 第三方插件
2. 关闭“安全模式”
3. 点击“浏览” → 搜索“Git”
4. 安装“Obsidian Git”并启用

## 推荐配置
设置 → Obsidian Git：

### 自动备份
- **自动备份间隔**：`5` 分钟
- **自动拉取间隔**：`5` 分钟
- **提交消息**：`vault backup: {{date}}`
- **推送前自动提交**：✅ 启用
- **拉取前自动备份**：✅ 启用

### 高级设置
- **备份当前文件夹**：`.`（当前目录）
- **提交更改**：✅ 启用
- **推送更改**：✅ 启用
- **拉取更改**：✅ 启用
- **自动拉取**：✅ 启用

## 手动操作
- **立即备份**：Ctrl+P → “Obsidian Git: Backup”
- **立即拉取**：Ctrl+P → “Obsidian Git: Pull”

## 故障排除
- 确保 Git 代理已配置（127.0.0.1:7890）
- 检查 Obsidian 控制台（Ctrl+Shift+I）错误信息
- 重启 Obsidian 或重新安装插件

## 注意事项
- 插件配置保存在 `.obsidian/plugins/obsidian-git/data.json`
- 此配置已被 `.gitignore` 排除，不会同步到 GitHub