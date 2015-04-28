import sqlalchemy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import db
import matplotlib

from points import Point, ImagePoint, ObjectPoint
from cameras import Camera
from images import Image
from vectors import Vector

def init():
	db.drop_all()
	db.create_all()
	camera = Camera(focal_length=0.02, height=0.23, width=0.23)
	image_1 = Image(camera=camera)
	image_2 = Image(camera=camera)
	object_point_1 = ObjectPoint(x=1, y=0, z=2)
	object_point_2 = ObjectPoint(x=0, y=1, z=3)
	db.session.add(object_point_1)
	db.session.add(object_point_2)
	db.session.add(camera)
	db.session.commit()

init()

def plot(vectors, points):
	fig = plt.figure()
	ax = fig.add_subplot(1, 2, 1, projection='3d')
	for point in points:
		assert issubclass(point.__class__, Point)
		ax.scatter(point.x, point.y, point.z, c='r', marker='o')
	for vector in vectors:
		assert issubclass(type(vector), Vector)
		from_ = vector.from_point
		to = vector.to_point
		ax.plot([from_.x, to.x], [from_.y, to.y], zs=[from_.z, to.z])
	plt.show()

object_points = db.session.query(ObjectPoint).all()

vectors = list()
vectors.append(Vector(from_point=object_points[0], to_point=object_points[1]))
plot(vectors, object_points)
