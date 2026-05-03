"""齿轮计算服务"""

import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def calc_spur_gear(m: float, z: int, alpha: float = 20.0, ha_star: float = 1.0, c_star: float = 0.25) -> dict:
    """直齿圆柱齿轮计算"""
    m_mm = Q_(m, "mm")

    d = m_mm * z
    ha = ha_star * m_mm
    hf = (ha_star + c_star) * m_mm
    h = ha + hf
    da = d + 2 * ha
    df = d - 2 * hf
    db = d * math.cos(math.radians(alpha))
    p = math.pi * m_mm

    return {
        "d": round(d.magnitude, 3),
        "da": round(da.magnitude, 3),
        "df": round(df.magnitude, 3),
        "db": round(db.magnitude, 3),
        "ha": round(ha.magnitude, 3),
        "hf": round(hf.magnitude, 3),
        "h": round(h.magnitude, 3),
        "p": round(p.magnitude, 3)
    }


def calc_helical_gear(mn: float, z: int, beta: float, alpha_n: float = 20.0, ha_star: float = 1.0, c_star: float = 0.25) -> dict:
    """斜齿圆柱齿轮计算"""
    mn_mm = Q_(mn, "mm")
    beta_rad = math.radians(beta)

    mt = mn_mm / math.cos(beta_rad)
    d = mt * z
    ha = ha_star * mn_mm
    hf = (ha_star + c_star) * mn_mm
    da = d + 2 * ha
    df = d - 2 * hf
    alpha_t = math.atan(math.tan(math.radians(alpha_n)) / math.cos(beta_rad))
    db = d * math.cos(alpha_t)
    pz = math.pi * d / math.tan(beta_rad)

    return {
        "mt": round(mt.magnitude, 3),
        "d": round(d.magnitude, 3),
        "da": round(da.magnitude, 3),
        "df": round(df.magnitude, 3),
        "db": round(db.magnitude, 3),
        "pz": round(pz.magnitude, 3)
    }


def calc_bevel_gear(m: float, z1: int, z2: int, sigma: float = 90.0, ha_star: float = 1.0) -> dict:
    """锥齿轮计算"""
    m_mm = Q_(m, "mm")
    sigma_rad = math.radians(sigma)

    i = z2 / z1
    delta1 = math.atan(math.sin(sigma_rad) / (i + math.cos(sigma_rad)))
    delta2 = sigma_rad - delta1

    d1 = m_mm * z1
    d2 = m_mm * z2
    R = d1 / (2 * math.sin(delta1))
    ha = ha_star * m_mm
    da1 = d1 + 2 * ha * math.cos(delta1)
    da2 = d2 + 2 * ha * math.cos(delta2)

    return {
        "i": round(i, 3),
        "delta1": round(math.degrees(delta1), 3),
        "delta2": round(math.degrees(delta2), 3),
        "d1": round(d1.magnitude, 3),
        "d2": round(d2.magnitude, 3),
        "R": round(R.magnitude, 3),
        "da1": round(da1.magnitude, 3),
        "da2": round(da2.magnitude, 3)
    }
