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

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


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
    return

def calculate_half_plabe_cutting():
    return

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
