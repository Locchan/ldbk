from sqlalchemy import Column, Integer, Text, Boolean, DateTime

from ldskbkp.database.connection import Base

class LdbkRun(Base):
    __tablename__ = 'ldbk_runs'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    run_datetime = Column(DateTime, nullable=False)
    run_uuid = Column(Text(32), nullable=True)