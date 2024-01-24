# -*- coding: utf-8 -*-
from src.canny import detect_edges
from src.houghTransform import detect_lines
from src.intersection import find_intersections
from src.quadrilateral import find_quadrilaterals
from src.main import process, draw

from os.path import dirname, realpath, join
from cv2 import imread

pwd = dirname(realpath(__file__))
im_folder = join(pwd, 'test')
# im = imread(join(pwd, 'res', 'sample.jpg'))
