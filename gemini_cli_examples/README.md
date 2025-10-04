# Gemini CLI 自定义命令示例

本目录提供一个基于 [Gemini CLI 命令文档](https://raw.githubusercontent.com/google-gemini/gemini-cli/refs/heads/main/docs/cli/commands.md) 的最小化自定义命令示例。

## 目录结构

```
./commands/demo/standup.toml
```

该 TOML 文件定义了 `/demo:standup` 命令。运行后，它会请 Gemini 将当前上下文内容整理成日常站会常用的三条要点。

## 使用步骤

1. 确保本地存在 `~/.gemini/commands` 目录：

   ```bash
   mkdir -p ~/.gemini/commands/demo
   ```

2. 将示例文件复制到 Gemini CLI 读取的目录：

   ```bash
   cp gemini_cli_examples/commands/demo/standup.toml ~/.gemini/commands/demo/standup.toml
   ```

3. 启动 Gemini CLI 并调用新命令：

   ```
   > @path/to/context/file.md
   > /demo:standup
   ```

Gemini CLI 会执行 `standup.toml` 中定义的提示词，返回一份整理好的站会更新内容。

## 继续扩展

- 修改 `prompt` 字段即可调整命令的输出行为。
- 更新 `description` 可以优化命令在 CLI 内的帮助文本。
- 在新的子目录下新增更多 `.toml` 文件即可构建额外命令组。

如需更多选项与最佳实践，请参考官方文档。
