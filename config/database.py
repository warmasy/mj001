"""数据库配置 - SQLAlchemy + aiomysql 异步引擎

本文件只提供数据库连接和 Session 管理，不自动创建表。
请确保数据库和表已在外部（如手动 SQL 或 Alembic）创建好。

========================================
快速测试数据库连接（不需要启动 FastAPI）：

    python config/database.py

如果看到 "数据库连接成功" 的提示，说明配置正确。
========================================
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import asyncio

# ==================== 数据库连接配置 ====================
# 请根据你的 MySQL 配置修改以下参数
DB_HOST = " "
DB_PORT = 1
DB_USER = " "
DB_PASSWORD = " "
DB_NAME = " "

# aiomysql 的异步连接 URL
# 格式: mysql+aiomysql://用户名:密码@主机:端口/数据库名
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建异步引擎
# pool_pre_ping=True: 连接池在返回连接前会先 ping 一下，防止连接过期
engine = create_async_engine(
    DATABASE_URL,
    echo=False,           # 设为 True 可打印所有 SQL 语句（调试用）
    pool_pre_ping=True,
    pool_size=10,       # 连接池大小
    max_overflow=20     # 超出 pool_size 时最多创建的额外连接数
)

# 创建异步 Session 工厂
# class_=AsyncSession: 使用异步 Session
# expire_on_commit=False: 提交后数据不会过期，可继续读取
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# 声明基类，所有 ORM 模型都继承这个类
Base = declarative_base()


# ==================== 依赖注入函数 ====================
async def get_db():
    """FastAPI 依赖注入用：每次请求创建一个 Session，结束后自动关闭

    用法:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ==================== 数据库连接测试函数 ====================
async def test_connection():
    """测试数据库连接是否成功

    直接执行 SQL 查询验证连接，并在终端打印结果。
    不需要启动 FastAPI，单独运行本文件即可测试。
    """
    print("=" * 50)
    print("正在测试数据库连接...")
    print(f"  主机: {DB_HOST}:{DB_PORT}")
    print(f"  数据库: {DB_NAME}")
    print(f"  用户: {DB_USER}")
    print("=" * 50)

    try:
        # 尝试建立连接并执行简单查询
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 AS test"))
            row = result.fetchone()

            if row and row[0] == 1:
                print("[OK] 数据库连接成功")
                print(f"[OK] 连接 URL: {DATABASE_URL.replace(DB_PASSWORD, '***')}")
                print("=" * 50)
                return True
            else:
                print("[FAIL] 数据库返回异常结果")
                return False

    except Exception as e:
        print("[FAIL] 数据库连接失败")
        print(f"  错误信息: {str(e)}")
        print("")
        print("常见原因及解决方法:")
        print("  1. MySQL 服务未启动          -> 启动 MySQL 服务")
        print("  2. 用户名/密码错误            -> 修改 DB_USER / DB_PASSWORD")
        print("  3. 数据库不存在               -> 执行 CREATE DATABASE mech_calc")
        print("  4. aiomysql 未安装            -> pip install aiomysql cryptography")
        print("=" * 50)
        return False

    finally:
        # 关闭引擎，释放连接
        await engine.dispose()


# ==================== 直接运行本文件时执行测试 ====================
if __name__ == "__main__":
    """当直接运行 python config/database.py 时，执行连接测试

    不需要启动 FastAPI 项目，单独运行即可验证数据库配置是否正确。
    """
    asyncio.run(test_connection())
