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
    tag = Column(String(50))
    rx = Column(Float, default=0)
    ry = Column(Float, default=0)
    rz = Column(Float, default=0)

    def __init__(self, camera, perspective_center, rx=0, ry=0, rz=0, tag=None, image_points=list()):
        self.camera = camera
        self.perspective_center = perspective_center
        self.image_points = image_points
        self.tag = tag
        self.rx = rx
        self.ry = ry
        self.rz = rz
