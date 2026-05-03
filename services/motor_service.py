"""电机计算服务"""

import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def calc_motor_power(P: float = None, T: float = None, n: float = None, U: float = 380.0, eta: float = 0.85) -> dict:
    """电机功率/力矩/电流计算

    公式:
        P = T * n / 9550  (kW)
        T = 9550 * P / n  (N·m)
        I = P * 1000 / (U * eta * 0.85)  (A)
    """
    if T is not None and n is not None:
        # 由力矩算功率
        T_qty = Q_(T, "N*m")
        n_qty = Q_(n, "rpm")
        P_qty = (T_qty * n_qty / 9550).to("kW")
        omega = (n_qty * 2 * math.pi / 60).to("rad/s")
        I = P_qty * 1000 / (Q_(U, "V") * eta * 0.85)
    elif P is not None and n is not None:
        # 由功率算力矩
        P_qty = Q_(P, "kW")
        n_qty = Q_(n, "rpm")
        T_qty = (P_qty * 9550 / n_qty).to("N*m")
        omega = (n_qty * 2 * math.pi / 60).to("rad/s")
        I = P_qty * 1000 / (Q_(U, "V") * eta * 0.85)
    elif P is not None and U is not None:
        # 由功率算电流
        P_qty = Q_(P, "kW")
        T_qty = Q_(T if T else 0, "N*m")
        n_qty = Q_(n if n else 0, "rpm")
        omega = (n_qty * 2 * math.pi / 60).to("rad/s") if n else Q_(0, "rad/s")
        I = P_qty * 1000 / (Q_(U, "V") * eta * 0.85)
    else:
        raise ValueError("参数不足，请至少提供 P+T+n 中的两个")

    return {
        "P": round(P_qty.magnitude, 3),
        "T": round(T_qty.magnitude, 3),
        "T_kgfm": round((T_qty.to("kgf*m")).magnitude, 3),
        "n": n if n else round(n_qty.magnitude, 3),
        "omega": round(omega.magnitude, 3),
        "I": round(I.magnitude, 2)
    }


def calc_motor_speed(D: float = None, n: float = None, v: float = None, t: float = None, J: float = None, T: float = None) -> dict:
    """速度与时间计算"""
    if D is not None and n is not None:
        D_qty = Q_(D, "mm")
        n_qty = Q_(n, "rpm")
        v_qty = (math.pi * D_qty * n_qty / 1000).to("m/min")
        omega = (n_qty * 2 * math.pi / 60).to("rad/s")
        return {
            "v": round(v_qty.magnitude, 3),
            "omega": round(omega.magnitude, 3),
            "n": n,
            "D": D,
            "t": 0.0,
            "a": 0.0
        }
    elif v is not None and D is not None:
        v_qty = Q_(v, "m/min")
        D_qty = Q_(D, "mm")
        n_qty = (v_qty * 1000 / (math.pi * D_qty)).to("rpm")
        omega = (n_qty * 2 * math.pi / 60).to("rad/s")
        return {
            "v": v,
            "omega": round(omega.magnitude, 3),
            "n": round(n_qty.magnitude, 1),
            "D": D,
            "t": 0.0,
            "a": 0.0
        }
    elif J is not None and T is not None and t is not None:
        J_qty = Q_(J, "kg*m**2")
        T_qty = Q_(T, "N*m")
        t_qty = Q_(t, "s")
        omega = (T_qty * t_qty / J_qty).to("rad/s")
        n_qty = (omega * 60 / (2 * math.pi)).to("rpm")
        a_qty = (T_qty / J_qty).to("rad/s**2")
        return {
            "v": 0.0,
            "omega": round(omega.magnitude, 3),
            "n": round(n_qty.magnitude, 1),
            "D": 0.0,
            "t": t,
            "a": round(a_qty.magnitude, 3)
        }
    else:
        raise ValueError("参数不足，请提供 D+n 或 v+D 或 J+T+t")
