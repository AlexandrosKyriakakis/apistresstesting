import uuid

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UUID

from src.postgres import Base


class TotalLoad(Base):
    __tablename__ = 'total_load'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_time = Column(DateTime, index=True)
    country = Column(String, index=True)
    load = Column(Integer)


class DailyTotalLoad(Base):
    __tablename__ = 'daily_total_load'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, index=True)
    country = Column(String, index=True)
    load = Column(Integer)


class WeeklyTotalLoad(Base):
    __tablename__ = 'weekly_total_load'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, index=True)
    country = Column(String, index=True)
    load = Column(Integer)
    week = Column(Integer)


class MonthlyTotalLoad(Base):
    __tablename__ = 'monthly_total_load'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, index=True)
    country = Column(String, index=True)
    load = Column(Integer)
    month = Column(Integer)
