import logging
from timing import log_timing, with_log_timing


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Segmentation(object):
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_min = float(x_min)
        self.x_max = float(x_max)
        self.y_min = float(y_min)
        self.y_max = float(y_max)
        self.z_min = float(z_min)
        self.z_max = float(z_max)

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

@log_timing('reading file', logger)
def get_list_of_lines_from_file(path='raw_subset.txt'):
    with open(path, 'r') as f:
        return f.readlines()

@log_timing('running segmentation', logger)
def perform_segmentaion(lines, segmentation):
    delim = ' '
    lines_for_subset = []
    for line in lines:
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
            lines_for_subset.append(line)
    return lines_for_subset

@log_timing('writing file', logger)
def write_file(list_of_lines, path='output.txt'):  
    with open(path, 'w') as f:
        for line in list_of_lines:
            f.write(line)

segmentation = Segmentation(-53387,-53345,-3754590,-3754558,0,11)
            
jameson = Segmentation(1,3,0,10,0,11)

lines = get_list_of_lines_from_file(r'C:\Users\rssjas005\Desktop\Lidar\jameson.xyz')
subset = perform_segmentaion(lines, jameson)
write_file(subset, path='jameson_subset.xyz')

#read_write_and_segment(read_path=r'C:\Users\rssjas005\Desktop\huge.txt', write_path='output.txt', segmentation=segmentation)



