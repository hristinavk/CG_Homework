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


def get_pixel(pixel):
    try:
        surface = pygame.display.get_surface()
        return surface.get_at(pixel)
    except IndexError:
        return black;


def four_symmetric(xc, yc, x, y, pixels):
    pixels.append((xc + x, yc + y))
    pixels.append((xc - x, yc - y))
    pixels.append((xc - x, yc + y))
    pixels.append((xc + x, yc - y))


def eight_symmetric(xc, yc, x, y, pixels):
    four_symmetric(xc, yc, x, y, pixels)
    four_symmetric(xc, yc, y, x, pixels)


def generate_simple_circle(center, r, pixels):
    xc, yc = center
    x = 0
    y = r
    pixels.append((xc, yc + r))
    pixels.append((xc, yc - r))
    pixels.append((xc + r, yc))
    pixels.append((xc - r, yc))

    while(x < y):
        x += 1

        y = int(math.sqrt(float(r * r - x* x)))
        eight_symmetric(xc, yc, x, y, pixels)

    if x == y:
        four_symmetric(xc, yc, x, y, pixels)


def draw_circle(center, r, use_bresenham):
    circle = []
    generate_simple_circle(center, r, circle)
    for pixel in circle:
        set_pixel(pixel, black)


def simple_flood_fill(pixel, color, old_color):
    
    values = [];
    values.append(pixel)

    while len(values) > 0:
        current_pixel = values[-1]
        values.pop()
        pix_color = get_pixel(pixel)

        if(get_pixel(current_pixel) == old_color):
            set_pixel(current_pixel, color)
            time.sleep(0.0005)
            pygame.display.flip()
            x, y = current_pixel;
            values.append((x - 1, y))
            values.append((x + 1, y))
            values.append((x, y - 1))
            values.append((x, y + 1))

num_circles_to_intersect = 2;

pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)

filling_mode = False

first_point = second_point = ()
current_number_of_circles = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                filling_mode =  not filling_mode
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if not filling_mode and current_number_of_circles < num_circles_to_intersect:
                if first_point == ():
                    first_point = last_click
                    pygame.display.flip()
                elif second_point == ():
                    second_point = last_click
                    draw_circle(first_point, int(distance(first_point, second_point)), True)
                    first_point = second_point = ()
                    current_number_of_circles += 1
                    pygame.display.flip()
                if current_number_of_circles == num_circles_to_intersect:
                    filling_mode = True
            else:
                simple_flood_fill(last_click, colors[int(random.random() * colors_count) % colors_count], white)
                pygame.display.flip()
                first_point = second_point = ()
                current_number_of_circles = 0
                
    pygame.display.flip()
