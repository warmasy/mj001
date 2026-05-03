"""电机计算路由"""

from fastapi import APIRouter
from schemas.motor import MotorPowerRequest, MotorSpeedRequest
from services.motor_service import calc_motor_power, calc_motor_speed
from utils.response import success, error

router = APIRouter(prefix="/motor", tags=["电机计算"])


@router.post("/power")
def motor_power(req: MotorPowerRequest):
    """电机功率与力矩计算"""
    try:
        result = calc_motor_power(req.P, req.T, req.n, req.U, req.eta)
        return success(result)
    except Exception as e:
        return error(str(e), 400)


@router.post("/speed")
def motor_speed(req: MotorSpeedRequest):
    """速度与时间计算"""
    try:
        result = calc_motor_speed(req.D, req.n, req.v, req.t, req.J, req.T)
        return success(result)
    except Exception as e:
        return error(str(e), 400)
