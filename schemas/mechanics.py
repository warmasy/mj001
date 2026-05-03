"""材料力学计算模型"""

from pydantic import BaseModel, Field


class BeamRequest(BaseModel):
    """梁的弯曲计算请求"""
    F: float = Field(..., description="集中载荷 (N)")
    L: float = Field(..., description="梁长度 (mm)")
    a: float = Field(..., description="载荷距左端距离 (mm)")
    E: float = Field(206000.0, description="弹性模量 (MPa)")
    I: float = Field(..., description="截面惯性矩 (mm⁴)")
    y: float = Field(..., description="截面最远纤维距离 (mm)")


class BeamResponse(BaseModel):
    """梁的弯曲计算响应"""
    RA: float = Field(..., description="左支座反力 (N)")
    RB: float = Field(..., description="右支座反力 (N)")
    M_max: float = Field(..., description="最大弯矩 (N·mm)")
    sigma_max: float = Field(..., description="最大正应力 (MPa)")
    f_max: float = Field(..., description="最大挠度 (mm)")


class ShaftRequest(BaseModel):
    """轴的强度计算请求"""
    M: float = Field(..., description="弯矩 (N·mm)")
    T: float = Field(..., description="扭矩 (N·mm)")
    d: float = Field(..., description="轴直径 (mm)")
    sigma_s: float = Field(..., description="屈服强度 (MPa)")
    S: float = Field(2.0, description="安全系数")


class ShaftResponse(BaseModel):
    """轴的强度计算响应"""
    sigma_ca: float = Field(..., description="弯曲应力 (MPa)")
    tau_ca: float = Field(..., description="扭转应力 (MPa)")
    sigma_eq: float = Field(..., description="等效应力 (MPa)")
    sigma_allow: float = Field(..., description="许用应力 (MPa)")
    safety: float = Field(..., description="实际安全系数")
    d_min: float = Field(..., description="最小轴径 (mm)")


class TorsionRequest(BaseModel):
    """扭转计算请求"""
    d: float = Field(..., description="轴直径 (mm)")
    T: float = Field(..., description="扭矩 (N·mm)")
    L: float = Field(1000.0, description="轴长度 (mm)")
    G: float = Field(79000.0, description="剪切模量 (MPa)")
    tau_allow: float = Field(..., description="许用切应力 (MPa)")


class TorsionResponse(BaseModel):
    """扭转计算响应"""
    Ip: float = Field(..., description="极惯性矩 (mm⁴)")
    Wt: float = Field(..., description="抗扭截面系数 (mm³)")
    tau_max: float = Field(..., description="最大切应力 (MPa)")
    theta: float = Field(..., description="单位长度扭转角 (°/m)")
    phi: float = Field(..., description="总扭转角 (°)")
    tau_allow: float = Field(..., description="许用切应力 (MPa)")
    safe: bool = Field(..., description="是否安全")
