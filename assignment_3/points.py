from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Point(object):
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)

class ImagePoint(Base, Point):
    __tablename__ = 'image_point'
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('image.id'))
    image = relationship('Image', back_populates='image_points', cascade='save-update, merge')

    def __init__(self, x, y, z):
        Point.__init__(self, x=x, y=y, z=z)

class ObjectPoint(Base, Point):
    __tablename__ = 'object_point'
    id = Column(Integer, primary_key=True)

    def __init__(self, x, y, z):
        Point.__init__(self, x=x, y=y, z=z)
