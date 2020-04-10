"""
Module containing people classes
"""

import numpy as np


class Country:

    def __init__(self,
                 super_spreader_proportion=0.05,
                 n_cities=10,
                 city_scale=100):
        self.n_cities = n_cities
        self.city_scale = city_scale
        self.city_populations = np.random.exponential(self.city_scale, self.n_cities).astype(int)
        self.population = self.city_populations.sum()
        self.n_infected = None
        self.n_ill = None
        self.n_not_infected = None
        self.n_recovered = None
        self.n_dead = None
        self.cities = []

        for pop in self.city_populations:
            city = City(np.random.exponential(1, 2) * np.random.choice([-1, 1], 2) * 40)
            city.population = pop
            city.physical_size = np.cbrt(pop)

            person_count = 0
            while person_count < pop * super_spreader_proportion:
                person = SuperSpreader(
                    np.random.exponential(1, 2) * np.random.choice([-1, 1], 2) * city.physical_size + city.pos)
                city.residents.append(person)
                person_count += 1
            while person_count < pop:
                person = NormalPerson(
                    np.random.exponential(1, 2) * np.random.choice([-1, 1], 2) * city.physical_size + city.pos)
                city.residents.append(person)
                person_count += 1

            self.cities.append(city)

    def update(self, time, infection_distance, infection_probability=1):
        for city in self.cities:
            city.move()
        for city in self.cities:
            city.update(time, infection_distance, infection_probability)
        self.update_counts()

    def update_counts(self):
        self.n_infected = 0
        self.n_ill = 0
        self.n_recovered = 0
        self.n_dead = 0
        for city in self.cities:
            city.update_counts()
            self.n_infected += city.n_infected
            self.n_ill += city.n_ill
            self.n_recovered += city.n_recovered
            self.n_dead += city.n_dead
        self.n_not_infected = self.population - self.n_infected


class City:

    def __init__(self, pos):
        self.pos = pos
        self.residents = []
        self.physical_size = None
        self.population = None
        self.n_infected = None
        self.n_ill = None
        self.n_not_infected = None
        self.n_recovered = None
        self.n_dead = None

    def move(self):
        for person in self.residents:
            person.move()

    def update(self, time, infection_distance, infection_probability=1):
        for person in self.residents:
            if person.infected:
                for other_person in self.residents:
                    if other_person is not person:
                        if np.linalg.norm(person.pos - other_person.pos) < infection_distance:
                            if np.random.rand() < infection_probability:
                                other_person.infect(time)
            person.update_health_status(time)
        self.update_counts()

    def update_counts(self):
        self.n_infected = 0
        self.n_ill = 0
        self.n_recovered = 0
        self.n_dead = 0
        for person in self.residents:
            if person.infected:
                self.n_infected += 1
            if person.ill:
                self.n_ill += 1
            if person.recovered:
                self.n_recovered += 1
            if person.dead:
                self.n_dead += 1
        self.n_not_infected = self.population - self.n_infected


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

    def update_health_status(self, time):
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
    # Move scalar and adjustment / fudge for proximity.  Could look at altering population layout instead
    def move(self, move_scalar=0.1):
        if not self.dead:
            if self.ill:
                self.pos += (np.random.rand(2) - 0.5) * move_scalar
            else:
                self.pos += (np.random.rand(2) - 0.5) * move_scalar * 2
                # self.pos -= 2 * vec_from_initial_pos

            # Introduce small tendency to move back to initial position to keep from drifting
            vec_from_initial_pos = self.pos - self.pos_initial
            self.pos -= 2 * vec_from_initial_pos


class SuperSpreader(Person):

    def move(self, move_scalar=0.1):
        if not self.dead:
            if self.ill:
                self.pos += (np.random.rand(2) - 0.5) * move_scalar * 2
            else:
                self.pos += (np.random.rand(2) - 0.5)* move_scalar * 10

            vec_from_initial_pos = self.pos - self.pos_initial
            self.pos -= 10 * vec_from_initial_pos
