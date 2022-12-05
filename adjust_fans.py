"""control comander pro and corsair hydro fan speeds"""

import argparse
import datetime
import logging
import os
import sqlite3
import time

from sqlite3 import Error

parser = argparse.ArgumentParser()
parser.add_argument("--speed", help="the percentage of max speed for fans")
parser.add_argument("--device", help="device name to adjust")
parser.add_argument("--all", dest="all_fans", action="store_true", default=False)
parser.add_argument("--fan", help="the fan identifier to set to percentage")
parser.add_argument("--status", help="show fan speed status", default=False, dest="status", action="store_true")
parser.add_argument("--gaming", help="85% rad 70% case", default=False, dest="gaming", action="store_true")
parser.add_argument("--quiet", help="60% rad 40% case", default=False, dest="quiet", action="store_true")
parser.add_argument("--dynamic", help="dynamically set fan speeds based off AIO temp", default=False, dest="dynamic_speed", action="store_true")
parser.add_argument("--monitor", help="watch AIO temp", default=False, dest="monitor", action="store_true")
parser.add_argument("--interval", help="interval in which to refresh monitor command")
args = parser.parse_args()

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

aio_fans = [ "fan1", "fan2", "fan3" ]
commander_fans = [ "fan1", "fan2", "fan3", "fan4", "fan5", "fan6" ]

def set_fan_speed(device: str, fan: str, speed: int):
    os.system(f'liquidctl --match "{device}" set {fan} speed {speed}')

def set_aio_fan_speed(fan: str, speed: int):
    set_fan_speed("Hydro", fan, speed)

def set_commander_fan_speed(fan: str, speed:int):
    set_fan_speed("Commander", fan, speed)

def get_status():
    os.system('liquidctl status')

if args.monitor is True:
    try:
        interval = args.interval
        if args.interval is None:
            interval = 10

        while args.monitor:
            temp = os.popen('liquidctl status | grep Liquid | awk \'{print $4 $5}\'').read().strip()
            ct = datetime.datetime.now().isoformat(timespec='seconds')
            print(f'{ct} - {temp}')
            time.sleep(int(interval))
    except KeyboardInterrupt:
        print('\nmonitor canceled')

if args.gaming is True:
    for fan in aio_fans:
        set_aio_fan_speed(fan, 85)
    for fan in commander_fans:
        set_commander_fan_speed(fan, 70)
    time.sleep(10)
    get_status()

if args.quiet is True:
    for fan in aio_fans:
        set_aio_fan_speed(fan, 60)
    for fan in commander_fans:
        set_commander_fan_speed(fan, 40)
    time.sleep(10)
    get_status()

if args.status is True:
    os.system(f'liquidctl status')

if args.device == "AIO" or args.all_fans is True:
    if args.fan is not None:
        set_aio_fan_speed(args.fan, args.speed)
    else:
        for fan in aio_fans:
            set_aio_fan_speed(fan, args.speed)
    time.sleep(10)
    get_status()

if args.device == "Commander" or args.all_fans is True:
    if args.fan is not None:
        set_commander_fan_speed(args.fan, args.speed)
    else:
        for fan in commander_fans:
            set_commander_fan_speed(fan, args.speed)
    time.sleep(10)
    get_status()

