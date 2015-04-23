from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base

""" I am using joined table inheritance here """

class Point(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity':'point',
        'polymorphic_on':type
    }

class ImagePoint(Point):
    __tablename__ = 'image_point'
    id = Column(Integer, ForeignKey('point.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'image_point',
    }


class ObjectPoint(Point):
    __tablename__ = 'object_point'
    id = Column(Integer, ForeignKey('point.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'object_point',
    }
