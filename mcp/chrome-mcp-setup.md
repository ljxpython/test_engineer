# Chrome MCP Server 配置指南

## 概述
Chrome MCP Server 是基于Chrome扩展的Model Context Protocol (MCP) 服务器，使AI助手能够控制Chrome浏览器，实现复杂的浏览器自动化、内容分析和语义搜索。

## 配置文件状态
✅ **配置文件已正确创建**: `/Users/.claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "type": "streamableHttp",
      "url": "http://127.0.0.1:12306/mcp"
    }
  }
}
```

## 安装步骤

### 1. 安装Chrome MCP Bridge
✅ **已完成** - 全局安装并注册Native Messaging Host

```bash
# 安装bridge服务
npm install -g mcp-chrome-bridge

# 注册Native Messaging host
mcp-chrome-bridge register
```

### 2. 下载Chrome扩展
✅ **已完成** - 扩展文件已下载到 `/tmp/`

```bash
# 下载最新版本扩展
curl -L -o /tmp/chrome-mcp-server-0.0.6.zip \
  https://github.com/hangwin/mcp-chrome/releases/download/v0.0.6/chrome-mcp-server-0.0.6.zip

# 解压扩展文件
cd /tmp && unzip chrome-mcp-server-0.0.6.zip
```

### 3. 安装Chrome扩展 (需手动操作)
⏳ **需要完成**

1. 打开Chrome浏览器
2. 访问 `chrome://extensions/`
3. 启用右上角的"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择目录: `/tmp/` (包含manifest.json等文件)
6. 扩展安装完成后，点击扩展图标
7. 在弹出页面中点击"连接"按钮

### 4. 验证连接
扩展配置完成后，HTTP服务器将在 `http://127.0.0.1:12306/mcp` 启动

```bash
# 测试连接
curl -I http://127.0.0.1:12306/mcp

# 应该返回200状态码，表示服务正常运行
```

## 使用方式

### 推荐连接方式
- **Streamable HTTP**: `http://127.0.0.1:12306/mcp` (推荐)
- **STDIO**: 使用全局安装的包路径

### 功能特性
- 🚄 **Streamable HTTP**: 高效的HTTP连接方式
- 🌐 **20+工具**: 支持截图、网络监控、交互操作、书签管理等
- 🚀 **SIMD加速**: 自定义WebAssembly优化，4-8倍向量运算性能提升
- 💻 **完全本地**: 纯本地MCP服务器，确保用户隐私
- 🔄 **实时同步**: 直接使用日常Chrome浏览器状态和配置

## 重启Claude Code
完成Chrome扩展安装和配置后，重启Claude Code以使MCP配置生效。

## 故障排除

### 连接失败
```bash
curl: (7) Failed to connect to 127.0.0.1 port 12306
```
**解决方案**: 确保Chrome扩展已正确安装并点击"连接"按钮启动HTTP服务

### 扩展无法加载
- 确认 `/tmp/` 目录包含 `manifest.json` 文件
- 检查Chrome开发者模式是否已启用
- 尝试重新解压扩展文件

### Native Messaging错误
```bash
# 重新注册Host
mcp-chrome-bridge register

# 修复权限
mcp-chrome-bridge fix-permissions
```

## 文件位置
- **配置文件**: `/Users/.claude/claude_desktop_config.json`
- **扩展文件**: `/tmp/` (临时位置)
- **Bridge安装**: `~/.nvm/versions/node/v20.17.0/lib/node_modules/mcp-chrome-bridge`
- **Native Host**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`

## 完成状态
- ✅ 配置文件已创建并格式正确
- ✅ Chrome MCP Bridge已安装并注册  
- ✅ Chrome扩展文件已下载到本地
- ⏳ 需要手动在Chrome中安装扩展并连接

完成Chrome扩展安装后即可在Claude Code中使用Chrome MCP功能。