"""气缸计算模型"""

from pydantic import BaseModel, Field


class CylinderForceRequest(BaseModel):
    """气缸力计算请求"""
    D: float = Field(..., description="气缸内径 (mm)")
    d: float = Field(0.0, description="活塞杆直径 (mm)")
    P: float = Field(..., description="工作压力 (MPa)")
    eta: float = Field(0.9, description="气缸效率")


class CylinderForceResponse(BaseModel):
    """气缸力计算响应"""
    F_push: float = Field(..., description="理论推力 (N)")
    F_pull: float = Field(..., description="理论拉力 (N)")
    F_push_actual: float = Field(..., description="实际推力 (N)")
    F_pull_actual: float = Field(..., description="实际拉力 (N)")
    A_push: float = Field(..., description="无杆侧面积 (mm²)")
    A_pull: float = Field(..., description="有杆侧面积 (mm²)")


class CylinderPressureRequest(BaseModel):
    """压力压强计算请求"""
    F: float = Field(None, description="力 (N)")
    A: float = Field(None, description="面积 (mm²)")
    P: float = Field(None, description="压强 (MPa)")


class CylinderPressureResponse(BaseModel):
    """压力压强计算响应"""
    P: float = Field(..., description="压强 (MPa)")
    P_bar: float = Field(..., description="压强 (bar)")
    P_psi: float = Field(..., description="压强 (psi)")
    F: float = Field(..., description="力 (N)")
    A: float = Field(..., description="面积 (mm²)")
    d: float = Field(..., description="等效直径 (mm)")
