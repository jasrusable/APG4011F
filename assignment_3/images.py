from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    width = Column(Float, nullable=False, default=0.02)
    width = Column(Float, nullable=False, default=0.02)
    camera_id = Column(Integer, ForeignKey('camera.id'))
