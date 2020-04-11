# covid-19_simulator

## Overview
Simulator that moves people objects around and transfers infections.

__NB: This has not been written by someone with medical knowlege or any previous experience in infection simulations. The coefficients and mechanisms have not been arrived at via a sound scientific method__. I just wanted to write a framework during the current covid-19 crisis. If some of the code is useful then feel free to use.

## Structure
The 2D space that the simulations takes place in is dealt with by the `Country` object which contains `City` objects which contains `Person` objects.  All of these classes are found in the population module.

* __`Country` class__ -- contains cities and contry-wide population statistic attributes e.g. n_infected.  The initiation of coordinates for all cities and people occurs on instatiation of `Country()`.
* __`City` class__ -- contains people (as a list ion the `residents` attribute) and city-wide population statisic attributes.
* __`Person` class__ -- represents people and contains coordinates (`pos`) and infection status booleans; `infected`, `ill`, `recovered`.  Note: Only children of the `Person` class are used in the simulation which contain the `move` method which alters the objects coordinates.  Current children are `NormalPerson` and `SuperSpreader`.

`Country.update()` will call `update` on each City which will call `move()` on each person

The simulation module is used to run simulations and the visualisation module to create plots.

## How to use
1. Import the simulation module.
1. Run the simulation with the `simulation.run()` which will return the country in it's final state, a pandas dataframe with simulation infection information and if `return_gif_frames=True` then also frames (matplotlib plots) that can be saved as a gif with the gif package (`pip install gif`).
