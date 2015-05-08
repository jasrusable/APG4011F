import math
import sqlalchemy
import numpy
import copy
import sympy
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
    pc_2 = PerspectiveCenterPoint(x=900, y=0, z=3000)
    image_1 = Image(tag='image_1', camera=camera, perspective_center=pc_1, rx=0, ry=0, rz=0)
    image_2 = Image(tag='image_2', camera=camera, perspective_center=pc_2, rx=0, ry=0, rz=0)
    db.session.add(camera)
    db.session.commit()

init()

points_to_plot += db.session.query(PerspectiveCenterPoint).all()

first_image = db.session.query(Image).filter(Image.tag=='image_1').one()
second_image = db.session.query(Image).filter(Image.tag=='image_2').one()

# Add n random image points to first image
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
        object_point.tag = tag
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

def add_error_to_points(points, x_min, x_max, y_min, y_max, z_min, z_max, tag='errored', colour='r'):
    for point in points:
        point = add_random_errors_to_point(point, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, z_min=z_min, z_max=z_max)
        db.session.add(point)
        db.session.commit()

add_random_points_to_image(first_image, colour='b', tag='pure')
add_corresponding_object_points_to_image_points(first_image, 10000, 'pure')
add_image_points_from_object_points(second_image, db.session.query(ObjectPoint).all(), 1/10000, colour='b', tag='pure')
add_error_to_points(db.session.query(ObjectPoint).all(), -50, 50, -50, 500, -50, 500, tag='errored')

points_to_plot += db.session.query(ObjectPoint).all()
points_to_plot += db.session.query(ImagePoint).all()

def populate_vectors_to_plot_list():
    for object_point in db.session.query(ObjectPoint).all():
        if len(object_point.image_points) > 1:
            for image_point in object_point.image_points:
                vectors_to_plot.append(Vector(from_point=image_point.image.perspective_center, to_point=object_point))
populate_vectors_to_plot_list()

#plot(vectors_to_plot, points_to_plot)


def resection(image_points):
    rx = sympy.Symbol('rx')
    ry = sympy.Symbol('ry')
    rz = sympy.Symbol('rz')
    X = sympy.Symbol('X')
    Y = sympy.Symbol('Y')
    Z = sympy.Symbol('Z')
    X0 = sympy.Symbol('X0')
    Y0 = sympy.Symbol('Y0')
    Z0 = sympy.Symbol('Z0')
    k = sympy.Symbol('k')

    cos = sympy.cos
    sin = sympy.sin

    Rx = numpy.matrix([
        [1, 0, 0],
        [0, cos(rx), -sin(rx)],
        [0, sin(rx), cos(rx)]
    ])
    Ry = numpy.matrix([
        [cos(ry), 0, sin(ry)],
        [0, 1, 0],
        [-sin(ry), 0, cos(ry)]
    ])
    Rz = numpy.matrix([
        [cos(rz), -sin(rz), 0],
        [sin(rz), cos(rz), 0],
        [0, 0, 1]
    ])

    R = Rx * Ry * Rz
    obj = numpy.matrix([
        [X],
        [Y],
        [Z],
        ])
    pc = numpy.matrix([
        [X0],
        [Y0],
        [Z0],
        ])

    image_coords = k*R*(obj - pc)
    x = image_coords.item(0)
    y = image_coords.item(1)
    negative_c = image_coords.item(2)

    A = numpy.matrix([[0] * 6,])
    A = numpy.delete(A, (0), axis=0)
    l = numpy.matrix([[0],])
    l = numpy.delete(l, (0), axis=0)
resection()