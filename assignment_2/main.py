import logging
from timing import log_timing, with_log_timing
from subsets import Subset
from points import Point
from segmentation import Segmentation

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)



@log_timing('everything', logger)    
def read_write_and_segment(read_path='', write_path='', segmentation=None, delim=' '):
    with open(read_path, 'r') as f:
        with open(write_path, 'w') as g:
            for line in f:
                parts = line.split(delim)
                x = float(parts[0])
                y = float(parts[1])
                z = float(parts[2])
                if (x > segmentation.x_min
                    and x < segmentation.x_max
                    and y > segmentation.y_min
                    and y < segmentation.y_max
                    and z > segmentation.z_min
                    and z < segmentation.z_max):
                    g.write(line)


@log_timing('running segmentation', logger)
def perform_segmentaion(points, segmentation):
    delim = ' '
    for point in points:
        parts = point.raw_line.split(delim)
        x = float(parts[0])
        y = float(parts[1])
        z = float(parts[2])
        if (x > segmentation.x_min
            and x < segmentation.x_max
            and y > segmentation.y_min
            and y < segmentation.y_max
            and z > segmentation.z_min
            and z < segmentation.z_max):
            segmentation.points.append(point)
    return segmentation

@log_timing('reading file', logger)
def get_points_from_file(path='raw_subset.txt'):
    points = []
    with open(path, 'r') as f:
        for line in f:
            points.append(Point(raw_line=line))
    return points


@log_timing('writing file', logger)
def write_file(points_dict, path='output.txt'):  
    with open(path, 'w') as f:
        for line in points_dict:
            f.write(line)

     
superset_points = get_points_from_file('data/Lidar/jameson.xyz')  
jameson_segmentation = Segmentation(1,3,0,10,0,11)
jameson_subset = Subset(superset_points, jameson_segmentation)
jameson_subset.write_subset_points_to_file('data/jameson_subset.xyz')
