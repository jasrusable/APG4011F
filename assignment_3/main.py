import math
import sqlalchemy
import numpy
import copy
from random import randint, uniform
from sqlalchemy.orm import make_transient

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
from utils import add_random_errors_to_point


points_to_plot = list()
vectors_to_plot = list()

def init():
    db.drop_all()
    db.create_all()
    camera = Camera(focal_length=0.9, height=0.23, width=0.23)
    pc_1 = PerspectiveCenterPoint(x=100, y=0, z=4000)
    pc_2 = PerspectiveCenterPoint(x=500, y=0, z=3000)
    image_1 = Image(tag='image_1', camera=camera, perspective_center=pc_1, rx=0, ry=0, rz=0)
    image_2 = Image(tag='image_2', camera=camera, perspective_center=pc_2, rx=0, ry=0, rz=0)
    db.session.add(camera)
    db.session.commit()

init()

points_to_plot += db.session.query(PerspectiveCenterPoint).all()

first_image = db.session.query(Image).filter(Image.tag=='image_1').one()
second_image = db.session.query(Image).filter(Image.tag=='image_2').one()

# Add 30 random image points to first image
def add_random_points_to_image(image, n=30, colour=None, tag='pure'):
    image.image_points = generate_random_image_points(image, n, tag=tag)
    if colour:
        for point in image.image_points:
            point.colour = colour
    db.session.add(image)
    db.session.commit()

# Create object points using an images' image points
def add_corresponding_object_points_to_image_points(image, scale, tag='pure'):
    for image_point in image.image_points:
        object_point = solve_for_object_point(image_point, scale, tag)
        image_point.object_point = object_point
        db.session.add(image_point)
        db.session.add(object_point)
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
            pass
    db.session.commit()

def create_errored_points(points, x_min, x_max, y_min, y_max, z_min, z_max, tag='errored', colour='y'):
    for point in points:
        db.session.expunge(point)
        make_transient(point)
        point.id = None
        errored_point = add_random_errors_to_point(point, x_min, x_max, y_min, y_max, z_min, z_max)
        errored_point.tag = tag
        errored_point.colour = colour
        db.session.add(errored_point)
    db.session.commit()


add_random_points_to_image(first_image, colour='b', tag='pure')
add_corresponding_object_points_to_image_points(first_image, 10000, 'pure')
add_image_points_from_object_points(second_image, db.session.query(ObjectPoint).all(), 1/10000, colour='b', tag='pure')
create_errored_points(db.session.query(ObjectPoint).all(), -5, 5, -5, 5, -5, 5)

points_to_plot += db.session.query(ObjectPoint).all()
points_to_plot += db.session.query(ImagePoint).all()

def populate_vectors_to_plot_list():
    for object_point in db.session.query(ObjectPoint).all():
        if len(object_point.image_points) > 1:
            for image_point in object_point.image_points:
                vectors_to_plot.append(Vector(from_point=image_point.image.perspective_center, to_point=object_point))
print(len(points_to_plot))
plot(vectors_to_plot, points_to_plot)
