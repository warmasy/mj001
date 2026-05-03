"""FastAPI 入口文件"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import API_PREFIX, CORS_ORIGINS, APP_TITLE, APP_VERSION, APP_DESCRIPTION
from config.database import engine, DB_HOST, DB_PORT, DB_NAME
from routers import gear, motor, cylinder, mechanics, common, history,test


app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)

# CORS 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(common.router, prefix=API_PREFIX)
app.include_router(gear.router, prefix=API_PREFIX)
app.include_router(motor.router, prefix=API_PREFIX)
app.include_router(cylinder.router, prefix=API_PREFIX)
app.include_router(mechanics.router, prefix=API_PREFIX)
# app.include_router(history.router, prefix=API_PREFIX)
app.include_router(test.router, prefix=API_PREFIX)


@app.get("/")
def root():
    """根路径 - 服务状态检查"""
    return {
        "code": 200,
        "message": "机械计算系统后端服务运行中",
        "version": APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """健康检查接口"""
    return {"status": "ok"}


@app.get("/db-health")
async def db_health():
    """数据库连接检查接口

    访问 http://localhost:8000/db-health 即可测试数据库是否连接成功。

    返回示例（成功）:
        {"code": 200, "connected": true, "database": "mech_calc", "message": "数据库连接正常"}

    返回示例（失败）:
        {"code": 500, "connected": false, "error": "具体错误信息"}
    """
    try:
        from sqlalchemy import text
        # 尝试执行一个简单的 SQL 查询验证连接
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                return {
                    "code": 200,
                    "connected": True,
                    "database": DB_NAME,
                    "host": f"{DB_HOST}:{DB_PORT}",
                    "message": "数据库连接正常"
                }
    except Exception as e:
        return {
            "code": 500,
            "connected": False,
            "database": DB_NAME,
            "host": f"{DB_HOST}:{DB_PORT}",
            "error": str(e),
            "message": "数据库连接失败，请检查配置"
        }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
