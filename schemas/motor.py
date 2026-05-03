"""电机计算模型"""

from pydantic import BaseModel, Field


class MotorPowerRequest(BaseModel):
    """电机功率计算请求"""
    P: float = Field(None, description="功率 (kW)")
    T: float = Field(None, description="力矩 (N·m)")
    n: float = Field(None, description="转速 (r/min)")
    U: float = Field(380.0, description="电压 (V)")
    eta: float = Field(0.85, description="效率")


class MotorPowerResponse(BaseModel):
    """电机功率计算响应"""
    P: float = Field(..., description="功率 (kW)")
    T: float = Field(..., description="力矩 (N·m)")
    T_kgfm: float = Field(..., description="力矩 (kgf·m)")
    n: float = Field(..., description="转速 (r/min)")
    omega: float = Field(..., description="角速度 (rad/s)")
    I: float = Field(..., description="电流 (A)")


class MotorSpeedRequest(BaseModel):
    """速度与时间计算请求"""
    D: float = Field(None, description="直径 (mm)")
    n: float = Field(None, description="转速 (r/min)")
    v: float = Field(None, description="线速度 (m/min)")
    t: float = Field(None, description="时间 (s)")
    J: float = Field(None, description="转动惯量 (kg·m²)")
    T: float = Field(None, description="扭矩 (N·m)")


class MotorSpeedResponse(BaseModel):
    """速度与时间计算响应"""
    v: float = Field(..., description="线速度 (m/min)")
    omega: float = Field(..., description="角速度 (rad/s)")
    n: float = Field(..., description="转速 (r/min)")
    D: float = Field(..., description="直径 (mm)")
    t: float = Field(..., description="时间 (s)")
    a: float = Field(..., description="角加速度 (rad/s²)")
