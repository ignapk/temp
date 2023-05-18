#!/usr/bin/env python3

import PyDMX
import argparse
from PatternEngine import PatternEngine

dmx_device = PyDMX.PyDMX('/dev/ttyUSB0')

def send_arr(dmx_values):
    dmx_values = dmx_values[::-1]
    dmx_values = [max(0, min(int(x), 255)) for x in dmx_values]
    for i in range(0, len(dmx_values), 3):
        print(f"{i+1}: {dmx_values[i+2]}")
        print(f"{i+2}: {dmx_values[i+1]}")
        print(f"{i+3}: {dmx_values[i+0]}")
        dmx_device.set_data(i+1, dmx_values[i+2])
        dmx_device.set_data(i+2, dmx_values[i+1])
        dmx_device.set_data(i+3, dmx_values[i+0])
    dmx_device.send()

parser = argparse.ArgumentParser(prog='swiatelka',
                                 description='Change lights in UMCS windows.',
                                 epilog='SKNI')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--filename', type=str, help='Bitmap file to display')
group.add_argument('-c', '--color', type=str, help='Solid color: black, white, light_gray, gray, dark_gray, red, pink, purple, light_blue, blue, yellow_green, green, yellow, orange, brown, pale_pink')
group.add_argument('-b', '--blackout', action='store_true', help='Turns off all the lights - changes color to black')
parser.add_argument('-p', '--preview', action='store_true', help='Preview pattern on terminal instead of displaying on the windows')
args = parser.parse_args()

colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'light_gray': (224, 224, 224),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'red': (255, 0, 0),
    'pink': (255, 96, 208),
    'purple': (160, 32, 255),
    'light_blue': (80, 208, 255),
    'blue': (0, 32, 255),
    'yellow-green': (96, 255, 128),
    'green': (0, 192, 0),
    'yellow': (255, 224, 32),
    'orange': (255, 160, 16),
    'brown': (160, 128, 96),
    'pale_pink': (255, 208, 160)
}

gen = PatternEngine()

if args.filename:
    if args.preview:
        gen.print_on_terminal(args.filename)
    else:
        send_arr(gen.arr_from_image(args.filename))
elif args.color:
    if args.preview:
        gen.print_color_on_terminal(colors[args.color])
    else:
        r, g, b = colors[args.color]
        arr = []
        for _ in range(129):
            arr.append(r)
            arr.append(g)
            arr.append(b)
        send_arr(arr)
elif args.blackout:
    dmx_device.sendzero()
else:
    parser.print_help()
