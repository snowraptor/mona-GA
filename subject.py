import cairo
from numpy import *
from itertools import *
from gene import *


class Subject:
  def __init__(self, num_genes, num_vertices, width, height):
    self.width = width
    self.height = height
    self.num_genes = num_genes
    self.dna = []

    for _ in xrange(num_genes):
      gene = Gene(num_vertices, width, height)
      
      self.dna.append(gene)


  def mutate(self, delta):
    for i,_ in enumerate(self.dna):
      self.dna[i].mutate_rgba(delta) if random.random() < 0.5 else self.dna[i].mutate_shape(delta)


  def fitness(self, goal):
    length = 4.0 * self.width * self.height
    
    individual = map(ord, self.draw().get_data())

    diff = list(imap(lambda x,y: abs(x-y)/255.0, individual, goal))

    return 1 - sum(diff) / length


  def draw(self):
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.width, self.height)
    context = cairo.Context(surface)
    context.set_source_rgb(1, 1, 1)
    context.rectangle(0, 0, self.width, self.height)
    context.fill()
    
    for gene in self.dna:
      context.set_source_rgba(*gene.rgba)
      context.set_line_width(0)
      context.move_to(*gene.vertices[0])

      for vertex in gene.vertices[1:]:
        context.line_to(*vertex)

      context.fill()

    return surface


  def save(self, output):
    self.draw().write_to_png(output)
    
    
class Child(Subject):
  def __init__(self, parent1, parent2, mutate_rate, delta):
    self.width = parent1.width
    self.height = parent1.height
    self.num_genes = parent1.num_genes
    
    cut = self.num_genes / 2

    self.dna = parent1.dna[:cut] + parent2.dna[cut:]

    if random.random() < mutate_rate:
      self.mutate(delta)