# """计算历史记录路由 - 数据库操作示例"""

# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List

# from config.database import get_db
# from crud.history import crud_history
# from schemas.common import ResponseModel
# from utils.response import success, error

# router = APIRouter(prefix="/history", tags=["计算历史"])


# @router.post("/save", response_model=ResponseModel)
# async def save_history(
#     module: str,
#     calc_type: str,
#     input_params: str,
#     result: str,
#     db: AsyncSession = Depends(get_db)
# ):
#     """保存一次计算记录到数据库

#     示例:
#         POST /api/history/save?module=gear&calc_type=spur&input_params={"m":2}&result={"d":40}
#     """
#     try:
#         obj = await crud_history.create(db, obj_in={
#             "module": module,
#             "calc_type": calc_type,
#             "input_params": input_params,
#             "result": result
#         })
#         return success({"id": obj.id, "created_at": obj.created_at})
#     except Exception as e:
#         return error(str(e), 400)


# @router.get("/list", response_model=ResponseModel)
# async def list_history(
#     skip: int = 0,
#     limit: int = 20,
#     db: AsyncSession = Depends(get_db)
# ):
#     """查询计算历史列表（分页）

#     示例:
#         GET /api/history/list?skip=0&limit=20
#     """
#     try:
#         items = await crud_history.get_multi(db, skip=skip, limit=limit)
#         data = [
#             {
#                 "id": item.id,
#                 "module": item.module,
#                 "calc_type": item.calc_type,
#                 "input_params": item.input_params,
#                 "result": item.result,
#                 "created_at": item.created_at.isoformat() if item.created_at else None
#             }
#             for item in items
#         ]
#         return success(data)
#     except Exception as e:
#         return error(str(e), 500)


# @router.get("/{history_id}", response_model=ResponseModel)
# async def get_history(history_id: int, db: AsyncSession = Depends(get_db)):
#     """根据 ID 查询单条记录"""
#     try:
#         item = await crud_history.get(db, id=history_id)
#         if not item:
#             return error("记录不存在", 404)
#         return success({
#             "id": item.id,
#             "module": item.module,
#             "calc_type": item.calc_type,
#             "input_params": item.input_params,
#             "result": item.result,
#             "created_at": item.created_at.isoformat() if item.created_at else None
#         })
#     except Exception as e:
#         return error(str(e), 500)


# @router.delete("/{history_id}", response_model=ResponseModel)
# async def delete_history(history_id: int, db: AsyncSession = Depends(get_db)):
#     """删除记录"""
#     try:
#         item = await crud_history.delete(db, id=history_id)
#         if not item:
#             return error("记录不存在", 404)
#         return success({"deleted_id": history_id})
#     except Exception as e:
#         return error(str(e), 500)
