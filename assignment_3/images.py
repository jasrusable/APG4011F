from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    width = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
