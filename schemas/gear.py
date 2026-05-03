"""齿轮计算模型"""

from pydantic import BaseModel, Field


class SpurGearRequest(BaseModel):
    """直齿圆柱齿轮计算请求"""
    m: float = Field(..., description="模数 (mm)")
    z: int = Field(..., description="齿数")
    alpha: float = Field(20.0, description="压力角 (°)")
    ha_star: float = Field(1.0, description="齿顶高系数")
    c_star: float = Field(0.25, description="顶隙系数")


class SpurGearResponse(BaseModel):
    """直齿圆柱齿轮计算响应"""
    d: float = Field(..., description="分度圆直径 (mm)")
    da: float = Field(..., description="齿顶圆直径 (mm)")
    df: float = Field(..., description="齿根圆直径 (mm)")
    db: float = Field(..., description="基圆直径 (mm)")
    ha: float = Field(..., description="齿顶高 (mm)")
    hf: float = Field(..., description="齿根高 (mm)")
    h: float = Field(..., description="全齿高 (mm)")
    p: float = Field(..., description="齿距 (mm)")


class HelicalGearRequest(BaseModel):
    """斜齿圆柱齿轮计算请求"""
    mn: float = Field(..., description="法向模数 (mm)")
    z: int = Field(..., description="齿数")
    beta: float = Field(..., description="螺旋角 (°)")
    alpha_n: float = Field(20.0, description="法向压力角 (°)")
    ha_star: float = Field(1.0, description="齿顶高系数")
    c_star: float = Field(0.25, description="顶隙系数")


class HelicalGearResponse(BaseModel):
    """斜齿圆柱齿轮计算响应"""
    mt: float = Field(..., description="端面模数 (mm)")
    d: float = Field(..., description="分度圆直径 (mm)")
    da: float = Field(..., description="齿顶圆直径 (mm)")
    df: float = Field(..., description="齿根圆直径 (mm)")
    db: float = Field(..., description="基圆直径 (mm)")
    pz: float = Field(..., description="导程 (mm)")


class BevelGearRequest(BaseModel):
    """锥齿轮计算请求"""
    m: float = Field(..., description="大端模数 (mm)")
    z1: int = Field(..., description="小轮齿数")
    z2: int = Field(..., description="大轮齿数")
    sigma: float = Field(90.0, description="轴交角 (°)")
    ha_star: float = Field(1.0, description="齿顶高系数")


class BevelGearResponse(BaseModel):
    """锥齿轮计算响应"""
    i: float = Field(..., description="传动比")
    delta1: float = Field(..., description="小轮分锥角 (°)")
    delta2: float = Field(..., description="大轮分锥角 (°)")
    d1: float = Field(..., description="小轮大端分度圆直径 (mm)")
    d2: float = Field(..., description="大轮大端分度圆直径 (mm)")
    R: float = Field(..., description="锥距 (mm)")
    da1: float = Field(..., description="小轮大端齿顶圆直径 (mm)")
    da2: float = Field(..., description="大轮大端齿顶圆直径 (mm)")
