from numpy import *


class Gene:
  def __init__(self, num_vertices, width, height):
    self.width = width
    self.height = height

    self.rgba = list(random.rand(4))

    self.num_vertices = num_vertices
    self.vertices = []
    
    for _ in xrange(num_vertices):
      x = random.random_integers(0, self.width)
      y = random.random_integers(0, self.height)
      self.vertices.append((x, y))


  def mutate_rgba(self, delta):
    elem = random.randint(0,4)
    
    new_value = self.rgba[elem] + delta * delta * random.randn()
    new_value = max(0, min(1, new_value))

    self.rgba[elem] = new_value

    
  def mutate_shape(self, delta):
    for i in xrange(self.num_vertices):
      x = self.vertices[i][0] + delta * random.randn() * self.width
      x = max(0, min(self.width, x))

      y = self.vertices[i][1] + delta * random.randn() * self.height
      y = max(0, min(self.height, y))

      self.vertices[i] = (x,y)
