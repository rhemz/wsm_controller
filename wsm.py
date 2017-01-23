import pibrella
import signal
import sys
import time

import config
import state


def fans_on(outputs):
    # pibrella.light.green.on()
    pibrella.light.green.pulse(0.5)
    pibrella.light.red.off()

    for output in outputs:
        output.on()


def fans_off(outputs):
    pibrella.light.green.off()
    # pibrella.light.red.on()
    pibrella.light.red.pulse(0.5)

    for output in outputs:
        output.off()


def button_pressed(button):
    if state.FANS_ON:
        fans_off(config.FAN_OUTPUTS)
        state.FANS_ON = False
    else:
        fans_on(config.FAN_OUTPUTS)
        state.FANS_ON = True


def main():
    print 'Starting WSM Monitor...'

    # pibrella.light.red.on()
    # pibrella.light.red.pulse(0.2)
    # pibrella.light.yellow.pulse(0.3)
    # pibrella.light.green.pulse(0.4)

    pibrella.button.pressed(button_pressed)

    try:
        signal.pause()
    except KeyboardInterrupt:
        print '\nShutting down...'

if __name__ == '__main__':
    main()
