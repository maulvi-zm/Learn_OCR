import cv2

import src


def process(im):
    im = cv2.bitwise_not(im)
    # cv2.imshow("afterbitwise",im)
    # cv2.waitKey(0)
    # edgesdef = src.detect_edges(im, blur_radius=7, thr1=0)
    edges = src.detect_edges(im, blur_radius=7)
    # cv2.imshow("edgesdef",edgesdef)
    cv2.imshow("edges",edges)

    lines_unique = src.detect_lines(edges)
    # cv2.imshow("line",lines_unique)
    print(lines_unique)
    _intersections = src.find_intersections(lines_unique, im)
    print(_intersections)
    return src.find_quadrilaterals(_intersections)


def draw(rects, im, debug=False):
    if len(rects) == 0:
        return im
    if debug:
        [draw_rect(im, rect, (0, 255, 0), 2) for rect in rects]
    best = max(rects, key=_area)
    if best:
        draw_rect(im, best)
    return im


def _area(rect): #luas terbesar
    x, y = zip(*rect)
    width = max(x) - min(x)
    height = max(y) - min(y)
    return width * height


def draw_rect(im, rect, col=(255, 0, 0), thickness=5):
    [cv2.line(im, rect[i], rect[(i+1) % len(rect)], col, thickness=thickness) for i in range(len(rect))]
