import logging
from timing import log_timing, with_log_timing
from subsets import Subset
from points import Point
from segmentation import Segmentation


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@log_timing('getting points from file', logger)
def get_points_from_file(path='superset.xyz'):
    points = []
    with open(path, 'r') as f:
        for line in f:
            points.append(Point(raw_line=line))
    return points

     
superset_points = get_points_from_file('data/Lidar/jameson.xyz')  
jameson_segmentation = Segmentation(1,3,0,10,0,11)
jameson_subset = Subset(superset_points, jameson_segmentation)
jameson_subset.write_subset_points_to_file('data/jameson_subset.xyz')
