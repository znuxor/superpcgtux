#!/usr/bin/env python3

import os
import pcgtux.GenerateLevel
from pcgtux.levelGenerators.LinearGenerator import LinearGenerator
from pcgtux.levelGenerators.RandomGenerator import RandomGenerator

if __name__ == '__main__':
    pcgtux.GenerateLevel.main(RandomGenerator)
