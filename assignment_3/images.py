from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('camera.id'))
    camera = relationship('Camera', back_populates='images', cascade='save-update, merge')
    image_points = relationship('ImagePoint', back_populates='image', cascade='save-update, merge, delete, delete-orphan')

    def __init__(self, camera, image_points=list()):
    	self.camera = camera
    	self.image_points = image_points
