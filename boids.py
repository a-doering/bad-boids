"""
An implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

import random
from numpy import array


class Boid:
    """A single Boid, which may belong to a flock of Boids (its owner)."""

    def __init__(self, x, y, xv, yv, owner):
        self.position = array([x, y])
        self.velocity = array([xv, yv])
        self.owner = owner

    def interaction(self, other):
        delta_v = array([0.0, 0.0])
        separation = other.position - self.position
        separation_sq = separation.dot(separation)

        # Fly towards the middle
        delta_v += separation * self.owner.flock_attraction

        # Fly away from nearby boids
        if separation_sq < self.owner.avoidance_radius ** 2:
            delta_v -= separation

        # Try to match speed with nearby boids
        if separation_sq < self.owner.formation_flying_radius ** 2:
            delta_v += (
                other.velocity - self.velocity
            ) * self.owner.speed_matching_strength

        return delta_v


class Boids:
    """A flock of Boids governed by a set of interaction parameters."""

    def __init__(
        self,
        flock_attraction,
        avoidance_radius,
        formation_flying_radius,
        speed_matching_strength,
    ):
        self.flock_attraction = flock_attraction
        self.avoidance_radius = avoidance_radius
        self.formation_flying_radius = formation_flying_radius
        self.speed_matching_strength = speed_matching_strength

    def initialise_random(
        self,
        count,
        x_range=(-450, 50.0),
        y_range=(300.0, 600.0),
        xv_range=(0, 10.0),
        yv_range=(-20.0, 20.0),
    ):
        self.boids = [
            Boid(
                random.uniform(*x_range),
                random.uniform(*y_range),
                random.uniform(*xv_range),
                random.uniform(*yv_range),
                self,
            )
            for i in range(count)
        ]

    def initialise_from_data(self, data):
        self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]

    def update(self):
        for me in self.boids:
            delta_v = array([0.0, 0.0])
            for him in self.boids:
                delta_v += me.interaction(him)
            # Accelerate as stated
            me.velocity += delta_v
            # Move according to velocities
            me.position += me.velocity
