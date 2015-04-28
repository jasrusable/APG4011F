import sqlalchemy

import db
from points import Point, ImagePoint, ObjectPoint
from cameras import Camera
from images import Image
from vectors import Vector
from plot import plot

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

object_points = db.session.query(ObjectPoint).all()

vectors = list()
vectors.append(Vector(from_point=object_points[0], to_point=object_points[1]))
plot(vectors, object_points)
