"""Defines the Controller interface and a few example controllers."""

import abc

import numpy as np

class Controller(object):
    """Abstract Controller class meant to be subclassed by all controllers."""

    def __init__(self, setpoint):
        """Initializes a new Controller instance.

        Args: The desired value towards which to drive the process.
        """
        self._setpoint = setpoint

    def _error(self, process_variable):
        """Returns the error between the process value and the setpoint."""
        return self._setpoint - process_variable

    @abc.abstractmethod
    def tick(self, process_variable, dt):
        """Controls the process at every instantaneous timestep (tick).
        
        Must be overridden by the subclass.

        Args:
            process_variable: The measured value of the process at the current
                insantenous timestep.
            dt: The elapsed time since this method was last called.

        Returns:
            The control signal in (-inf, inf). It is the responsiblity of the
            caller to convert the control signal to a range usable by the 
            process.
        """


class OnOffController(Controller):
    """An on-off (or bang-bang) hover controller.

    The simplest type of controller which returns a binary signal of full on
    (inf) when the error is positive or full off (-inf) when the error is 
    negative.
    """

    def tick(self, process_var, dt):
        del dt  # Unused.
        return np.inf * self._error(process_var)

class PIDController(Controller):
    """A proportional-integral-derivative (PID) controller.

    Uses a weighted combination of the error, error integral, and error
    derivative to control the process.

    Since we fundementally operate in a discrete regime, the integral is
    approximated by summing up the error term over each instantaneous timestep.
    The derivative is similarly approximated by taking the slope between the 
    errors at the current and previous instantaneous timesteps.
    """
    def __init__(self, setpoint, kp=1., ki=0., di=1.):
        """Initializes a new PIDController instance.
        
        Args:
            setpoint: See Controller base class.
            kp: The proportional weight constant.
            ki: The integral weight constant.
            di: The derivative weight constant.
        """
        super(PIDController, self).__init__(setpoint=setpoint)

        self._kp = kp
        self._ki = ki
        self._di = di

        self._error_previous = 0
        self._error_integral = 0

    def tick(self, process_var, dt):
        error = self._error(process_var)
        self._error_integral += error * dt
        derivative = (error - self._error_previous) / dt
        self._error_previous = error
        return (self._kp * error + 
                self._ki * self._error_integral + 
                self._di * derivative)

