from sqlalchemy import Column, Integer, Float, String, DateTime, UniqueConstraint
from database import Base


class Rainfall(Base):
    __tablename__ = "rainfall"

    __table_args__ = (
    UniqueConstraint("latitude", "longitude", "timestamp"),
)
  

    id = Column(Integer, primary_key=True,index=True)
    latitude= Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    precipitation = Column(Float)
    unit = Column(String)
    risk_level=Column(String)
    risk_score=Column(Float)
    


class SoilMoisture(Base):
    __tablename__="soil_moisture"

    id=Column(Integer,primary_key=True,index=True)
    latitude=Column(Float)
    longitude=Column(Float)
    timestamp=Column(DateTime)
    moisture=Column(Float)
    unit = Column(String)


class IncidentReport(Base):
    __tablename__ = "incident_reports"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    role = Column(String)
    state = Column(String)
    problem_type = Column(String)
    location = Column(String)
    description = Column(String)

    photo = Column(String, nullable=True)

    rating = Column(String, nullable=True)
    feedback = Column(String, nullable=True)

    status = Column(String, default="Open")
    created_at = Column(DateTime)