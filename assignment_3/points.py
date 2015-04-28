from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Point(object):
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    marker = Column(String(50))
    colour = Column(String(50))

    def __init__(self, x, y, z, colour, marker):
        self.x = x
        self.y = y
        self.z = z
        self.colour = colour
        self.marker = marker

class ImagePoint(Base, Point):
    __tablename__ = 'image_point'
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship('Image', back_populates='image_points', 
        cascade='save-update, merge')

    def __init__(self, x, y, z, colour='b', marker='o'):
        Point.__init__(self, x=x, y=y, z=z, colour=colour, marker=marker)

class ObjectPoint(Base, Point):
    __tablename__ = 'object_point'
    id = Column(Integer, primary_key=True)

    def __init__(self, x, y, z, colour='k', marker='o'):
        Point.__init__(self, x=x, y=y, z=z, colour=colour, marker=marker)

class PerspectiveCenterPoint(Base, Point):
    __tablename__ = 'perspective_center_point'
    id =Column(Integer, primary_key=True)
    images = relationship('Image', back_populates='perspective_center', 
        cascade='save-update, merge, delete, delete-orphan')

    def __init__(self, x, y, z, colour='r', marker='o', images=list()):
        self.images = images
        Point.__init__(self, x=x, y=y, z=z, colour=colour, marker=marker)
