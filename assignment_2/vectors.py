

class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_xyz_list(self):
        return [self.x, self.y, self.z]