"""材料力学计算路由"""

from fastapi import APIRouter
from schemas.mechanics import BeamRequest, ShaftRequest, TorsionRequest
from services.mechanics_service import calc_beam, calc_shaft, calc_torsion
from utils.response import success, error

router = APIRouter(prefix="/mechanics", tags=["材料力学"])


@router.post("/beam")
def beam(req: BeamRequest):
    """梁的弯曲计算"""
    try:
        result = calc_beam(req.F, req.L, req.a, req.E, req.I, req.y)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/shaft")
def shaft(req: ShaftRequest):
    """轴的强度计算"""
    try:
        result = calc_shaft(req.M, req.T, req.d, req.sigma_s, req.S)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/torsion")
def torsion(req: TorsionRequest):
    """扭转计算"""
    try:
        result = calc_torsion(req.d, req.T, req.L, req.G, req.tau_allow)
        return success(result)
    except Exception as e:
        return error(str(e), 400)
