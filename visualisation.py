import gif
import matplotlib.pyplot as plt
import numpy as np

import simulation


@gif.frame
def plot_scene(scene, time):
    plt.figure(figsize=(8, 8))
    for person in scene.people:
        markertype = 'o'
        markercol = 'k'
        markersize = 10
        if person.dead:
            markertype = 'x'
            markersize = 20
        if person.infected:
            markercol = 'red'
            markersize = 20
        elif person.recovered:
            markercol = 'green'

        plt.scatter(person.pos[0], person.pos[1], marker=markertype, c=markercol, s=markersize)
    plt.axis('equal')
    plt.xlim(-30, 130)
    plt.ylim(-30, 130)


@gif.frame
def plot_scene2(scene, time):
    dead = []
    infected = []
    recovered = []
    not_infected = []
    plt.figure(figsize=(8, 8))
    for person in scene.people:
        if person.dead:
            dead.append(person.pos)
        elif person.infected:
            infected.append(person.pos)
        elif person.recovered:
            recovered.append(person.pos)
        else:
            not_infected.append(person.pos)

    if len(dead) > 0:
        dead = np.array(dead)
        plt.scatter(dead[:, 0], dead[:, 1], c='k', marker='x', s=20)
    if len(infected) > 0:
        infected = np.array(infected)
        plt.scatter(infected[:, 0], infected[:, 1], c='r', s=20)
    if len(recovered) > 0:
        recovered = np.array(recovered)
        plt.scatter(recovered[:, 0], recovered[:, 1], c='g', s=20)
    if len(not_infected) > 0:
        not_infected = np.array(not_infected)
        plt.scatter(not_infected[:, 0], not_infected[:, 1], c='k', s=10)

    ax = plt.gca()
    plt.text(0, 1.01, f'frame = {time}', transform=ax.transAxes)
    plt.axis('equal')
    plt.xlim(-30, 130)
    plt.ylim(-30, 130)


def create_gif(n_people, n_infected, total_time, scene=None, save_loc='gifs/'):
    if not scene:
        scene, frames = simulation.run(n_people, n_infected, total_time, create_gif=True)
    name = f'{n_people}people_{n_infected}infected_{total_time}time.gif'
    gif.save(frames, save_loc + name, duration=100)

