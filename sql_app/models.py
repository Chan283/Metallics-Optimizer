from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Commodity(Base):
    __tablename__ = "commodities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    inventory = Column(Float)
    price = Column(Float)

    chemicals = relationship("Chemical", back_populates="cmdty")


class Chemical(Base):
    __tablename__ = "chemicals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    percentage=Column(Integer)
    cmdty_id = Column(Integer, ForeignKey("commodities.id"))

    cmdty = relationship("Commodity", back_populates="chemicals")
