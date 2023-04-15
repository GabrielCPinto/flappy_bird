import pygame
import os
pygame.font.init()

WIN_HEIGHT = 800
WIN_WIDTH = 500

VEL = 5

POP = 100

BIRD_IMGS = [pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'bird1.png'))), pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'bird2.png'))), pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'bird3.png')))]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'pipe.png')))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'bg.png')))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets\imgs', 'base.png')))

STAT_FONT = pygame.font.SysFont('comicsans', 50)
