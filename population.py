import cairo
from subject import *


class Population:
  num_genes = 50
  num_vertices = 6

  mutate_rate = 0.3
  delta = 0.25
  
  
  def __init__(self, original_image, pop_size):
    self.pop_size = pop_size
    self.num_parents = int(round(pop_size * 0.25 ))
  
    image = cairo.ImageSurface.create_from_png(original_image)
    self.width = image.get_width()
    self.height = image.get_height()

    self.goal = map(ord, image.get_data())

    self.population = []

    for _ in xrange(self.pop_size):
      subject = Subject(self.num_genes, self.num_vertices, self.width, self.height)
      
      self.population.append(subject)

    self.pop_fitness()


  def pop_fitness(self):
    self.fitness_last_generation = {}

    for i in xrange(self.pop_size):
      self.fitness_last_generation[i] = self.population[i].fitness(self.goal)


  def next_generation(self):
    candidates = sorted(self.fitness_last_generation, key=self.fitness_last_generation.get, reverse=True)[:self.num_parents]

    self.best_subject_last_generation = self.population[candidates[0]]
    self.best_fitness_last_generation = self.fitness_last_generation[candidates[0]]
    
    new_population = []

    for _ in xrange(self.pop_size):
      p1 = random.randint(0, self.num_parents)
      p2 = random.randint(0, self.num_parents)

      parent1 = self.population[p1]
      parent2 = self.population[p2]

      child = Child(parent1, parent2, self.mutate_rate, self.delta)

      new_population.append(child)

    self.population = new_population

    self.pop_fitness()


  def evolve(self):
    self.best_subject_ever = self.population[0]
    self.best_fitness_ever = self.fitness_last_generation[0]

    generation = 0
    
    while self.best_fitness_ever < 1:
      self.next_generation()

      if self.best_fitness_last_generation > self.best_fitness_ever:
        self.best_subject_ever = self.best_subject_last_generation
        self.best_fitness_ever = self.best_fitness_last_generation

        self.best_subject_ever.save("generation%05d.png" % generation)

        print "best fitness ever: %.4f (generation %d)" % (self.best_fitness_ever, generation)

      print "`-> current best fitness: %.4f (generation %d)" % (self.best_fitness_last_generation, generation)

      generation += 1
