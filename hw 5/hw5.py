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

CONTOL_LINES_ON = True
CONTROL_COLOR = (0, 51, 51)
SEGMENT_COUNT = 500

points = []

control_points = [[]]

curves = []

def set_pixel(pixel, color = black, pixel_size = 1):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)


def caluclate_bezier_point(points, t):
    u = 1 - t
    tt = t ** 2;
    uu = u ** 2
    
    a = (1 - t) ** 3
    b = 3 * ((1 - t) ** 2) * t
    c = 3 * (1 - t) * (t ** 2)
    d = t ** 3
    xp = (a * points[0][0]) + (b * points[1][0]) + (c * points[2][0]) + (d * points[3][0])
    yp = (a * points[0][1]) + (b * points[1][1]) + (c * points[2][1]) + (d * points[3][1]) 
 
    return (xp, yp)


def calculate_bezier_curve_cubic(points, curve):
    for i in range(SEGMENT_COUNT):
        t = i / SEGMENT_COUNT
        pixel = caluclate_bezier_point(points, t)
        curve.append(pixel)


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


def draw_contol_lines_and_points():

    if not CONTOL_LINES_ON:
        return;

    for points in control_points:
        for point in points:
            set_pixel((point[0] - 3, point[1] - 3), CONTROL_COLOR, 6)

        if len(points) <= 1:
            continue

        lines = []

        for i in range(len(points) - 1):
            generate_simple_line(points[i], points[i + 1], lines)

        for pixel in lines:
            set_pixel(pixel, CONTROL_COLOR)

        

def add_bezier_curve(points):
    curves.append([])
    calculate_bezier_curve_cubic(points, curves[-1])    

def draw_bezier_curves():
    for curve in curves:
        color = red
        for point in curve:
            set_pixel((int(point[0]), int(point[1])), color)


pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)

control_points = [[(249, 101), (307, 141), (308, 213), (248, 246)],
                  [(338, 99), (276, 138), (275, 210), (347, 242)]]

for points in control_points:
    add_bezier_curve(points)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                if CONTOL_LINES_ON:
                    CONTOL_LINES_ON = False
                else:
                    CONTOL_LINES_ON = True
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if len(control_points[-1]) < 4:
                control_points[-1].append(last_click)
                if len(control_points[-1]) == 4:
                    add_bezier_curve(control_points[-1])
                    pygame.display.flip()
                    control_points.append([])
    
    pygame.display.get_surface().fill(white)
    draw_contol_lines_and_points()
    draw_bezier_curves()

    pygame.display.flip()
