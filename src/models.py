from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class BaseClass:
    __abstract__ = True
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
