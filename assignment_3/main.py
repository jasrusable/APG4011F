import math
import sqlalchemy
import numpy
from random import randint

import db
from points import Point, ImagePoint, ObjectPoint
from points import PerspectiveCenterPoint
from cameras import Camera
from images import Image
from vectors import Vector
from plot import plot
from utils import generate_random_image_points
from utils import get_list_of_all_point_from_image
from utils import solve_for_object_point
from utils import solve_for_image_point
from utils import is_image_point_in_image


points_to_plot = list()
vectors_to_plot = list()

def init():
    db.drop_all()
    db.create_all()
    camera = Camera(focal_length=0.2, height=0.23, width=0.23)
    pc_1 = PerspectiveCenterPoint(x=100, y=0, z=3000)
    pc_2 = PerspectiveCenterPoint(x=200, y=0, z=3000)
    image_1 = Image(tag='image_1', camera=camera, perspective_center=pc_1, rx=0, ry=0, rz=0)
    image_2 = Image(tag='image_2', camera=camera, perspective_center=pc_2, rx=0, ry=0, rz=0)
    db.session.add(camera)
    db.session.commit()

init()

points_to_plot += db.session.query(PerspectiveCenterPoint).all()

first_image = db.session.query(Image).filter(Image.tag=='image_1').one()
second_image = db.session.query(Image).filter(Image.tag=='image_2').one()

# Add 30 random image points to first image
def add_random_points_to_image(image, n=2, colour=None, tag='pure'):
	image.image_points = generate_random_image_points(image, n, tag=tag)
	if colour:
		for point in image.image_points:
			point.colour = colour
	db.session.add(image)
	db.session.commit()

# Create object points using an images' image points
def add_object_points_to_image_points(image, scale, tag='pure'):
	for image_point in image.image_points:
	    object_point = solve_for_object_point(image_point, scale, tag)
	    image_point.object_point = object_point
	    db.session.add(image_point)
	db.session.commit()

# Create image points given an image and object points
def add_image_points_from_object_points(image, object_points, scale, colour=None, tag='pure'):
	for object_point in object_points:
		image_point = solve_for_image_point(image, object_point, scale, tag)	
		if colour:
			image_point.colour = colour
		if is_image_point_in_image(image_point, image):
			image.image_points.append(image_point)
			object_point.image_points.append(image_point)
			db.session.add(image)
			db.session.add(object_point)
		else:
			print('not in image.')
	db.session.commit()

add_random_points_to_image(first_image, colour='k')
add_object_points_to_image_points(first_image, 10000)
add_image_points_from_object_points(second_image, db.session.query(ObjectPoint).all(), 1/10000, colour='k')

points_to_plot += db.session.query(ObjectPoint).all()
points_to_plot += db.session.query(ImagePoint).all()


plot(vectors_to_plot, points_to_plot)
