import logging
from timing import log_timing, log_timing_
from points import Point

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Subset(object):
    def __init__(self, points=None, path=None, path_line_delim=' '):
        if path and points:
            raise Exception('Cannot create subset using points as well as a file.')
        elif path and not points:
            self.load_points_from_file(path=path, line_delim=path_line_delim)
        elif not path and points:
            self.points = points
        else:
            logger.warn('Created empty subset.')

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

    @log_timing('writing subset file', logger)
    def write_subset_points_to_file(self, path='data/subset.xyz'):
        with open(path, 'w') as f:
            for point in self.points:
                f.write(point.to_line())