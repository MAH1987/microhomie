import asyn
import colorsys

from uasyncio import sleep_ms


# Color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)


def convert_str_to_rgb(rgb_str):
    try:
        r, g, b = rgb_str.split(b",")
        return (int(r.strip()), int(g.strip()), int(b.strip()))
    except (ValueError, TypeError):
        return None


def all_off(np):
    np.fill(BLACK)
    np.write()


def all_on(np, color=WHITE):
    np.fill(color)
    np.write()


def set_leds(np, start, end, color=BLACK, autowrite=True):
    r = range(start, end)
    for i in r:
        np[i] = color
    if autowrite:
        np.write()

def set_led(np, led, color=BLACK, autowrite=True):
    np[led] = color
    if autowrite:
        np.write()


@asyn.cancellable
async def flash(np, on=RED, off=BLACK, iterations=8, delay=250, end=BLACK):
    fill = np.fill
    write = np.write
    iterations = iterations * 2
    r = range(iterations)
    for i in r:
        if i % 2 == 0:
            fill(on)
            write()
        else:
            fill(off)
            write()

        await sleep_ms(delay)

    fill(end)
    write()


@asyn.cancellable
async def center_to_bottom(np, color=(8, 8, 14)):
    center = int(len(np) / 2)
    np[center] = color
    np.write()
    await sleep_ms(100)
    np[center] = BLACK
    for i in range(center):
        # left
        np[center - i] = color
        # right
        np[center + i] = color
        np.write()
        sleep_ms(100)

@asyn.cancellable
async def fill_solid_rainbow(np):
    leds = int(len(np))
    deltahue = 1 / leds
    r = range(leds)
    for l in r:
        rgb = list(colorsys.hsv_to_rgb(deltahue * l, 1, 1))
        color = (
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        set_led(np, l, color)
