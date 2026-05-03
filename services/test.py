"""电机计算服务"""

import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def test001(who: float = None, n: float = None) -> dict:
    """测试001

    """
    
    return {
        "who": f'你好呀!{who}。',
        "发送的数字":n,
        "平方":n**2

    }


