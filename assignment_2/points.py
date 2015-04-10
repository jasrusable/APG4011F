

class Point(object):
    def __init__(self, x, y, z, intensity, red, green, blue, normal):
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.red = red
        self.green = green
        self.blue = blue
        self.normal = normal

    def to_line(self):
    	pass

    def to_xyz_list(self):
    	return [self.x, self.y, self.z]

class Vector(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
