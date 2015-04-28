import sqlalchemy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import db
import matplotlib

from points import Point, ImagePoint, ObjectPoint
from cameras import Camera
from images import Image

def init():
	db.drop_all()
	db.create_all()
	camera = Camera(focal_length=0.02, height=0.23, width=0.23)
	image_1 = Image(camera=camera)
	image_2 = Image(camera=camera)

	db.session.add(camera)
	db.session.commit()

init()

def plot(vectors, points):
	fig = plt.figure()
	ax = fig.add_subplot(1, 2, 1, projection='3d')
	for point in points:
		assert issubclass(point, Point)
		ax.scatter(point.x, point.y, point.z, c='r', marker='o')
	plt.show()

plot(None, db.session.query(ImagePoint, ObjectPoint).all())
