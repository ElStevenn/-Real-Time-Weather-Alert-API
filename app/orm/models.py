from sqlalchemy import String, UUID, BINARY, Float, DateTime, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from datetime import datetime
import uuid

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(40), nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    # Define relationship 1:N with subscriptions and alerts
    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="user")
    alerts: Mapped[list["Alert"]] = relationship("Alert", back_populates="user")

class Subscription(Base): 
    __tablename__ = "subscriptions"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    notification_method: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="subscriptions")

class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    conditions: Mapped[str] = mapped_column(String(200), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="alerts")
