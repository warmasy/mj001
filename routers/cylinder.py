"""气缸计算路由"""

from fastapi import APIRouter
from schemas.cylinder import CylinderForceRequest, CylinderPressureRequest
from services.cylinder_service import calc_cylinder_force, calc_cylinder_pressure
from utils.response import success, error

router = APIRouter(prefix="/cylinder", tags=["气缸计算"])


@router.post("/force")
def cylinder_force(req: CylinderForceRequest):
    """气缸力计算"""
    try:
        result = calc_cylinder_force(req.D, req.d, req.P, req.eta)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/pressure")
def cylinder_pressure(req: CylinderPressureRequest):
    """压力与压强计算"""
    try:
        result = calc_cylinder_pressure(req.F, req.A, req.P)
        return success(result)
    except Exception as e:
        return error(str(e), 400)
