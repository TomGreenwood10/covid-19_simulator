"""
Module for running / handing simulation
"""

import numpy as np
import pandas as pd
import gif

import visualisation
from population import Country


def run(n_infected,
        total_time,
        super_spreader_proportion=0.05,
        infection_distance=0.5,
        infection_probability=0.1,
        return_gif_frames=False,
        figsize=(8, 8)):

    df = pd.DataFrame(columns=['n_total', 'n_not_infected', 'n_infected', 'n_recovered', 'n_dead'])
    if return_gif_frames:
        frames = []

    # Initiate country and infections
    country = Country(super_spreader_proportion)
    i = 0
    while i < n_infected:
        infection_initiated = False
        while not infection_initiated:
            city = np.random.choice(country.cities)
            patient_zero = np.random.choice(city.residents)
            if not patient_zero.infected:
                patient_zero.infect(0)
                infection_initiated = True
        i += 1

    # Run simulation
    for time in range(total_time):
        country.update(time, infection_distance, infection_probability)
        df = log(
            df,
            country.population,
            country.n_not_infected,
            country.n_infected,
            country.n_recovered,
            country.n_dead
        )
        if return_gif_frames:
            frames.append(visualisation.plot(country, time, figsize))

    if return_gif_frames:
        return country, df, frames
    else:
        return country, df


def log(df, population, n_not_infected, n_infected, n_recovered, n_dead):
    df = pd.concat([
        df,
        pd.DataFrame(
            [[population, n_not_infected, n_infected, n_recovered, n_dead]],
            columns=['n_total', 'n_not_infected', 'n_infected', 'n_recovered', 'n_dead']
        )
    ])
    df.reset_index(drop=True, inplace=True)
    return df
