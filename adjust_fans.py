"""control comander pro and corsair hydro fan speeds"""

import argparse
import logging
import os

parser = argparse.ArgumentParser()
parser.add_argument("--speed", help="the percentage of max speed for fans")
parser.add_argument("--device", help="device name to adjust")
parser.add_argument("--all", dest="all_fans", action="store_true", default=False)
parser.add_argument("--fan", help="the fan identifier to set to percentage")
parser.add_argument("--status", help="show fan speed status", default=False, dest="status", action="store_true")
parser.add_argument("--gaming", help="85% rad 70% case", default=False, dest="gaming", action="store_true")
parser.add_argument("--normal", help="50% rad 40% case", default=False, dest="normal", action="store_true")
args = parser.parse_args()

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

aio_fans = [ "fan1", "fan2", "fan3" ]
commander_fans = [ "fan1", "fan2", "fan3", "fan4", "fan5", "fan6" ]

if args.gaming is True:
    for fan in aio_fans:
        os.system(f'liquidctl --match "Hydro" set {fan} speed 85')
    for fan in commander_fans:
        os.system(f'liquidctl --match "Commander" set {fan} speed 70')

if args.normal is True:
    for fan in aio_fans:
        os.system(f'liquidctl --match "Hydro" set {fan} speed 50')
    for fan in commander_fans:
        os.system(f'liquidctl --match "Commander" set {fan} speed 40')

if args.status is True:
    os.system(f'liquidctl status')

if args.device == "AIO" or args.all_fans is True:
    if args.all_fans is True:
        for fan in aio_fans:
            os.system(f'liquidctl --match "Hydro" set {fan} speed {args.speed}')
    elif args.fan is not None:
        os.system(f'liquidctl --match "Hydro" set fan{args.fan} speed {args.speed}')
    else:
        for fan in aio_fans:
            os.system(f'liquidctl --match "Hydro" set {fan} speed {args.speed}')

if args.device == "Commander" or args.all_fans is True:
    if args.all_fans is True:
        for fan in commander_fans:
            os.system(f'liquidctl --match "Commander" set {fan} speed {args.speed}')
    elif args.fan is not None:
        os.system(f'liquidctl --match "Commander" set fan{args.fan} speed {args.speed}')
    else:
        for fan in commander_fans:
            os.system(f'liquidctl --match "Commander" set {fan} speed {args.speed}')
