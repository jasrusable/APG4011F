import sqlalchemy

import db

from points import Point, ImagePoint, ObjectPoint
from cameras import Camera
from images import Image

#db.create_all()

new_point = Point(x=2, y=4, z=10)
db.session.add(new_point)
db.session.commit()


print(db.session.query(Point).all()[0].z)