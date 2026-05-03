"""常用计算路由"""

from fastapi import APIRouter
from schemas.common import UnitConvertRequest, MassCalcRequest
from services.unit_service import convert_unit, calc_mass
from utils.response import success, error

router = APIRouter(prefix="/common", tags=["常用计算"])


@router.post("/convert")
def unit_convert(req: UnitConvertRequest):
    """单位转换"""
    try:
        result = convert_unit(req.value, req.from_unit, req.to_unit)
        return success({
            "value": req.value,
            "from_unit": req.from_unit,
            "to_unit": req.to_unit,
            "result": result
        })
    except Exception as e:
        return error(str(e), 400)


@router.post("/mass")
def mass_calc(req: MassCalcRequest):
    """质量计算"""
    try:
        result = calc_mass(req.density, req.volume)
        return success(result)
    except Exception as e:
        return error(str(e), 400)
