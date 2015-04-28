from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref
from db import Base


class Camera(Base):
	__tablename__ = 'camera'
	id = Column(Integer, primary_key=True)
	focal_length = Column(Float, nullable=False, default=0.02)
	width = Column(Float, nullable=False)
	height = Column(Float, nullable=False)
	images = relationship('Image', back_populates='camera', 
		cascade='save-update, merge')

	def __init__(self, focal_length, width, height):
		self.focal_length = focal_length
		self.width = width
		self.height = height
