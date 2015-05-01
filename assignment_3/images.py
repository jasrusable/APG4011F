from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    camera_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    camera = relationship('Camera', back_populates='images', cascade='save-update, merge')
    image_points = relationship('ImagePoint', back_populates='image', 
        cascade='save-update, merge, delete, delete-orphan')
    perspective_center_id = Column(Integer, ForeignKey('perspective_center_point.id'), nullable=False)
    perspective_center = relationship('PerspectiveCenterPoint', back_populates='images', 
        cascade='save-update, merge, delete, delete-orphan', single_parent=True)

    def __init__(self, camera, perspective_center, image_points=list()):
        self.camera = camera
        self.perspective_center = perspective_center
        self.image_points = image_points
