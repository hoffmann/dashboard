from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from dashboard.database import Base
import time

class Monitor(Base):
    __tablename__ = 'monitors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))#, unique=True)
    url = Column(String())
    interval = Column(Integer)
    checks = relationship("Check")
    runs = relationship("Run", order_by="desc(Run.timestamp)")

    def __repr__(self):
        return '<Monitor %s %s>' % (self.id, self.name)


class Check(Base):
    __tablename__ = 'checks'
    id = Column(Integer, primary_key=True)
    monitor_id = Column(Integer, ForeignKey('monitors.id'))
    field = Column(String(), unique=True)
    warn = Column(String())
    error = Column(String())


    def __repr__(self):
        return '<Check %s %s %s;%s>' % (self.id, self.field, self.warn, self.error)


class Run(Base):
    __tablename__ = 'runs'
    id = Column(Integer, primary_key=True)
    monitor_id = Column(Integer, ForeignKey('monitors.id'))
    timestamp = Column(Integer, default=lambda: int(time.time()))
    status = Column(Integer())
    data = Column(Text())
    alerts = relationship("Alert")
    
    def __repr__(self):
        return '<Run %s %s %s %s>' % (self.id, self.monitor_id, self.timestamp, self.status)

#todo ggf reference auf check
class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('runs.id'))
    field = Column(String())
    message = Column(String())

