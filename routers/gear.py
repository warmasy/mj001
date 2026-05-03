"""齿轮计算路由"""

from fastapi import APIRouter
from schemas.gear import SpurGearRequest, HelicalGearRequest, BevelGearRequest
from services.gear_service import calc_spur_gear, calc_helical_gear, calc_bevel_gear
from utils.response import success, error

router = APIRouter(prefix="/gear", tags=["齿轮计算"])


@router.post("/spur")
def spur_gear(req: SpurGearRequest):
    """直齿圆柱齿轮计算"""
    try:
        result = calc_spur_gear(req.m, req.z, req.alpha, req.ha_star, req.c_star)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/helical")
def helical_gear(req: HelicalGearRequest):
    """斜齿圆柱齿轮计算"""
    try:
        result = calc_helical_gear(req.mn, req.z, req.beta, req.alpha_n, req.ha_star, req.c_star)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/bevel")
def bevel_gear(req: BevelGearRequest):
    """锥齿轮计算"""
    try:
        result = calc_bevel_gear(req.m, req.z1, req.z2, req.sigma, req.ha_star)
        return success(result)
    except Exception as e:
        return error(str(e), 400)
