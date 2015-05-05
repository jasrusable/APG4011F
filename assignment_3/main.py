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
from init_db import init


init()

points = list()
vectors = list()
my_image = db.session.query(Image).first()

my_image.image_points = generate_random_image_points(my_image, 50)
db.session.add(my_image)
db.session.commit()

for image_point in my_image.image_points:
    points.append(image_point)
    object_point = solve_for_object_point(image_point, 0, 0, 0, 1000)
    points.append(object_point)
    vectors.append(Vector(from_point=image_point.image.perspective_center, to_point=object_point))

points.append(my_image.perspective_center)

plot(vectors, points)
