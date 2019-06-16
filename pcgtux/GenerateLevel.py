#!/usr/bin/env python3

import os
import numpy as np
from pcgtux.engine.core.TuxLevelModel import TuxLevelModel

TEMPLATE_LOC = os.path.join(os.path.dirname(__file__), 'template.stl')
LEVEL_DIR = os.path.expanduser('~/.local/share/supertux2/levels/Infinitux')
GEN_FILENAME = 'generated.stl'


def main(generator_class, levels_dir=LEVEL_DIR, gen_filename=GEN_FILENAME):
    '''Drives the generator and makes the verifications'''
    generator = generator_class()


    tuxLevelModel = TuxLevelModel(150, 16)

    levelmap, items = generator.getGeneratedLevel(tuxLevelModel)

    print('Loading level template...')
    with open(TEMPLATE_LOC, 'r') as f:
        level_template = f.read()
        start, end = level_template.split('LEVELMAP')
        start, middle = start.split('COINS')


    print('Start saving level...')
    filepath = os.path.join(levels_dir, gen_filename)
    with open(filepath, 'w') as f:
        f.write(start)
        f.write(items)
        f.write(middle)
        f.write(levelmap)
        f.write(end)
    print('Done saving level.')
