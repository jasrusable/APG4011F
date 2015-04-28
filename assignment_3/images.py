from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('camera.id'))
    camera = relationship('Camera', back_populates='images', cascade='save-update, merge')
    image_points = relationship('ImagePoint', back_populates='image', cascade='save-update, merge, delete, delete-orphan')
    perspective_center_id = Column(Integer, ForeignKey('perspective_center_point.id'))
    perspective_center = relationship('PerspectiveCenterPoint', back_populates='images', cascade='save-update, merge')

    def __init__(self, camera, image_points=list()):
    	self.camera = camera
    	self.image_points = image_points
