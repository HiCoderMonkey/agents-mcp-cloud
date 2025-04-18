# MCP Agents Cloud

MCP Agents Cloud是一个提供管理MCP服务器和代理（Agent）的平台。

## 功能特性

- 用户管理（注册、登录、密码重置）
- MCP服务器管理（添加、编辑、删除、查看）
- Agent管理（创建、编辑、删除、查看）
- Agent SDK（Python包和HTTP API）
- Agent聊天交互（流式输出）
- SDK密钥管理

## 技术栈

### 前端
- Vue.js
- Element UI
- Axios
- Vue Router
- Vuex

### 后端
- Python
- FastAPI
- SQLAlchemy
- JWT
- openai-agent框架

### 数据库
- MySQL 8.0

## 快速开始

### 安装依赖组件

项目依赖MySQL数据库，可以通过Docker快速安装：

```bash
# 进入docker目录
cd docker

# 确保数据目录存在
sudo mkdir -p /appdata/share/agents-mcp-cloud/mysql/data
sudo chown -R $USER:$USER /appdata/share/agents-mcp-cloud/mysql/data

# 启动MySQL服务
docker-compose up -d mysql
```

数据库将在63307端口启动。详细说明请参考[Docker依赖组件文档](docker/README.md)。

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境：
```bash
python -m venv venv
```

3. 激活虚拟环境：
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. 安装依赖：
```bash
pip install -r requirements.txt
```

5. 配置系统：
```bash
# 根据环境选择复制对应的配置文件
cp config.yml.example config-dev.yml
# 然后编辑配置文件
```

6. 运行应用：
```bash
# 设置环境（默认为dev）
export ENV=dev  # 或 test, prod

# 或直接指定配置文件的绝对路径
export CONFIG_FILE="$(pwd)/config-dev.yml"

# 运行服务
cd backend  # 确保在backend目录下运行
uvicorn main:app --reload
```

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run serve
```

4. 构建生产版本：
```bash
npm run build
```

## 配置说明

项目使用基于环境的YAML配置文件：

- `config-dev.yml`：开发环境配置
- `config-test.yml`：测试环境配置
- `config-prod.yml`：生产环境配置

配置文件应放在backend目录下，可以通过以下两种方式指定配置：

```bash
# 1. 通过环境变量指定环境，系统将查找backend/config-{ENV}.yml
export ENV=dev  # 或 test, prod

# 2. 直接指定配置文件的绝对路径（推荐）
export CONFIG_FILE="/完整路径/到配置文件/config-dev.yml"
```

主要配置项包括：

- `app`: 应用名称、版本等基本信息
- `api`: API路径前缀和文档URL
- `server`: 服务器主机、端口设置
- `security`: 安全设置（密钥、令牌过期时间）
- `cors`: 跨域设置
- `database`: 数据库连接URL和连接池设置
- `openai`: OpenAI API密钥和模型设置
- `email`: 电子邮件发送设置
- `smtp`: SMTP服务器配置

详细配置示例请参考`config.yml.example`文件。

## API文档

启动后端服务器后，可以在以下地址访问API文档：

```
http://localhost:8000/docs
```

## 项目结构

```
agents-mcp-cloud/
├── backend/             # 后端代码
│   ├── app/             # 应用代码
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心功能
│   │   ├── db/          # 数据库工具
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic模式
│   │   ├── utils/       # 工具函数
│   │   └── services/    # 业务服务
│   ├── config-dev.yml   # 开发环境配置 
│   ├── config-test.yml  # 测试环境配置
│   ├── config-prod.yml  # 生产环境配置
│   ├── main.py          # 主应用入口
│   └── requirements.txt # 依赖列表
├── docker/              # Docker依赖组件
│   ├── docker-compose.yml # Docker编排文件
│   └── mysql/           # MySQL相关配置
├── frontend/            # 前端代码
│   ├── public/          # 静态资源
│   ├── src/             # 源代码
│   │   ├── assets/      # 资源文件
│   │   ├── components/  # Vue组件
│   │   ├── router/      # 路由配置
│   │   ├── store/       # Vuex存储
│   │   ├── views/       # 页面视图
│   │   └── api/         # API客户端
│   └── package.json     # 依赖列表
└── scripts/             # 脚本文件
```

## 许可证

[MIT](LICENSE)
