# BOIDS

This Python script simulates a flock of birds and predators using the Pyxel game engine. It allows you to interact with the simulation by moving a target with your mouse. The birds and predators exhibit flocking behavior, seeking cohesion, alignment, and separation, while predators also actively pursue and attack nearby birds.

## Functionalities:

### Bird Behavior:

- **Alignment:** Birds align their direction with nearby birds within a certain radius.
- **Cohesion:** Birds move towards the center of mass of nearby birds within a certain radius.
- **Separation:** Birds avoid crowding by steering away from nearby birds within a certain radius.
- **Attraction:** Birds are attracted to a target point (controlled by the mouse cursor) within a specified attraction radius.
- **Color Change:** Birds may change color based on the colors of nearby birds.

### Predator Behavior:

- **Attack:** Predators actively pursue and attack nearby birds within a certain radius.
- **Separation:** Predators avoid crowding by steering away from other predators within a certain radius.
- **Bigger:** Predators grow in size and health by consuming birds.

### Simulation:

- **Initialization:** The simulation initializes with a specified number of birds and predators randomly placed within the screen boundaries.
- **Updating:** The simulation updates the positions and behaviors of birds and predators based on their interactions and environment.
- **Drawing:** The simulation draws birds, predators, and the target point on the screen using Pyxel's graphics capabilities.
- **Population and Predator Count Display:** The current population of birds and the count of predators are displayed on the screen.

## Quadtree Optimization:

To optimize neighbor search and collision detection, the simulation integrates a quadtree data structure. A quadtree divides space into regions, reducing the number of objects to check for interactions.

### Quadtree Functionalities:

- **Subdivision:** Divides a region into smaller quadrants when it reaches its capacity.
- **Insertion:** Inserts objects into the quadtree, distributing them among the appropriate quadrants.
- **Query Range:** Retrieves objects within a specified range, efficiently reducing the number of objects to check.

## How to Use:

1. **Installation:**
    - Ensure you have Python installed on your system.
    - Install the Pyxel library using `pip install pyxel`.

2. **Execution:**
    - Run the `app.py` script using Python (`python retro.py`).
    - Use your mouse cursor to control the target point.

3. **Interact:**
    - Observe the flocking behavior of birds and the hunting behavior of predators.
    - Experiment with different parameters such as the number of birds, predator count, and attraction radius.

## To-Do:

- Implement genetic algorithms for evolving behaviors.
- Enhance the simulation with additional game mechanics such as resource management and environmental hazards.

## Acknowledgements:

This project was inspired by the concepts of flocking behavior and predator-prey dynamics in nature. Special thanks to the Pyxel developers for providing a simple yet powerful game engine for Python.
