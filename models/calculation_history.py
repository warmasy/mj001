"""计算历史记录表"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.sql import func
from config.database import Base

class CalculationHistory(Base):
    __tablename__ = "calculation_history"
    __table_args__ = (
        Index("idx_module_created", "module", "created_at"),
        {"comment": "存储用户的计算历史"},
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    module = Column(String(50), nullable=False, comment="计算模块")
    calc_type = Column(String(50), nullable=False, comment="计算类型")
    input_params = Column(Text, nullable=False, comment="输入参数 JSON")
    result = Column(Text, nullable=False, comment="结果 JSON")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
