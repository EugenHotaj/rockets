"""Extremley simple rocket hover simulation with a PID controller.

The rocket is treated as a point with the only forces acting on it being
gravity and upward thrust. The rocket is perfectly stable with no forces
acting on it in the horizontal directon.
"""

import graphics as g
import numpy as np
import tkinter as tk


TITLE = 'Rockets'
WIDTH = 800
HEIGHT = 600

GRAVITY = np.array((0, .1))
GROUND_Y = 500
TARGET_Y = 200

class Rocket(object):
    """A rocket equipped with a bottom thruster.
    
    The thruster is binary and can only opperate at either 100% capacity or
    0% capacity.
    """

    def __init__(self, window, pos):
        """Initializes a new Rocket instance.
        
        Args:
            window: The window to use when drawing the Rocket.
            pos: The initial position of the rocket.
        """
        self._window = window
        self._pos = np.array(pos)
        x, y = pos
        self._body = g.Polygon(
                g.Point(x - 10, y + 10), 
                g.Point(x +  10, y + 10), 
                g.Point(x, y - 10))
        self._body.draw(self._window)
        self._exhaust = g.Line(g.Point(x, y + 10), g.Point(x, y + 30))
        self._exhaust.setWidth(5)
        self._exhaust.setOutline("orange")

        self._vel = np.array((0., 0.))
        self._thrust_acc = np.array((0., -.13))

    def update(self):
        """Updates the Rocket's position by applying thrust and gravity."""
        self._exhaust.undraw()

        # Apply forces.
        acc = GRAVITY
        if self._pos[1]  > TARGET_Y:
            acc = acc + self._thrust_acc
            self._exhaust.draw(self._window)
        self._vel += acc
        self._pos += self._vel

        # Check ground collisions and update shape.
        dx, dy = self._vel.tolist()
        bottom = self._body.getPoints()[0].getY()
        if bottom + dy >= GROUND_Y:
            dy = GROUND_Y - bottom
        self._body.move(dx, dy)
        self._exhaust.move(dx, dy)

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
        
        self._rocket = Rocket(self._window, pos=(WIDTH/2, GROUND_Y))

    def run(self):
        while self._window.isOpen():
            self._rocket.update()
            g.update(60)

if __name__ == '__main__':
    sim = Simulation()
    sim.run()
