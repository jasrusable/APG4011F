import logging
from timing import log_timing
from points import Point


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Subset(object):
    def __init__(self, superset_points=None, segmentation=None, path='points.xyz', path_line_delim=' '):
        self.segmentation = segmentation
        self.superset_points = superset_points
        self.points = []
        self.path = path
        self.path_line_delim = path_line_delim
        if self.path:
            self.load_points_from_file(path=path, line_delim=path_line_delim)

    @log_timing('loaded points from file', logger)
    def load_points_from_file(self, path='points.xyz', line_delim=' '):
        points = []
        with open(path, 'r') as f:
            for line in f:
                parts = line.split(line_delim)
                point = Point(
                    x = float(parts[0]),
                    y = float(parts[1]),
                    z = float(parts[2]),
                    intensity = float(parts[3]),
                    red = float(parts[4]),
                    green = float(parts[5]),
                    blue = float(parts[6]),
                    normal = None,
                    )
                points.append(point)
        self.path = path
        self.points = points

    @log_timing('running segmentation', logger)
    def perform_segmentaion(self):
        for point in self.superset_points:
            x = point.x
            y = point.y
            z = point.y
            if (x > self.segmentation.x_min
                and x < self.segmentation.x_max
                and y > self.segmentation.y_min
                and y < self.segmentation.y_max
                and z > self.segmentation.z_min
                and z < self.segmentation.z_max):
                self.points.append(point)

    @log_timing('writing subset file', logger)
    def write_subset_points_to_file(self, path='data/subset.xyz'):
        with open(path, 'w') as f:
            for point in self.points:
                f.write(point.to_line())