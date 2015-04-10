from timing import log_timing
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Subset(object):
    def __init__(self, superset_points, segmentation):
        self.segmentation = segmentation
        self.superset_points = superset_points
        self.points = []
        self.perform_segmentaion()

    @log_timing('running segmentation', logger)
    def perform_segmentaion(self):
        for point in self.superset_points:
            x = point[0]
            y = point[1]
            z = point[2]
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
                f.write(point)