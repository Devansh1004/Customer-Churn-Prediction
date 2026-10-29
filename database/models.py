from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    
    id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    timestamp : Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.now
    )
    
    prediction : Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    churn_probability : Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    
    display_probability : Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    
    model_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    shap_values : Mapped[list | None] = mapped_column(
        JSON,
        nullable=True
    )
    
    