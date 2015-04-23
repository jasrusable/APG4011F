from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from db import Base


class Camera(Base):
	__tablename__ = 'camera'
	id = Column(Integer, primary_key=True)
	focal_length = Column(Float, nullable=False, default=0.02)
	images= relationship('Image', backref=backref('camera'))
