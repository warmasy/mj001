"""电机计算模型"""

from pydantic import BaseModel, Field


class Test(BaseModel):
    """请求测试"""
    who: float = Field(None, description="请求人")
    n: float = Field(2, description="效率")



