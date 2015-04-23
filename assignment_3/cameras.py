from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Camera(Base):
	__tablename__ = 'camera'
	id = Column(Integer, primary_key=True)
	focal_length = Column(Float, nullable=False)
