"""气缸计算服务"""

import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def calc_cylinder_force(D: float, d: float = 0.0, P: float = 0.6, eta: float = 0.9) -> dict:
    """气缸推力/拉力计算

    公式:
        F_push = P * π * D² / 4
        F_pull = P * π * (D² - d²) / 4
    """
    D_qty = Q_(D, "mm")
    d_qty = Q_(d, "mm")
    P_qty = Q_(P, "MPa")

    A_push = math.pi * D_qty**2 / 4
    A_pull = math.pi * (D_qty**2 - d_qty**2) / 4

    F_push = P_qty * A_push
    F_pull = P_qty * A_pull

    return {
        "F_push": round(F_push.to("N").magnitude, 2),
        "F_pull": round(F_pull.to("N").magnitude, 2),
        "F_push_actual": round(F_push.to("N").magnitude * eta, 2),
        "F_pull_actual": round(F_pull.to("N").magnitude * eta, 2),
        "A_push": round(A_push.to("mm**2").magnitude, 2),
        "A_pull": round(A_pull.to("mm**2").magnitude, 2)
    }


def calc_cylinder_pressure(F: float = None, A: float = None, P: float = None) -> dict:
    """压力压强计算

    公式:
        P = F / A = 4F / (πD²)
    """
    if F is not None and A is not None:
        F_qty = Q_(F, "N")
        A_qty = Q_(A, "mm**2")
        P_qty = (F_qty / A_qty).to("MPa")
    elif F is not None and P is not None:
        F_qty = Q_(F, "N")
        P_qty = Q_(P, "MPa")
        A_qty = (F_qty / P_qty).to("mm**2")
    elif A is not None and P is not None:
        A_qty = Q_(A, "mm**2")
        P_qty = Q_(P, "MPa")
        F_qty = (P_qty * A_qty).to("N")
    else:
        raise ValueError("请至少提供 F+A、F+P 或 A+P 两组参数")

    d = 2 * math.sqrt(A_qty.to("mm**2").magnitude / math.pi)

    return {
        "P": round(P_qty.magnitude, 4),
        "P_bar": round((P_qty.to("bar")).magnitude, 4),
        "P_psi": round((P_qty.to("psi")).magnitude, 4),
        "F": round(F_qty.magnitude, 2),
        "A": round(A_qty.magnitude, 2),
        "d": round(d, 2)
    }
