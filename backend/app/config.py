import os
from typing import List, Dict, Any, Optional, Union
from pathlib import Path

import yaml
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """应用配置类，从YAML文件读取配置"""
    
    # 获取当前环境，默认为开发环境
    ENV: str = os.environ.get("ENV", "dev")
    CONFIG_FILE: str = os.environ.get("CONFIG_FILE", f"config-{ENV}.yml")
    
    # 项目信息 - 设置默认值防止验证错误
    PROJECT_NAME: str = "MCP Agents Cloud"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520
    SERVER_HOST: str = "http://localhost:8000"
    
    # CORS设置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库设置
    DATABASE_URL: str = "mysql+pymysql://mcp_user:mcp_password@localhost:63307/mcp_agents_dev"
    
    # OpenAI设置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE: float = 0.7
    
    # 电子邮件设置
    EMAILS_FROM_EMAIL: str = "info@example.com"
    EMAILS_FROM_NAME: str = "MCP Agents Cloud"
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: Path = Path("app/email-templates")
    
    # SMTP设置
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_TLS: bool = True
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    def __init__(self, **values: Any):
        """初始化配置类，从YAML文件读取配置"""
        # 首先设置接收到的值
        super().__init__(**values)
        
        # 获取配置文件路径
        config_file = self.CONFIG_FILE
        if not os.path.isabs(config_file):
            # 如果是相对路径，则相对于项目根目录
            base_dir = Path(__file__).parents[1]  # 从app/config.py上去两级到项目根目录
            config_file = os.path.join(base_dir, config_file)
        
        # 打印配置文件路径以便调试
        print(f"尝试读取配置文件: {config_file}")
        
        # 读取YAML配置文件
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                if config_data:
                    # 更新配置值
                    self._update_from_yaml(config_data)
                    print(f"成功从 {config_file} 加载配置")
                else:
                    print(f"警告: 配置文件 {config_file} 为空或格式不正确")
            except Exception as e:
                print(f"错误: 读取配置文件 {config_file} 时出错: {str(e)}")
        else:
            print(f"警告: 配置文件 {config_file} 不存在，将使用默认值")
    
    def _update_from_yaml(self, config_data: Dict[str, Any]) -> None:
        """从YAML配置数据更新配置值"""
        # 应用名称和描述
        self.PROJECT_NAME = config_data.get('app', {}).get('name', self.PROJECT_NAME)
        
        # API设置
        self.API_V1_STR = config_data.get('api', {}).get('prefix', self.API_V1_STR)
        
        # 服务器设置
        server_config = config_data.get('server', {})
        self.SERVER_HOST = server_config.get('server_url', self.SERVER_HOST)
        
        # 安全设置
        security_config = config_data.get('security', {})
        self.SECRET_KEY = security_config.get('secret_key', self.SECRET_KEY)
        self.ACCESS_TOKEN_EXPIRE_MINUTES = security_config.get('access_token_expire_minutes', self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # CORS设置
        cors_config = config_data.get('cors', {})
        self.BACKEND_CORS_ORIGINS = cors_config.get('origins', self.BACKEND_CORS_ORIGINS)
        
        # 数据库设置
        db_config = config_data.get('database', {})
        self.DATABASE_URL = db_config.get('url', self.DATABASE_URL)
        
        # OpenAI设置
        openai_config = config_data.get('openai', {})
        self.OPENAI_API_KEY = openai_config.get('api_key', self.OPENAI_API_KEY)
        self.OPENAI_MODEL = openai_config.get('model', self.OPENAI_MODEL)
        self.OPENAI_TEMPERATURE = openai_config.get('temperature', self.OPENAI_TEMPERATURE)
        
        # 电子邮件设置
        email_config = config_data.get('email', {})
        self.EMAILS_FROM_EMAIL = email_config.get('from_email', self.EMAILS_FROM_EMAIL)
        self.EMAILS_FROM_NAME = email_config.get('from_name', self.EMAILS_FROM_NAME)
        self.EMAIL_RESET_TOKEN_EXPIRE_HOURS = email_config.get('reset_token_expire_hours', self.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
        
        templates_dir = email_config.get('templates_dir', 'app/email-templates')
        if os.path.isabs(templates_dir):
            self.EMAIL_TEMPLATES_DIR = Path(templates_dir)
        else:
            base_dir = Path(__file__).parent  # app目录
            self.EMAIL_TEMPLATES_DIR = base_dir / templates_dir
        
        # SMTP设置
        smtp_config = config_data.get('smtp', {})
        self.SMTP_HOST = smtp_config.get('host', self.SMTP_HOST)
        self.SMTP_PORT = smtp_config.get('port', self.SMTP_PORT)
        self.SMTP_TLS = smtp_config.get('tls', self.SMTP_TLS)
        self.SMTP_USER = smtp_config.get('user', self.SMTP_USER)
        self.SMTP_PASSWORD = smtp_config.get('password', self.SMTP_PASSWORD)
    
    class Config:
        case_sensitive = True


# 创建单例实例 - 使用模块级别的单例
settings = _Settings()
