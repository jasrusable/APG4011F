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

def init():
    db.drop_all()
    db.create_all()
    camera = Camera(focal_length=0.02, height=0.23, width=0.23)
    pc_1 = PerspectiveCenterPoint(x=10, y=0, z=10)
    #pc_2 = PerspectiveCenterPoint(x=1, y=0, z=10)
    image_1 = Image(camera=camera, perspective_center=pc_1)
    #image_2 = Image(camera=camera, perspective_center=pc_2)
    db.session.add(camera)
    db.session.commit()

init()


def solve_for_object_point(image_point, rx, ry, rz, sx, sy, sz):
    cos = math.cos
    sin = math.sin
    perspective_center = image_point.image.perspective_center
    S = numpy.matrix([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, sz],
    ])
    Rx = numpy.matrix([
        [1, 0, 0],
        [0, cos(rx), sin(rx)],
        [0, -sin(rx), cos(rx)]
    ])
    Ry = numpy.matrix([
        [cos(ry), 0, -sin(ry)],
        [0, 1, 0],
        [sin(ry), 0, cos(ry)]
    ])
    Rz = numpy.matrix([
        [cos(rz), sin(rz), 0],
        [-sin(rz), cos(rz), 0],
        [0, 0, 1]
    ])
    image_point_vector = numpy.matrix([
        [image_point.x], 
        [image_point.y], 
        [image_point.z]
    ])
    perspective_center_vector = numpy.matrix([
        [perspective_center.x],
        [perspective_center.y],
        [perspective_center.z]
    ])

    R = Rx * Ry * Rz

    result = S * R.T * image_point_vector + perspective_center_vector
    x = result.item(0,0)
    y = result.item(1,0)
    z = result.item(2,0)
    return ObjectPoint(x=x, y=y, z=z)

points = list()
vectors = list()
my_image = db.session.query(Image).first()

my_image.image_points = generate_random_image_points(my_image, 50)

for image_point in my_image.image_points:
    object_point = solve_for_object_point(image_point, 0, 0, 0, 100, 100, 100)
    points.append(object_point)
    vectors.append(Vector(from_point=image_point.image.perspective_center, to_point=object_point))

points.append(my_image.perspective_center)


plot(vectors, points)
