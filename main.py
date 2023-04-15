import pygame
import neat
import time
import os
import random
import pickle

from assets.constants import *
from assets.Bird import Bird
from assets.Base import Base
from assets.Pipe import Pipe

FPS = 30
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


def draw_window(birds, pipes, base, score):
    WIN.blit(BG_IMG, (0, 0))
    for bird in birds:
        bird.draw(WIN)
    for pipe in pipes:
        pipe.draw(WIN)
    text = STAT_FONT.render(f'Score: {score}', 1, (255, 255, 255))
    WIN.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    base.draw(WIN)
    pygame.display.update()


def eval_genomes(genomes, config):

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]
    clock = pygame.time.Clock()
    run = True
    score = 0

    while run and len(birds) > 0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (bird.y, abs(bird.y-pipes[pipe_ind].height), abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))
        for r in rem:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < -50:
                ge[birds.index(bird)].fitness -= 2
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        base.move()
        draw_window(birds, pipes, base, score)
        if score > 50:
            pickle.dump(nets[0], open('best.pickle', 'wb'))
            break


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    winner = pop.run(eval_genomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
