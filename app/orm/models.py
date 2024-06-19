from sqlalchemy import String, UUID, BINARY, Float, DateTime, Text
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
    username: Mapped[String] = mapped_column(String(40), nullable=False)
    email: Mapped[String] = mapped_column(String(40), nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(BINARY, nullable=False)

    # Define relationship 1:N with subscriptions
    subscriptions: Mapped[list["Subscriptions"]] = relationship("Subscriptions", back_populates="user")
    alerts: Mapped[list["Alerts"]] = relationship("Alerts", back_populates="user")

class Subscriptions(Base): 
    __tablename__ = "subscriptions"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[String] = mapped_column(String(100), nullable=False)
    alert_type: Mapped[String] = mapped_column(String(50), nullable=False)
    notification_method: Mapped[String] = mapped_column(String(50), nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")

class Weather_Data(Base):
    __tablename__ = "weather_data"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[String] = mapped_column(String(200), nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    conditions: Mapped[String] = mapped_column(String(200), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

class Alerts(Base):
    __tablename__ = "alerts"

    id: Mapped[UUID] = mapped_column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location: Mapped[String] = mapped_column(String(100), nullable=False)
    alert_type: Mapped[String] = mapped_column(String(String(100)), nullable=False)
    message: Mapped[Text] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship("User", back_populates="alerts")