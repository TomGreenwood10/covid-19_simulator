"""
Module for running / handing simulation
"""

import numpy as np
import pandas as pd

import visualisation
from people import NormalPerson


class Scene:
    """
    Class for scene to contain people with coordinates.
    """
    def __init__(self, n_people, n_infected=0):
        self.people = []
        self.n_people = n_people
        self.n_infected = n_infected
        self.n_not_infected = n_people - n_infected
        self.n_recovered = 0
        self.n_dead = 0
        self.size = 100
        self.infection_distance = 0.5
        for i in range(self.n_not_infected):
            self.people.append(
                NormalPerson(
                    pos=np.random.rand(2) * self.size,
                    infected=False
                )
            )
        for i in range(self.n_infected):
            self.people.append(
                NormalPerson(
                    pos=np.random.rand(2) * self.size,
                    infected=True
                )
            )
        self.df = pd.DataFrame(
            [[len(self.people), self.n_not_infected, self.n_infected, self.n_recovered, self.n_dead]],
            columns=['n_total', 'n_not_infected', 'n_infected', 'n_recovered', 'n_dead']
        )

    def update(self, time):
        for person in self.people:
            person.move()
        for person in self.people:
            if person.infected:
                for other_person in self.people:
                    if other_person is not person:
                        if np.linalg.norm(person.pos - other_person.pos) < self.infection_distance:
                            other_person.infect(time)
            person.update(time)
        self.update_counts()

    def update_counts(self):
        n_infected = 0
        n_not_infected = 0
        n_recovered = 0
        n_dead = 0
        for person in self.people:
            if person.dead:
                n_dead += 1
                continue
            if person.infected:
                n_infected += 1
            elif person.recovered:
                n_recovered += 1
            else:
                n_not_infected += 1
        self.n_infected = n_infected
        self.n_not_infected = n_not_infected
        self.n_recovered = n_recovered
        self.n_dead = n_dead

    def log(self):
        self.df = pd.concat([
            self.df,
            pd.DataFrame(
                [[len(self.people), self.n_not_infected, self.n_infected, self.n_recovered, self.n_dead]],
                columns=['n_total', 'n_not_infected', 'n_infected', 'n_recovered', 'n_dead']
            )
        ])


def run(n_people, n_infected, total_time, create_gif=False, plot_func=2):
    if create_gif:
        frames = []

    scene = Scene(n_people=n_people, n_infected=n_infected)
    for time in range(total_time):
        scene.update(time)
        scene.log()
        if create_gif:
            if plot_func == 1:
                frames.append(visualisation.plot_scene(scene, time))
            if plot_func == 2:
                frames.append(visualisation.plot_scene2(scene, time))
    scene.df.reset_index(drop=True, inplace=True)
    if create_gif:
        return scene, frames
    else:
        return scene
