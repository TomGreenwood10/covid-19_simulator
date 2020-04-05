"""
Module containing people classes
"""

import numpy as np


class Country:

    def __init__(self):
        self.population = None
        self.cities = []
        self.n_cities = None
        self.city_scale = 200
        self.city_populations = np.random.exponential(self.city_scale, self.n_cities).astype(int)


class City:

    def __init__(self, pos):
        self.pos = pos
        self.residents = []
        self.physical_size = None


class Person:

    def __init__(self,
                 pos,
                 infected=False,
                 ill=False,
                 recovered=False,
                 death_probability=0.1):
        self.pos_initial = pos
        self.pos = pos
        self.infected = infected
        self.ill = ill
        self.recovered = recovered
        self.dead = False
        self.time_of_infection = 0 if infected else None
        self.death_probability = death_probability

    def infect(self, time):
        if not self.recovered and not self.dead:
            self.infected = True
            self.time_of_infection = time

    def update(self, time):
        if not self.dead:
            if self.infected:
                time_since_infected = time - self.time_of_infection
                if 5 * 24 <= time_since_infected < 12 * 24:
                    self.ill = True
                if time_since_infected == 12 * 24:
                    if np.random.rand() < self.death_probability:
                        self.dead = True
                        self.infected = False
                        self.ill = False
                    else:
                        self.recovered = True
                        self.infected = False


class NormalPerson(Person):

    def move(self):
        if not self.dead:
            if self.ill:
                self.pos += (np.random.rand(2) - 0.5)
            else:
                self.pos += (np.random.rand(2) - 0.5) * 2
                # self.pos -= 2 * vec_from_initial_pos

            # Introduce small tendency to move back to initial position to keep from drifting
            vec_from_initial_pos = self.pos - self.pos_initial
            self.pos -= 2 * vec_from_initial_pos


class SuperSpreader(Person):

    def move(self):
        if not self.dead:
            if self.ill:
                self.pos += (np.random.rand(2) - 0.5) * 2
            else:
                self.pos += (np.random.rand(2) - 0.5) * 10

            vec_from_initial_pos = self.pos - self.pos_initial
            self.pos -= 10 * vec_from_initial_pos
