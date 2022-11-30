from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey

from ldskbkp.database.connection import Base
from ldskbkp.database.models.LdbkRun import LdbkRun


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    path = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    sha256 = Column(Text(32), nullable=False)
    mime = Column(Text, nullable=False)
    backed_up = Column(Boolean, nullable=False)
    created_on = Column(DateTime, nullable=False)
    modified_on = Column(DateTime, nullable=False)
    backup_uuids = Column(Text)
    split = Column(Boolean)
    split_parts = Column(Integer)
    compressed = Column(Boolean)
    encrypted = Column(Boolean)
    ldbk_run_uuid = Column(ForeignKey(LdbkRun.run_uuid))

