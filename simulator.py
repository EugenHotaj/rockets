"""Simple rocket simulator.

We make a few simplifying assumptions about the rocket:
    * The rocket is treated as point with only thrust and gravity acting on it.
    * The rocket is perfectly stable with no horizontal forces acting on it.
    * The rocket is indestructable.
    * The rocket has infinite fuel and therefore its mass does not change as 
      it burns fuel.
    * The rocket is able to apply any percentage of thrust instantenously and
      with perfect precision.
"""

import graphics as g
import numpy as np
import tkinter as tk

TITLE = 'Rockets'
WIDTH = 800
HEIGHT = 600

FPS = 60
DT = 1 / FPS  # This is a rough estimate of the actual FPS.

GRAVITY = np.array((0, 9.8))
GROUND_Y = 550
TARGET_Y = 150


class Rocket(object):
    """A rocket equipped with a bottom thruster."""

    def __init__(self, 
                 pos, 
                 height=21.2,
                 diameter=1.7,
                 mass=27670., 
                 max_thrust_force=410000.):
        """Initializes a new Rocket instance.

        The default arguments correspond to the SpaceX Falcon 1 rocket.
        
        Args:
            pos: The tuple of the initial (x, y) position of the rocket. The 
                position specifies the bottom center of the rocket. For example
                the rocket's tip will be at y + height. 
            height: The height of the rocket. Only affects the rocket's look
                and not the simulation.
            diameter: The diameter of the rocket. Only affects the rocket's 
                look and not the simulation.
            mass: The mass of the rocket in kilograms.
            max_thrust_force: The maximum thrust force at full burn in newtons.
        """
        self._pos = np.array(pos, dtype=np.float32)
        self._height = height
        self._diameter = diameter
        self._mass = mass 
        self._max_thrust_force = np.array((0., -max_thrust_force))
        self._thrust_percent = 0

        self._vel = np.array((0., 0.))

    def set_thrust(self, percent):
        """Sets the rocket's thrust."""
        assert percent in np.arange(0, 1.1, .1)
        self._thrust_percent = percent

    def update(self):
        """Resolve the forces acting on the rocket and update position."""
        if self._pos[1]  > TARGET_Y:
            self.set_thrust(1.)
        else:
            self.set_thrust(0)

        acc = GRAVITY
        if self._thrust_percent:
            thrust_force = self._max_thrust_force * self._thrust_percent
            thrust_acc = thrust_force / self._mass
            acc = acc + thrust_acc 
        self._vel += acc * DT
        self._pos += self._vel * DT

        # TODO(ehotaj): Temporary hack for ground collision. Long term, figure
        # out what the reacting force is and apply to rocket.
        if self._pos[1] >= GROUND_Y:
            # Do not stop the rocket if it is going up.
            self._pos[1] = GROUND_Y
            self._vel[1] = min(0, self._vel[1])
            
    def draw(self):
        """Returns a list of Graphics Objects necessary to draw the rocket."""
        drawables = []
        x, y = self._pos.tolist()
        radius = self._diameter / 2
        body = g.Polygon(g.Point(x - radius, y), g.Point(x + radius, y), 
                         g.Point(x, y - self._height)) 
        drawables.append(body)

        # TODO(ehotaj): Use a constants for these? 
        exhaust_height = 15 * self._thrust_percent
        if exhaust_height:
            exhaust = g.Line(g.Point(x, y),
                             g.Point(x, y + exhaust_height))
            exhaust.setWidth(1)
            exhaust.setOutline("orange")
            drawables.append(exhaust)
        return drawables


class Simulation(object):
    """Simulates the Rocket environment."""

    def __init__(self):
        self._window = g.GraphWin(TITLE, WIDTH, HEIGHT, autoflush=False)
        ground = g.Line(g.Point(0, GROUND_Y), g.Point(WIDTH, GROUND_Y))
        ground.draw(self._window)
        target = g.Line(g.Point(WIDTH/2 - 50, TARGET_Y), 
                        g.Point(WIDTH/2 + 50, TARGET_Y))
        target.setOutline("red")
        target.draw(self._window)
        
        self._rocket = Rocket(pos=(WIDTH/2, GROUND_Y))

    def run(self):
        """Runs the simulation until the user closes out."""
        drawables = []
        while self._window.isOpen():
            # Undraw the previous graphics objects.
            for drawable in drawables:
                drawable.undraw()
            drawables = []

            # Update and create next drawables.
            self._rocket.update()
            drawables.extend(self._rocket.draw())

            # Draw the current graphics objects.
            for drawable in drawables:
                drawable.draw(self._window)

            # Enforce FPS.
            g.update(FPS)

if __name__ == '__main__':
    sim = Simulation()
    sim.run()
