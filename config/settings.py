"""全局配置"""

# API 前缀
API_PREFIX = "/api"

# CORS 允许的前端地址
CORS_ORIGINS = [
    "http://localhost:5173",   # Vite 默认开发端口
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

# 应用信息
APP_TITLE = "机械计算系统后端 API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "基于 FastAPI + Pint 的机械工程计算服务"
