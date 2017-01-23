"""
PID Notes:
    https://en.wikipedia.org/wiki/PID_controller#Control_loop_basics
    https://en.wikipedia.org/wiki/Integral_windup
"""

import numbers
import time


class PID(object):

    def __init__(self, set_point, p=1.0, i=1.0, d=1.0, interval=1.0, windup_correction=10.0):
        """
        :param set_point: Desired output of the system
        :type set_point: float
        :param p: Proportional gain
        :type p: float
        :param i: Integral gain
        :type i: float
        :param d: Derivative gain
        :type d: float
        :param interval: sampling interval
        :type interval: float (seconds)
        :param windup_correction: Corrective value to apply in case of integral windup (see link above)
        :type windup_correction: float
        """
        self._p = None
        self._i = None
        self._d = None
        self._set_point = None
        self._windup_correction = None
        self._interval = None

        self.set_point = set_point
        self.P = p
        self.I = i
        self.D = d
        self.interval = interval
        self.windup_correction = windup_correction

        self.current_time = time.time()
        self.last_calculation_time = self.current_time
        self.last_error = 0.0
        self.p_term = 0.0
        self.i_term = 0.0
        self.d_term = 0.0

        self.output = None

    def calculate(self, input_value):
        self.current_time = time.time()

        error = self._set_point - input_value
        time_diff = self.current_time - self.last_calculation_time
        error_diff = error - self.last_error

        # check to see if any new calculations should be performed
        if self.output is not None and time_diff < self._interval:
            return self.output

        self.p_term = self.P * error
        self.i_term = error * time_diff
        self.d_term = error_diff / time_diff if time_diff > 0 else 0.0

        # integral windup protection
        if self.i_term > self.windup_correction:
            self.i_term = self.windup_correction
        elif self.i_term < self.windup_correction * -1:
            self.i_term = self.windup_correction * -1

        self.last_calculation_time = self.current_time
        self.last_error = error

        self.output = self.p_term + (self.I * self.i_term) + (self.D * self.d_term)

        return self.output

    def _valid_gain(self, value):
        return (isinstance(value, int) or isinstance(value, float)) and value >= 0.0

    @property
    def set_point(self):
        return self._set_point

    @set_point.setter
    def set_point(self, value):
        assert isinstance(value, numbers.Number)
        self._set_point = value

    @property
    def P(self):
        return self._p

    @P.setter
    def P(self, value):
        assert self._valid_gain(value)
        self._p = value

    @property
    def I(self):
        return self._i

    @I.setter
    def I(self, value):
        assert self._valid_gain(value)
        self._i = value

    @property
    def D(self):
        return self._d

    @D.setter
    def D(self, value):
        assert self._valid_gain(value)
        self._d = value

    @property
    def windup_correction(self):
        return self._windup_correction

    @windup_correction.setter
    def windup_correction(self, value):
        assert isinstance(value, numbers.Number) and value > 0.0
        self._windup_correction = value

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        assert isinstance(value, numbers.Number) and value > 0.0
        self._interval = value

