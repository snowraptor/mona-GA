#!/usr/bin/python2

import sys
import cairo
from numpy import *


class Gene():
    def __init__(self, numvertices, imgshape):
        self.imgshape = imgshape
        self.rgba = list(random.rand(4))
        self.vertices = []

        for vertex in range(numvertices):
            x = random.random_integers(0, imgshape[0])
            y = random.random_integers(0, imgshape[1])
            self.vertices.append((x, y))


    def mutate(self, sigma):
        if random.random() < 0.5:
            self.mutate_rgba(sigma)
        else:
            self.mutate_shape(sigma)


    def mutate_rgba(self, sigma):
        self.rgba += sigma * sigma * random.randn(4)

        self.rgba = map(lambda x: max(0, min(1, x)), self.rgba)


    def mutate_shape(self, sigma):
        for i,_ in enumerate(self.vertices):
            new_vertex0 = self.vertices[i][0] + sigma * random.randn() * self.imgshape[0]
            new_vertex0 = max(0, min(self.imgshape[0], new_vertex0))

            new_vertex1 = self.vertices[i][1] + sigma * random.randn() * self.imgshape[1]
            new_vertex1 = max(0, min(self.imgshape[1], new_vertex1))

            self.vertices[i] = (new_vertex0, new_vertex1)


def read_png(pngfile):
    with open(pngfile, 'r') as png:
        surface = cairo.ImageSurface.create_from_png(png)
    
    if surface.get_format() != cairo.FORMAT_RGB24:
        raise TypeError
    
    imgshape = [surface.get_width(), surface.get_height()]
    
    return array(map(ord,surface.get_data())), imgshape


def init_population(popsize, numshapes, numvertices, imgshape):
    population = []

    for i in range(popsize):
        dna = []

        for shape in range(numshapes):
            dna.append(Gene(numvertices, imgshape))

        population.append(dna)

    return population


def draw_shape(gene, ctx):
    ctx.set_source_rgba(*gene.rgba) # Solid color
    ctx.set_line_width(0)
    ctx.move_to(*gene.vertices[0])

    for vertex in gene.vertices[1:]:
        ctx.line_to(*vertex)

    ctx.fill()


def draw_DNA(dna):
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, dna[0].imgshape[0],  dna[0].imgshape[1])
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, dna[0].imgshape[0],  dna[0].imgshape[1])
    ctx.fill()
    for gene in dna:
        draw_shape(gene,ctx)
    return surface


def delta(test, reference):
    return sqrt(sum((test - reference) ** 2))

def pop_fitness(population, reference, max_fitness):
    fitness = {}
    for index,individual in enumerate(population):
        fit = delta(map(ord,draw_DNA(individual).get_data()), reference)
        fit = 1 - (fit / max_fitness)
        fitness[index] = fit
    return fitness


def crossover(parent1, parent2):
    cut = random.randint(0, len(parent1))
    child = parent1[0:cut]
    child.extend(parent2[cut:])
    return child



def mate(population,fitness, mutaterate, sigma):
    roulette = sorted(fitness, key=fitness.get)
    sum_fitness = sum(fitness.values())
    newpop = [population[roulette[-1]]]

    while len(newpop) < len(population):
        parents = random.choice(roulette,
                                 size = 2,
                                 replace = False,
                                 p = map(lambda x: x/sum_fitness, fitness.values()))

        child = crossover(population[parents[0]], population[parents[1]])

        for i,_ in enumerate(child):
            if random.random() < mutaterate:
                child[i].mutate(sigma)

        if random.random() < mutaterate:
            swap = random.randint(0, len(child), size = 2)
            child[swap[0]], child[swap[1]] = child[swap[1]], child[swap[0]]

        newpop.append(child)

    return newpop


def output(pop, gen):
    individual = 0
    for i in pop:
        outfile = 'gen_{:05d}_ind_{:02d}.png'.format(gen, individual)
        image = draw_DNA(i)
        with open(outfile, 'w') as out:
            image.write_to_png(out)
        individual += 1



#surface.write_to_png ("from_DNA.png") # Output to PNG
def main():
    popsize = 20
    numshapes = 100
    numvertices = 3
    mutaterate = 0.1
    sigma = 0.01
    reference, imgshape = read_png("test.png")

    population = init_population(popsize, numshapes, numvertices, imgshape)

    max_fitness = delta(reference, zeros(len(reference)))
    generation = 0
    output(population, generation)
    while(True):
        fitness = pop_fitness(population, reference, max_fitness)
        population = mate(population, fitness, mutaterate, sigma)
        generation += 1

        if generation % 10 == 0:
            print("Generation: {}\tMax Fitness: {}".format(generation, max(zip(*fitness)[0])))
            sys.stdout.flush()
            if generation % 100 == 0:
                output(population, generation)


main()
