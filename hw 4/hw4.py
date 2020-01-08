from __future__ import division
import pygame
import sys
import math
import random
import time
from pygame import gfxdraw

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
aquamarine = (0, 255, 255)
yellow = (255, 255, 0)
colors = [black, red, green, blue, purple, yellow, aquamarine]
colors_count = len(colors)

def set_pixel(pixel, color = black, pixel_size = 1):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)


def generate_simple_line(point_A, point_B, pixels):
    x1, y1 = point_A
    x2, y2 = point_B

    h = abs(x2 - x1)
    v = abs(y2 - y1)

    sx = False
    sy = False

    if x2 < x1:
        sx = True
    if y2 < y1:
        sy = True

    reverse = False

    if h < v:
        reverse = True
        a = h
        h = v
        v = a

    if h == 0:
        pixels.append((x1,y1))
        return

    slope = v / h

    for i in range(h):
        x = i
        y = int(math.floor(slope*x + 0.5))

        if reverse:
            a = x
            x = y
            y = a
        if sx:
            x = -x
        if sy:
            y = -y

        pixels.append((x + x1, y + y1))


def draw_lines_and_points(points, color = black, draw_points = True):

    if draw_points:
        for point in points:
            set_pixel((point[0] - 3, point[1] - 3), color, 6)

    if len(points) <= 1:
        return;

    lines = []

    for i in range(len(points) - 1):
        generate_simple_line(points[i], points[i + 1], lines)

    for pixel in lines:
        set_pixel(pixel, color)

def draw_cutting_object(cutting_object_points):
    if len(cutting_object_points) == 1:
        #draw_lines_and_points(cutting_object_points, blue, False)
        return

    if(cutting_object == 'p'):
        draw_lines_and_points(cutting_object_points, blue)
        draw_lines_and_points([cutting_object_points[0]], white)
        return

    #else - rect cutting
    points = [cutting_object_points[0]]
    points.append((cutting_object_points[1][0], cutting_object_points[0][1]))
    points.append(cutting_object_points[1])
    points.append((cutting_object_points[0][0], cutting_object_points[1][1]))
    points.append(cutting_object_points[0])
    draw_lines_and_points(points, blue, False)

def calculate_and_draw_cutting():
    cut_points = []
    if cutting_object == 'p':
        calculate_half_plane_cutting(cutting_object_points, current_polygon_points, cut_points)
    elif cutting_object == 'r':
        calculate_rectangle_cutting(cutting_object_points[0], cutting_object_points[1], current_polygon_points, cut_points)

    if len(cut_points) > 0:
        cut_points.append(cut_points[0])

    draw_lines_and_points(cut_points, red, False)

def calculate_rectangle_side_cutting(polygon_verts, cut_points, inside_check, intersection_point):
    verts_len = len(polygon_verts)
    for i in range(verts_len):
        edge_p1 = polygon_verts[i];
        edge_p2 = polygon_verts[(i + 1) % verts_len]

        p1_inside = inside_check(edge_p1)
        p2_inside = inside_check(edge_p2)

        if p1_inside and p2_inside:
            cut_points.append(edge_p2)
        elif not(p1_inside or p2_inside):
            continue
        else:
            crosspoint = intersection_point([edge_p1, edge_p2])

            if (not p1_inside) and p2_inside:
                cut_points.append(crosspoint)
                cut_points.append(edge_p2)
            else:
                cut_points.append(crosspoint)

def calculate_rectangle_cutting(top_left, bottom_right, polygon_verts, cut_points):
    top_right = (bottom_right[0], top_left[1])
    bottom_left = (top_left[0], bottom_right[1])

    current_points = current_polygon_points
    result_points = []
    calculate_rectangle_side_cutting(current_points, result_points, lambda point : point[0] >= top_left[0], lambda line : get_point_from_line_with_min_x(line[0], line[1], top_left[0]))

    current_points = result_points;
    result_points = []
    calculate_rectangle_side_cutting(current_points, result_points,  lambda point : point[1] >= top_left[1], lambda line : get_point_from_line_with_y(line[0], line[1], top_left[1]))

    current_points = result_points;
    result_points = []
    calculate_rectangle_side_cutting(current_points, result_points,  lambda point : point[0] <= bottom_right[0], lambda line : get_point_from_line_with_x(line[0], line[1], bottom_right[0]))

    calculate_rectangle_side_cutting(result_points, cut_points, lambda point : point[1] <= bottom_right[1], lambda line : get_point_from_line_with_max_y(line[0], line[1], bottom_right[1]))

def get_lines_intesection(l1_points, l2_points):
    l1x1, l1y1 = l1_points[0]
    l1x2, l1y2 = l1_points[1]
    m1 = 0
    if not l1x2 == l1x1:
        m1 = float(l1y2 - l1y1) / float(l1x2 - l1x1)

    l2x1, l2y1 = l2_points[0]
    l2x2, l2y2 = l2_points[1]
    m2 = 0
    if not l2x2 == l2x1:
        m2 = float(l2y2 - l2y1) / float(l2x2 - l2x1)

    x = float((m1 * l1x1) - (m2 * l2x1) - l1y1 + l2y1) / float(m1 - m2)
    y = m1 * (x - l1x1) + l1y1

    return (int(x), int(y))

def get_point_from_line_with_x(p1, p2, x):
    x1, y1 = p1
    x2, y2 = p2
    m = 0
    if not x2 == x1:
        m = float(y2 - y1) / float(x2 - x1)

    y = m * (x - x1) + y1

    return (int(x), int(y))

def get_point_from_line_with_y(p1, p2, y):
    x1, y1 = p1
    x2, y2 = p2
    m = 0
    if not x2 == x1:
        m = float(y2 - y1) / float(x2 - x1)

    x = 0
    if not m == 0:
        x = (y - y1 + (m * x1)) / m

    return (int(x), int(y))

def get_point_from_line_with_min_x(p1, p2, x):
    x1, y1 = p1
    x2, y2 = p2

    y = y1 + float(y2 - y1) * float(x - x1) / float(x2 - x1)

    return (int(x), int(y))

def get_point_from_line_with_max_y(p1, p2, y):
    x1, y1 = p1
    x2, y2 = p2
    
    x = x1 + float(x2 - x1) * float(y - y1) /  float(y2 - y1)

    return (int(x), int(y))

def calculate_half_plane_cutting(vector, polygon_verts, cut_points, inside_point = ()):

    p1 = vector[0];
    p2 = vector[1]
    x1, y1 = p1
    x2, y2 = p2
    m = 0
    if not x2 == x1:
        m = float(y2 - y1) / float(x2 - x1)

    if inside_point == ():
        ox, oy = p1
        px, py = p2
        angle = -math.pi / 6.0;
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        inside_point = (int(qx), int(qy))

    get_line_eq = lambda point: m * (point[0] - x1) - point[1] + y1

    test_point_val = get_line_eq(inside_point)

    check_same_sign = lambda v1, v2 : ((v1 > 0) and ( v2 > 0)) or ((v1 < 0) and (v2 < 0))

    verts_len = len(polygon_verts)
    for i in range(verts_len):
        edge_p1 = polygon_verts[i];
        edge_p2 = polygon_verts[(i + 1) % verts_len]

        p1_val = get_line_eq(edge_p1)
        p2_val = get_line_eq(edge_p2)

        p1_inside = check_same_sign(test_point_val, p1_val)
        p2_inside = check_same_sign(test_point_val, p2_val)

        if p1_inside and p2_inside:
            cut_points.append(edge_p2)
        elif not(p1_inside or p2_inside):
            continue
        else:
            crosspoint = get_lines_intesection(vector, [edge_p1, edge_p2])

            if (not p1_inside) and p2_inside:
                cut_points.append(crosspoint)
                cut_points.append(edge_p2)
            else:
                cut_points.append(crosspoint)


pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)

current_polygon_points = []
polygon_closed = False
cutting_object = 'p'
cutting_object_points = [];

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                polygon_closed = True
                draw_lines_and_points([current_polygon_points[-1], current_polygon_points[0]])
            elif event.key == pygame.K_p:
                cutting_object = 'p'
            elif event.key == pygame.K_r:
                cutting_object = 'r'
        elif event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if not polygon_closed:
                if(len(current_polygon_points) == 0):
                    polygon_closed = False
                current_polygon_points.append(last_click);
                draw_lines_and_points(current_polygon_points[-2:])
            elif len(cutting_object_points) < 2:
                cutting_object_points.append(last_click);
                draw_cutting_object(cutting_object_points)
                if len(cutting_object_points) == 2:
                    calculate_and_draw_cutting()
                    current_polygon_points = []
                    polygon_closed = False
                    cutting_object_points = [];

    pygame.display.flip()
