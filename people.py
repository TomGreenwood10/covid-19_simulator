"""
Module containing people classes
"""

import numpy as np


class Person:

    def __init__(self, pos, infected=False, ill=False, recovered=False, death_probability=0.1):
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
                self.pos += (np.random.rand(2) * 0.2)
            else:
                self.pos += (np.random.rand(2) - 0.5) * 2
