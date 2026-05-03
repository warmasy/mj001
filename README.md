# 机械计算系统后端 API

基于 **FastAPI + Pint + SQLAlchemy(aiomysql)** 的机械工程计算服务。

---

## 一、项目结构

```
mech-calc-backend/
├── main.py                     # FastAPI 入口（含数据库生命周期）
├── requirements.txt            # Python 依赖
├── README.md                   # 本文件
├── .env                        # 环境变量（可选）
│
├── config/                     # 配置文件夹
│   ├── __init__.py
│   ├── settings.py             # 全局配置（CORS、API前缀、应用信息）
│   └── database.py             # SQLAlchemy + aiomysql 数据库配置
│
├── schemas/                    # Pydantic 数据验证模型（请求/响应）
│   ├── __init__.py
│   ├── common.py               # 通用模型（单位转换、质量计算）
│   ├── gear.py                 # 齿轮计算模型
│   ├── motor.py                # 电机计算模型
│   ├── cylinder.py             # 气缸计算模型
│   └── mechanics.py            # 材料力学模型
│
├── models/                     # SQLAlchemy ORM 数据库模型
│   ├── __init__.py
│   ├── calculation_history.py  # 计算历史记录表
│   ├── user.py                 # 用户表（示例）
│   └── material_property.py    # 材料属性表（示例）
│
├── routers/                    # FastAPI 路由（API 接口层）
│   ├── __init__.py
│   ├── common.py               # 常用计算接口
│   ├── gear.py                 # 齿轮计算接口
│   ├── motor.py                # 电机计算接口
│   ├── cylinder.py             # 气缸计算接口
│   ├── mechanics.py            # 材料力学接口
│   └── history.py              # 计算历史 CRUD 接口（数据库示例）
│
├── services/                   # 业务逻辑层（核心计算）
│   ├── __init__.py
│   ├── unit_service.py         # 单位转换（Pint）
│   ├── gear_service.py
│   ├── motor_service.py
│   ├── cylinder_service.py
│   └── mechanics_service.py
│
├── crud/                       # 数据库 CRUD 封装
│   ├── __init__.py             # 通用 CRUDBase 基类
│   └── history.py              # 计算历史的 CRUD 实例
│
└── utils/
    └── response.py             # 统一响应格式
```

---

## 二、快速开始

### 1. 安装 MySQL

确保本地或远程有可用的 MySQL 数据库，并创建数据库：

```sql
CREATE DATABASE mech_calc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 安装依赖

```bash
cd mech-calc-backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**如果 pydantic-core 构建失败，请参考 TROUBLESHOOTING.md。**

### 3. 配置数据库

编辑 `config/database.py`，修改为你的 MySQL 账号密码：

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "你的密码"
DB_NAME = "mech_calc"
```

### 4. 启动服务

```bash
python main.py
```

启动后：
- API 地址：`http://localhost:8000`
- 接口文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/health`

启动时会自动创建所有表（`init_db()`）。

---

## 三、数据库配置详解

### 3.1 文件位置

| 文件 | 用途 |
|------|------|
| `config/database.py` | 数据库引擎、Session 工厂、Base 基类 |
| `models/*.py` | 数据库表对应的 ORM 模型 |
| `crud/__init__.py` | 通用 CRUD 基类 |
| `crud/history.py` | 具体表的 CRUD 实例 |

### 3.2 核心配置

```python
# config/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# aiomysql 异步连接 URL
DATABASE_URL = "mysql+aiomysql://root:密码@localhost:3306/mech_calc"

# 异步引擎
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# Session 工厂
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)

# ORM 基类
Base = declarative_base()
```

### 3.3 在路由中使用数据库

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db

@router.post("/xxx")
async def some_endpoint(db: AsyncSession = Depends(get_db)):
    # db 是一个异步 Session，支持 await
    result = await db.execute(...)
    return success(...)
```

### 3.4 CRUD 基类用法

```python
from crud import CRUDBase
from models.calculation_history import CalculationHistory

# 创建实例
crud_history = CRUDBase(CalculationHistory)

# 使用
item = await crud_history.create(db, obj_in={"module": "gear", ...})
item = await crud_history.get(db, id=1)
items = await crud_history.get_multi(db, skip=0, limit=20)
await crud_history.delete(db, id=1)
```

---

## 四、Pint 单位库使用

所有计算服务都使用 **Pint** 进行单位管理：

```python
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

length = Q_(100, "mm")
print(length.to("m"))  # 0.1 m
```

---

## 五、扩展新功能的方法

### 5.1 添加新的 Pydantic 模型（schemas/）

```python
# schemas/bearing.py
from pydantic import BaseModel, Field

class BearingLifeRequest(BaseModel):
    C: float = Field(..., description="额定动载荷 (N)")
    P: float = Field(..., description="当量动载荷 (N)")
```

### 5.2 添加新的数据库表（models/）

```python
# models/bearing_result.py
from sqlalchemy import Column, Integer, Float
from config.database import Base

class BearingResult(Base):
    __tablename__ = "bearing_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    L10 = Column(Float, nullable=False)
    L10h = Column(Float, nullable=False)
```

### 5.3 添加新的计算服务（services/）

```python
# services/bearing_service.py
def calc_bearing_life(C: float, P: float) -> dict:
    L10 = (C / P) ** 3
    return {"L10": round(L10, 2)}
```

### 5.4 添加新的 API 路由（routers/）

```python
# routers/bearing.py
from fastapi import APIRouter
from schemas.bearing import BearingLifeRequest
from services.bearing_service import calc_bearing_life
from utils.response import success

router = APIRouter(prefix="/bearing", tags=["轴承计算"])

@router.post("/life")
def bearing_life(req: BearingLifeRequest):
    result = calc_bearing_life(req.C, req.P)
    return success(result)
```

### 5.5 注册路由（main.py）

```python
from routers import bearing
app.include_router(bearing.router, prefix=API_PREFIX)
```

---

## 六、前端对接

前端 axios baseURL 为 `/api`，开发时需在 `vite.config.js` 配置代理：

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

---

## 七、部署建议

### 使用 Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

*文档生成时间：2026-05-02*
