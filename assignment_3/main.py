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


points_to_plot = list()
vectors_to_plot = list()

def init():
    db.drop_all()
    db.create_all()
    camera = Camera(focal_length=0.2, height=0.23, width=0.23)
    pc_1 = PerspectiveCenterPoint(x=100, y=0, z=3000)
    pc_2 = PerspectiveCenterPoint(x=200, y=0, z=3000)
    image_1 = Image(tag='image_1', camera=camera, perspective_center=pc_1)
    image_2 = Image(tag='image_2', camera=camera, perspective_center=pc_2)
    db.session.add(camera)
    db.session.commit()
init()

first_image = db.session.query(Image).filter(Image.tag=='image_1').one()

# Add 30 random image points to first image
def add_random_points_to_image(image, n=30, tag=None):
	image.image_points = generate_random_image_points(image, n, tag=tag)
	db.session.add(image)
	db.session.commit()

# Create object points using an images' image points
def add_object_points_to_image_points(image, rx, ry, rz, scale, tag=None):
	for image_point in image:
	    object_point = solve_for_object_point(image_point, rx, ry, rz, scale, tag)
	    image_point.object_point = object_point
	    db.session.add(image_point)
	db.session.commit()

def add_image_points_from_object_points(image, object_points):
	pass


#plot(vectors_to_plot, points_to_plot)
