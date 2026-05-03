"""电机计算路由"""

from fastapi import APIRouter
from schemas.motor import MotorPowerRequest, MotorSpeedRequest
from services.test import test001
from utils.response import success, error

router = APIRouter(prefix="/test", tags=["测试路由"])


@router.get("/test001")
def get_test001(req: MotorPowerRequest):
    """电机功率与力矩计算"""
    try:
        result = test001(req.who, req.n)
        return success(result)
    except Exception as e:
        return error(str(e), 400)

