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
