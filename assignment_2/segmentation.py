

class Segmentation(object):
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = float(x_min)
        self.x_max = float(x_max)
        self.y_min = float(y_min)
        self.y_max = float(y_max)
        self.z_min = float(z_min)
        self.z_max = float(z_max)

