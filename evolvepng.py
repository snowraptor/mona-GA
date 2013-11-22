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
            self.vertices.append([x, y])
    def mutate(self, sigma):
        if random.random() < 0.5:
            self.mutate_rgba(sigma)
        else:
            self.mutate_shape(sigma)
    def mutate_rgba(self, sigma):
        self.rgba = sigma * random.randn(4) + rgba
        highlights = self.rgba > 1.0
        self.rgba[highlights] = 1.0
        shadows = self.rgba < 0.0
        self.rgba[shadows] = 0.0
    def mutate_shape(self, sigma):
        pass
        #TODO

def read_png(pngfile):
    with open(pngfile, 'r') as png:
        surface = cairo.ImageSurface.create_from_png(png)
    if surface.get_format() != cairo.FORMAT_RGB24:
        raise TypeError
    imgshape = [surface.get_width(), surface.get_height()]
    return array(map(ord,surface.get_data())), imgshape

def init_population(popsize, numshapes, numvertices, imgshape):
    species = []
    for i in range(popsize):
        dna = []
        for shape in range(numshapes):
            dna.append(Gene(numvertices, imgshape))
        species.append(dna)
    return species

def draw_shape(gene, ctx):
    ctx.set_source_rgba(*gene.rgba) # Solid color
    ctx.set_line_width (0)
    ctx.move_to(*gene.vertices[0])
    for vertex in gene.vertices[1:]:
        ctx.line_to(*vertex)
    ctx.fill()

def draw_DNA(dna):
    surface = cairo.ImageSurface (cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context (surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.retangle(0, 0, width, height)
    ctx.fill()
    for gene in dna:
        draw_shape(gene,ctx)
    return surface


def delta(test, reference):
    return average(test - reference)**2

def pop_fitness(population, reference):
    i = 0
    fitness = []
    for indivudual in population:
        fit = delta(map(ord,draw_DNA(individual)), reference)
        fitness.append([delta, i])
        i += 1


def rouletewheel(fitness):

    pass
    #TODO



#surface.write_to_png ("from_DNA.png") # Output to PNG
def main():
    popsize = 20
    numshapes = 1000
    numvertices=3
    reference, imgshape = read_png("test.png")

    population = init_population(popsize, numshapes, numvertices, imgshape)

    sys.exit()
    generation = 0
    while(True):
        fitness = pop_fitness(population, reference)
        keep = rouletewheel(fitness)
        population = mate(keep)
        generation += 1




main()
