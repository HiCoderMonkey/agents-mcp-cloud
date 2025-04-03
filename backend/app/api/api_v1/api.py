from fastapi import APIRouter

from app.api.api_v1.endpoints import users, auth, mcp_servers, agents, sdk_keys, chat

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(mcp_servers.router, prefix="/mcp-servers", tags=["MCP服务器"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agent"])
api_router.include_router(sdk_keys.router, prefix="/sdk-keys", tags=["SDK密钥"])
api_router.include_router(chat.router, prefix="/chat", tags=["聊天"])