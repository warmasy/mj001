"""通用请求/响应模型"""

from pydantic import BaseModel, Field
from typing import Optional


class UnitConvertRequest(BaseModel):
    """单位转换请求"""
    value: float = Field(..., description="数值")
    from_unit: str = Field(..., description="源单位")
    to_unit: str = Field(..., description="目标单位")


class UnitConvertResponse(BaseModel):
    """单位转换响应"""
    value: float
    from_unit: str
    to_unit: str
    result: float


class MassCalcRequest(BaseModel):
    """质量计算请求"""
    density: float = Field(..., description="密度 (g/cm³)")
    volume: float = Field(..., description="体积 (cm³)")


class MassCalcResponse(BaseModel):
    """质量计算响应"""
    mass_g: float
    mass_kg: float
    mass_ton: float
    density: float
    volume: float
