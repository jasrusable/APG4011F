import math
import numpy
from random import randint, uniform

from points import Point, ImagePoint, ObjectPoint
from points import PerspectiveCenterPoint
from cameras import Camera
from images import Image
from vectors import Vector

def is_image_point_in_image(image_point, image):
    camera = image.camera
    x_lower_bound = -camera.width / 2
    x_upper_bound = camera.width / 2
    y_lower_bound = -camera.height / 2
    y_upper_bound = camera.height / 2

    if (image_point.x > x_lower_bound and image_point.x < x_upper_bound
        and image_point.y > y_lower_bound and image_point.y < y_upper_bound):
        return True
    return False

def generate_random_image_point(image, tag=None):
    camera = image.camera
    # Should these ranges be (0, camera.heigh * 100) / 100, or like I have them below:
    x = uniform(-camera.height * 100 / 2, camera.height * 100 / 2) / 100
    y = uniform(-camera.width * 100 / 2, camera.width * 100) / 100
    z = -camera.focal_length
    return ImagePoint(x=x, y=y, z=z, tag=tag)

def generate_random_image_points(image, n=25, tag=None):
    points = []
    for i in range(n):
        points.append(generate_random_image_point(image, tag=tag))
    return points

def get_list_of_all_point_from_image(image):
    points = []
    for image_point in image.image_points:
        points.append(image_point)
    return points

def solve_for_object_point(image_point, scale, tag=None):
    image = image_point.image
    rx = math.radians(image.rx)
    ry = math.radians(image.ry)
    rz = math.radians(image.rz)
    cos = math.cos
    sin = math.sin
    perspective_center = image_point.image.perspective_center
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

    result = (scale * R.T * image_point_vector) + perspective_center_vector
    x = result.item(0,0)
    y = result.item(1,0)
    z = result.item(2,0)
    return ObjectPoint(x=x, y=y, z=z, tag=tag)

def solve_for_image_point(image, object_point, scale, tag=None):
    rx = math.radians(image.rx)
    ry = math.radians(image.ry)
    rz = math.radians(image.rz)
    cos = math.cos
    sin = math.sin
    perspective_center = image.perspective_center
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
    perspective_center_vector = numpy.matrix([
        [perspective_center.x],
        [perspective_center.y],
        [perspective_center.z]
    ])
    object_point_vector = numpy.matrix([
        [object_point.x],
        [object_point.y],
        [object_point.z],
    ])

    R = Rx * Ry * Rz

    result = scale * R * (object_point_vector - perspective_center_vector)
    x = result.item(0,0)
    y = result.item(1,0)
    z = result.item(2,0)
    return ImagePoint(x=x, y=y, z=z, tag=tag)