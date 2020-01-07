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

pixel_size = 1

def set_pixel(pixel, color = black):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)

def get_pixel(pixel):
    surface = pygame.display.get_surface()
    return surface.get_at(pixel)

def generate_bresenham_line(point_A, point_B, pixels):
    x1, y1 = point_A
    x2, y2 = point_B

    h = abs(x2 - x1)
    v = abs(y2 - y1)

    incX = 1
    incY = 1
    reverse = False

    if x2 < x1 :
        incX = -1
    if y2 < y1:
        incY = -1

    if h < v:
        reverse = True
        a = h
        h = v
        v = a

    inc_up = 2 * v - 2 * h
    inc_dn = 2 * v

    x = x1
    y = y1
    est = 2 * v - h

    for i in range(h):
        pixels.append((x, y))

        if est >= 0:
            est += inc_up
            x += incX
            y += incY
        else:
            est += inc_dn

            if reverse:
                y += incY
            else:
                x += incX

def set_pixel_if_not_set(pixel, color):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            if get_pixel((pixel[0] + i, pixel[1] + j)) == white : 
                pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)

def draw_line(point_A, point_B):
    line = []

    generate_bresenham_line(point_A, point_B, line)
    for pixel in line:
        set_pixel(pixel, black)

    pygame.display.flip()

    for pixel in line:
        x, y = pixel
        surroundig_pixels = [(x - pixel_size, y - pixel_size), (x, y - pixel_size), (x + pixel_size, y - pixel_size),
                             (x - pixel_size, y),                                   (x + pixel_size, y),
                             (x - pixel_size, y + pixel_size), (x, y + pixel_size), (x + pixel_size, y + pixel_size)]
        for p in surroundig_pixels:
            set_pixel_if_not_set(p, red)

        pygame.display.flip() 
        time.sleep(0.1)


pygame.init()

pixel_size = input("Enter pixel size:\n")

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
            set_pixel(last_click)
            if first_point == ():
                first_point = last_click
            elif second_point == ():
                second_point = last_click


    if first_point != () and second_point != ():
        draw_line(first_point, second_point)
        first_point = second_point = ()
    
    pygame.display.flip()