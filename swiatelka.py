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
args = parser.parse_args()

gen = PatternEngine()

if args.filename:
    send_arr(gen.arr_from_image(args.filename))
else:
    parser.print_help()
