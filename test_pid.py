import random
import time

from PID import PID


SET_POINT = 225
INTERVAL = 0.25

START_INPUT = 150
INPUT = START_INPUT
NUM_INPUTS = 100


if __name__ == '__main__':
    pid = PID(
        set_point=SET_POINT,
        interval=INTERVAL,
        p=1.0,
        i=1.0,
        d=1.0
    )

    for i in xrange(1, NUM_INPUTS):
        # v = pid.calculate(random.randint(90, 110))
        v = pid.calculate(INPUT)
        print v

        if INPUT != SET_POINT:
            INPUT += 1

        time.sleep(INTERVAL)
