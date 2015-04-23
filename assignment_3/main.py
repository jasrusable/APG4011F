import sqlalchemy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import db
import matplotlib

from points import Point, ImagePoint, ObjectPoint
from cameras import Camera
from images import Image

db.drop_all()
db.create_all()

def init():
	pass

init()

def plot(vectors, points):
	fig = plt.figure()
	ax = fig.add_subplot(1, 2, 1, projection='3d')
	for point in points:
		ax.scatter(point.x, point.y, point.z, c='r', marker='o')
	plt.show()

#plot(None, db.session.query(Point).all())
c = Camera()
i = Image()