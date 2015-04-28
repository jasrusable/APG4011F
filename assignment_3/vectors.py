from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Vector(object):
	def __init__(self, from_point, to_point, colour='k'):
		self.from_point = from_point
		self.to_point = to_point
		self.colour = colour
