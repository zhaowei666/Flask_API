from sqlalchemy import Column, Integer, TIMESTAMP, BigInteger
from sqlalchemy.orm import column_property
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import func
from datetime import datetime as dt
import time


@as_declarative()
class Base(object):
    __abstract__ = True

    pk = Column(Integer, primary_key=True)
    created_timestamp = Column(BigInteger, default=time.time)
    updated_timestamp = Column(BigInteger, onupdate=time.time)

    @property
    def created(self):
        return dt.utcfromtimestamp(self.created_timestamp)

    @property
    def updated(self):
        return dt.utcfromtimestamp(self.updated_timestamp)

