import colorsys
import math
import threading
import time

import blinkt


def turn_off_leds():
    blinkt.set_all(0, 0, 0)
    blinkt.show()


def rainbow(stop):
    # adapted from
    # https://github.com/pimoroni/blinkt/blob/master/examples/rainbow.py
    spacing = 360.0 / 16.0

    blinkt.set_clear_on_exit()
    blinkt.set_brightness(0.1)

    while True:
        if stop():
            turn_off_leds()
            break
        hue = int(time.time() * 100) % 360
        for x in range(blinkt.NUM_PIXELS):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()
        time.sleep(0.001)


def larson(stop):
    # adapted from
    # https://github.com/pimoroni/blinkt/blob/master/examples/larson.py
    REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]

    start_time = time.time()
    blinkt.set_brightness(0.3)

    while True:
        if stop():
            turn_off_leds()
            break
        delta = (time.time() - start_time) * 8
        offset = int(round(((math.sin(delta) + 1) / 2) * (blinkt.NUM_PIXELS - 1)))

        for i in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(i, REDS[offset + i], 0, 0)

        blinkt.show()

        time.sleep(0.001)


def blink_message(success=True):
    if success:
        color = (0, 255, 0)  # green
    else:
        color = (255, 0, 0)  # red

    blinkt.set_brightness(0.1)

    for _ in range(3):
        blinkt.set_all(*color)
        blinkt.show()
        time.sleep(0.2)

        turn_off_leds()
        time.sleep(0.1)

#
# def run_for_delay(count: int):
#     stop_thread = False
#     thread1 = threading.Thread(target=rainbow, args=(lambda: stop_thread,))
#     thread1.start()
#
#     time.sleep(count)
#
#     stop_thread = True
#     thread1.join()
#
#     blink_message(success=True)
