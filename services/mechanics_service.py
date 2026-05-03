"""材料力学计算服务"""

import math
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity


def calc_beam(F: float, L: float, a: float, E: float = 206000.0, I: float = None, y: float = None) -> dict:
    """简支梁弯曲计算（集中载荷）

    公式:
        RA = F * b / L
        RB = F * a / L
        M_max = F * a * b / L
        σ_max = M_max * y / I
        f_max = F*a*b*(L²-a²-b²) / (6*E*I*L)
    """
    F_qty = Q_(F, "N")
    L_qty = Q_(L, "mm")
    a_qty = Q_(a, "mm")
    b_qty = L_qty - a_qty
    E_qty = Q_(E, "MPa")
    I_qty = Q_(I, "mm**4")
    y_qty = Q_(y, "mm")

    RA = F_qty * b_qty / L_qty
    RB = F_qty * a_qty / L_qty
    M_max = F_qty * a_qty * b_qty / L_qty
    sigma_max = (M_max * y_qty / I_qty).to("MPa")
    f_max = (F_qty * a_qty * b_qty * (L_qty**2 - a_qty**2 - b_qty**2) / (6 * E_qty * I_qty * L_qty)).to("mm")

    return {
        "RA": round(RA.magnitude, 2),
        "RB": round(RB.magnitude, 2),
        "M_max": round(M_max.to("N*mm").magnitude, 2),
        "sigma_max": round(sigma_max.magnitude, 3),
        "f_max": round(f_max.magnitude, 4)
    }


def calc_shaft(M: float, T: float, d: float, sigma_s: float, S: float = 2.0) -> dict:
    """轴的强度计算（第三强度理论）

    公式:
        σ_ca = M / W = 32M / (πd³)
        τ_ca = T / Wt = 16T / (πd³)
        σ_eq = √(σ_ca² + 3τ_ca²) ≤ [σ]
        d_min = ³√(16M_eq / (π[τ]))
    """
    M_qty = Q_(M, "N*mm")
    T_qty = Q_(T, "N*mm")
    d_qty = Q_(d, "mm")
    sigma_s_qty = Q_(sigma_s, "MPa")

    W = math.pi * d_qty**3 / 32
    Wt = math.pi * d_qty**3 / 16

    sigma_ca = (M_qty / W).to("MPa")
    tau_ca = (T_qty / Wt).to("MPa")
    sigma_eq = math.sqrt(sigma_ca.magnitude**2 + 3 * tau_ca.magnitude**2)
    sigma_allow = sigma_s_qty / S

    M_eq = math.sqrt(M_qty.magnitude**2 + 0.75 * T_qty.magnitude**2)
    d_min = ((16 * M_eq / (math.pi * sigma_allow.magnitude)) ** (1/3))

    return {
        "sigma_ca": round(sigma_ca.magnitude, 3),
        "tau_ca": round(tau_ca.magnitude, 3),
        "sigma_eq": round(sigma_eq, 3),
        "sigma_allow": round(sigma_allow.magnitude, 3),
        "safety": round(sigma_s / sigma_eq, 2),
        "d_min": round(d_min, 2)
    }


def calc_torsion(d: float, T: float, L: float = 1000.0, G: float = 79000.0, tau_allow: float = 40.0) -> dict:
    """圆轴扭转计算

    公式:
        Ip = πd⁴ / 32
        Wt = πd³ / 16
        τ_max = T / Wt = 16T / (πd³)
        θ = T / (G·Ip) × 180/π  (°/m)
        φ = T·L / (G·Ip) × 180/π  (°)
    """
    d_qty = Q_(d, "mm")
    T_qty = Q_(T, "N*mm")
    L_qty = Q_(L, "mm")
    G_qty = Q_(G, "MPa")
    tau_allow_qty = Q_(tau_allow, "MPa")

    Ip = math.pi * d_qty**4 / 32
    Wt = math.pi * d_qty**3 / 16

    tau_max = (T_qty / Wt).to("MPa")
    theta = (T_qty / (G_qty * Ip) * (180 / math.pi) * 1000).to("deg/m")
    phi = (T_qty * L_qty / (G_qty * Ip) * (180 / math.pi)).to("deg")

    return {
        "Ip": round(Ip.to("mm**4").magnitude, 2),
        "Wt": round(Wt.to("mm**3").magnitude, 2),
        "tau_max": round(tau_max.magnitude, 3),
        "theta": round(theta.magnitude, 4),
        "phi": round(phi.magnitude, 4),
        "tau_allow": tau_allow,
        "safe": tau_max.magnitude <= tau_allow
    }
