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

use_bresenham_to_draw_circle = False
pixel_size = 1

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def set_pixel(pixel, color = black):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)

def four_symmetric(xc, yc, x, y, pixels, fill_rows):
    pixels.append((xc + x, yc + y))
    pixels.append((xc - x, yc - y))
    pixels.append((xc - x, yc + y))
    pixels.append((xc + x, yc - y))
    fill_rows.append((xc - x, xc + x, yc + y));
    fill_rows.append((xc - x, xc + x, yc - y));



def put_pixel_row(xleft, xright, y, color):
    for x in range(xleft, xright + 1):
        set_pixel((x, y), color)

def draw_circle(center, r, use_bresenham):
    circle = []
    fill_rows = []

    xc, yc = center
    x = r
    y = 0
    d = 2 - 2 * r

    while x >= 0:
        four_symmetric(xc, yc, x, y, circle, fill_rows)

        if d < 0:
            D = 2 * d + 2 * x - 1

            if D <= 0:
                y += pixel_size
                d += 2 * y + 1
                continue
        elif d > 0:
            D = 2 * d - 2 * y - 1
            if D >= 0:
                x -= pixel_size
                d -= 2 * x - 1
                continue
        
        x -= pixel_size
        y += pixel_size
        d += 2 * y - 2 * x + 2

    color = colors[int(random.random() * 10) % colors_count]
    for pixel in circle:
        set_pixel(pixel, color)

    for (xl, xr, y) in fill_rows:
        put_pixel_row(xl, xr, y, color);

pixel_size = input("Enter pixel size:\n")

pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)
first_point = second_point = ()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if first_point == ():
                set_pixel(last_click)
                first_point = last_click
            elif second_point == ():
                second_point = last_click


    if first_point != () and second_point != ():
        draw_circle(first_point, int(distance(first_point, second_point)), True)
        first_point = second_point = ()
    
    pygame.display.flip()
