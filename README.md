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

### 其他工具
- Redis

## 快速开始

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

5. 设置环境变量：
```bash
# 创建.env文件
cp .env.example .env
# 编辑.env文件设置数据库连接和其他配置
```

6. 运行迁移并启动服务器：
```bash
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

## API文档

启动后端服务器后，可以在以下地址访问API文档：

```
http://localhost:8000/api/v1/docs
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
│   ├── main.py          # 主应用入口
│   └── requirements.txt # 依赖列表
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
