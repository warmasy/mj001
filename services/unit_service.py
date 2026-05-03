"""单位转换服务 - 使用 Pint 库"""

from pint import UnitRegistry

# 创建全局单位注册器
ureg = UnitRegistry()
Q_ = ureg.Quantity


def convert_unit(value: float, from_unit: str, to_unit: str) -> float:
    """单位转换

    示例:
        convert_unit(100, "mm", "m") -> 0.1
        convert_unit(1, "kW", "hp") -> 1.341
    """
    try:
        quantity = Q_(value, from_unit)
        result = quantity.to(to_unit)
        return result.magnitude
    except Exception as e:
        raise ValueError(f"单位转换失败: {from_unit} -> {to_unit}, 错误: {str(e)}")


def calc_mass(density_g_cm3: float, volume_cm3: float) -> dict:
    """质量计算

    使用 Pint 进行单位换算:
    - 输入: g/cm³, cm³
    - 输出: g, kg, t
    """
    density = Q_(density_g_cm3, "g/cm**3")
    volume = Q_(volume_cm3, "cm**3")

    mass = density * volume

    return {
        "mass_g": round(mass.to("g").magnitude, 3),
        "mass_kg": round(mass.to("kg").magnitude, 6),
        "mass_ton": round(mass.to("t").magnitude, 9),
        "density": density_g_cm3,
        "volume": volume_cm3
    }
