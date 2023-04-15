import pygame
import neat
import time
import os
import random

from assets.constants import *
from assets.Bird import Bird
from assets.Base import Base
from assets.Pipe import Pipe

FPS = 30
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


def draw_window(bird, pipes, base, score):
    WIN.blit(BG_IMG, (0, 0))
    bird.draw(WIN)
    for pipe in pipes:
        pipe.draw(WIN)
    text = STAT_FONT.render(f'Score: {score}', 1, (255, 255, 255))
    WIN.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    base.draw(WIN)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()
        add_pipe = False
        rem = []
        base.move()
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)
        if bird.y + bird.img.get_height() >= 730:
            pass
        draw_window(bird, pipes, base, score)
        if score >= 100:
            run = False
    pygame.quit()
    quit()


main()
