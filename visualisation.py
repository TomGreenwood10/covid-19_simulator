import gif
import matplotlib.pyplot as plt
import numpy as np

import simulation


@gif.frame
def plot(country, time, figsize=(8, 8), xlim=(-230, 80), ylim=(-100, 210)):
    dead = []
    infected = []
    ill = []
    recovered = []
    not_infected = []
    for city in country.cities:
        for person in city.residents:
            if person.dead:
                dead.append(person.pos)
            elif person.infected:
                if person.ill:
                    ill.append(person.pos)
                else:
                    infected.append(person.pos)
            elif person.recovered:
                recovered.append(person.pos)
            else:
                not_infected.append(person.pos)

    plt.figure(figsize=figsize)
    if len(not_infected) > 0:
        not_infected = np.array(not_infected)
        plt.scatter(not_infected[:, 0], not_infected[:, 1], c='k', s=10, alpha=0.1)
    if len(recovered) > 0:
        recovered = np.array(recovered)
        plt.scatter(recovered[:, 0], recovered[:, 1], c='g', s=20)
    if len(dead) > 0:
        dead = np.array(dead)
        plt.scatter(dead[:, 0], dead[:, 1], c='k', marker='x', s=20)
    if len(infected) > 0:
        infected = np.array(infected)
        plt.scatter(infected[:, 0], infected[:, 1], c='r', s=20)
    if len(ill) > 0:
        ill = np.array(ill)
        plt.scatter(ill[:, 0], ill[:, 1], c='purple', s=20)



    ax = plt.gca()
    plt.text(0, 1.01, f'frame = {time}', transform=ax.transAxes)
    plt.axis('equal')
    plt.xlim(xlim)
    plt.ylim(ylim)


def create_gif(n_people, n_infected, total_time, scene=None, save_loc='gifs/'):
    if not scene:
        scene, frames = simulation.run(n_people, n_infected, total_time, create_gif=True)
    name = f'{n_people}people_{n_infected}infected_{total_time}time.gif'
    gif.save(frames, save_loc + name, duration=100)


def trends(df, country=None):
    if country:
        print(
            f'Country population = {country.population:,}   infected = {country.n_infected:,}  '
            f'died = {country.n_dead:,}')

    plt.figure(figsize=(15, 5))
    plt.plot(df.n_infected, c='r', label='infected')
    plt.plot(df.n_recovered, c='g', label='recovered')
    plt.plot(df.n_dead, c='k', label='dead')
    plt.legend()
    plt.grid()
    plt.title('Infections in Country Population')
    plt.xlabel('time step');
    plt.ylabel('people')


def compare_infections(df_list, attribute, labels, title):
    plt.figure(figsize=(15, 5))
    for df, label in zip(df_list, labels):
        plt.plot(df[attribute], label=label)
    plt.legend()
    plt.grid()
    plt.title(f'{attribute} for {title}')
    plt.xlabel('time step');
    plt.ylabel('people')
