from sqlalchemy import Column, Integer, Text, Boolean

from ldskbkp.database.connection import Base


class Config(Base):
    __tablename__ = 'configuration'
    key = Column(Text, nullable=False, primary_key=True)
    value = Column(Text, nullable=False)

