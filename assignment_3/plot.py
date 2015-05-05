import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

from points import Point
from vectors import Vector

def plot(vectors, points):
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1, projection='3d')
	for point in points:
		assert issubclass(point.__class__, Point)
		ax.scatter(point.x, point.y, point.z, c='r', marker='o')
	for vector in vectors:
		assert issubclass(type(vector), Vector)
		from_ = vector.from_point
		to = vector.to_point
		ax.plot([from_.x, to.x], [from_.y, to.y], zs=[from_.z, to.z])
	ax.set_autoscale_on(False) 
	plt.show()
