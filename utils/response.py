"""统一响应格式封装"""

from typing import Any, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """统一 API 响应格式"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


def success(data: Any = None, message: str = "success") -> dict:
    """成功响应"""
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error(message: str = "请求失败", code: int = 500) -> dict:
    """错误响应"""
    return {
        "code": code,
        "message": message,
        "data": None
    }
