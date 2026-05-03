"""材料属性表"""
from sqlalchemy import Column, Integer, String, Float, Text
from config.database import Base

class MaterialProperty(Base):
    __tablename__ = "material_properties"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="材料名称")
    density = Column(Float, nullable=True, comment="密度 g/cm³")
    elastic_modulus = Column(Float, nullable=True, comment="弹性模量 MPa")
    yield_strength = Column(Float, nullable=True, comment="屈服强度 MPa")
    shear_modulus = Column(Float, nullable=True, comment="剪切模量 MPa")
    description = Column(Text, nullable=True)
