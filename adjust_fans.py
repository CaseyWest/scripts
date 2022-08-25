"""control comander pro and corsair hydro fan speeds"""

import argparse
import logging
import os

parser = argparse.ArgumentParser()
parser.add_argument("--speed", help="the percentage of max speed for fans")
parser.add_argument("--device", help="device name to adjust")
parser.add_argument("--all", dest="all_fans", action="store_true", default=False)
parser.add_argument("--fan", help="the fan identifier to set to percentage")
args = parser.parse_args()

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

aio_fans = [ "fan1", "fan2", "fan3" ]
commander_fans = [ "fan1", "fan2", "fan3", "fan4", "fan5", "fan6" ]

if args.device == "AIO" or args.all_fans is True:
    if args.all_fans is True:
        for fan in aio_fans:
            os.system(f'sudo liquidctl --match "Hydro" set {fan} speed {args.speed}')
    elif args.fan is not None:
        os.system(f'sudo liquidctl --match "Hydro" set fan{args.fan} speed {args.speed}')

if args.device == "Commander" or args.all_fans is True:
    if args.all_fans is True:
        for fan in commander_fans:
            os.system(f'sudo liquidctl --match "Commander" set {fan} speed {args.speed}')
    elif args.fan is not None:
        os.system(f'sudo liquidctl --match "Commander" set fan{args.fan} speed {args.speed}')
