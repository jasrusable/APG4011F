import math
import numpy
from random import randint, uniform

from points import Point, ImagePoint, ObjectPoint
from points import PerspectiveCenterPoint
from cameras import Camera
from images import Image
from vectors import Vector

def generate_random_image_point(image):
    camera = image.camera
    # Should these ranges be (0, camera.heigh * 100) / 100, or like I have them below:
    x = uniform(-camera.height * 100 / 2, camera.height * 100 / 2) / 100
    y = uniform(-camera.width * 100 / 2, camera.width * 100) / 100
    z = -camera.focal_length
    return ImagePoint(x=x, y=y, z=z)

def generate_random_image_points(image, n=25):
    points = []
    for i in range(n):
        points.append(generate_random_image_point(image))
    return points

def get_list_of_all_point_from_image(image):
    points = []
    for image_point in image.image_points:
        points.append(image_point)
    return points

def solve_for_object_point(image_point, rx, ry, rz, scale):
    rx = math.radians(rx)
    ry = math.radians(ry)
    rz = math.radians(rz)
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

    result = scale * R.T * image_point_vector + perspective_center_vector
    x = result.item(0,0)
    y = result.item(1,0)
    z = result.item(2,0)
    return ObjectPoint(x=x, y=y, z=z)