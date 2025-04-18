# MCP Workspace

这是一个用于开发和部署自定义 MCP (Model Context Protocol) 服务器的工作空间。您可以在这里实现和管理您的 MCP 服务器。

## 目录结构

```
mcp-workspace/
├── README.md
├── servers/                # MCP 服务器实现目录
│   └── my_server/         # 您的自定义服务器
│       ├── __init__.py
│       ├── config.json    # 服务器配置文件
│       └── server.py      # 服务器实现
├── servers-example/       # 参考实现
└── utils/                 # 工具函数
```

## 快速开始

### 1. 环境准备

1. 安装 Python 3.10 或更高版本
2. 安装 uv 包管理工具：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 2. 创建新的 MCP 服务器

1. 初始化项目：
```bash
uv init my_server
cd my_server
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx
```

2. 创建服务器文件：
```bash
touch server.py
```

### 3. 实现服务器逻辑

在 `server.py` 中实现您的 MCP 服务器逻辑。基本结构如下：

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器
mcp = FastMCP("my_server")

# 工具实现示例
@mcp.tool()
async def my_tool(param1: str, param2: int) -> str:
    """工具描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    """
    # 实现工具逻辑
    return "工具执行结果"

# 运行服务器
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### 4. 配置服务器

在 `config.json` 中定义服务器配置：

```json
{
    "name": "my_server",
    "description": "我的自定义 MCP 服务器",
    "version": "1.0.0",
    "config": {
        "api_base": "http://your-api-endpoint",
        "api_key": "your-api-key"
    }
}
```

## MCP 核心概念

MCP 服务器可以提供三种主要类型的功能：

1. **资源 (Resources)**: 客户端可以读取的文件类数据（如 API 响应或文件内容）
2. **工具 (Tools)**: LLM 可以调用的函数（需要用户批准）
3. **提示 (Prompts)**: 帮助用户完成特定任务的预写模板

## 测试服务器

### 1. 运行服务器

```bash
uv run server.py
```

### 2. 配置 Claude Desktop

1. 打开配置文件：
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. 添加服务器配置：
```json
{
    "mcpServers": {
        "my_server": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/mcp-workspace/servers/my_server",
                "run",
                "server.py"
            ]
        }
    }
}
```

3. 重启 Claude Desktop

## 故障排除

如果遇到问题，可以：

1. 检查 Claude Desktop 日志：
```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

2. 常见问题：
   - 确保配置文件语法正确
   - 使用绝对路径而不是相对路径
   - 完全重启 Claude Desktop

## 参考实现

在 `servers-example` 目录中提供了完整的参考实现，展示了：

1. 如何正确实现 MCP 接口
2. 如何处理配置和初始化
3. 如何实现工具功能
4. 如何处理错误和异常
5. 如何管理 API 连接和资源

## 最佳实践

1. **错误处理**
   - 妥善处理 API 调用错误
   - 提供有意义的错误信息

2. **配置验证**
   - 实现配置验证
   - 确保必要的配置项存在

3. **资源管理**
   - 正确管理 API 连接
   - 实现清理方法

4. **日志记录**
   - 使用日志记录重要操作
   - 便于问题排查

## 注意事项

1. 所有 API 调用都应该是异步的
2. 确保正确处理工具调用
3. 妥善保管 API 密钥等敏感信息
4. 遵循 Python 异步编程最佳实践

## 帮助和支持

如果您在开发过程中遇到问题，请：

1. 查看示例代码
2. 检查错误日志
3. 参考文档
4. 提交 Issue
