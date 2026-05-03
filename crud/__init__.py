"""CRUD 操作封装

为每个数据库表提供增删改查的基础操作。
所有方法都是异步的（async/await），配合 SQLAlchemy 异步 Session 使用。
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import TypeVar, Generic, List, Optional

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """通用 CRUD 基类

    用法:
        crud_history = CRUDBase(CalculationHistory)
        history = await crud_history.create(db, obj_in={...})
    """

    def __init__(self, model: type):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """根据 ID 查询单条记录"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession,
        *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """分页查询多条记录"""
        result = await db.execute(
            select(self.model).offset(skip).limit(limit).order_by(desc(self.model.id))
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: dict) -> ModelType:
        """创建记录"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """删除记录"""
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
