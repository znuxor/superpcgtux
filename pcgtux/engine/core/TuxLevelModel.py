from abc import ABC, abstractmethod
import numpy as np


class TuxLevelModel:

    EMPTY = 0
    MARIO_START = -2
    MARIO_EXIT = -3

    GROUND = 47
    PYRAMID_BLOCK = 48
    NORMAL_BRICK = 77
    COIN_BRICK = 104
    # TODO: change these to correct blocks
    LIFE_BRICK = 128  # not supported?
    SPECIAL_BRICK = 83
    SPECIAL_QUESTION_BLOCK = 102  # assumed fire flower
    COIN_QUESTION_BLOCK = 2947  # ??
    COIN_HIDDEN_BLOCK = 2946  # ??
    LIFE_HIDDEN_BLOCK = 112   # ??

    USED_BLOCK = 84
    COIN = 44
    PIPE = 57
    _PIPEUL = 57
    _PIPEUR = 58
    _PIPESL = 59
    _PIPESR = 60
    PIPE_FLOWER = 57  # unsupported
    BULLET_BILL = -12
    PLATFORM_BACKGROUND = -1
    PLATFORM = -1

    GOOMBA = -4
    GOOMBA_WINGED = -5
    RED_KOOPA = -6
    RED_KOOPA_WINGED = -7
    GREEN_KOOPA = -8
    GREEN_KOOPA_WINGED = -9
    SPIKY = -10
    SPIKY_WINGED = -11

    ENTITIES = {
            MARIO_START: 'spawnpoint\n    (name "main")',
            MARIO_EXIT: 'sequencetrigger\n    (sequence "endsequence")\n      (width 32)\n      (height 608)',
            GOOMBA: 'snowball\n(direction "left")',
            GOOMBA_WINGED: 'bouncingsnowball\n(direction "left")',
            RED_KOOPA: 'smartblock\n(direction "left")',
            RED_KOOPA_WINGED: 'smartblock\n(direction "left")',
            GREEN_KOOPA: 'mriceblock\n(direction "left")',
            GREEN_KOOPA_WINGED: 'mriceblock\n(direction "left")',
            SPIKY: 'spiky\n(direction "left")',
            SPIKY_WINGED: 'spiky\n(direction "left")',
            BULLET_BILL: 'kamikazesnowball\n(direction "left")',
            }

    def getEnemyTiles(self):
        return [BULLET_BILL, PIPE_FLOWER]

    def getBumpableTiles(self):
        return [self.NORMAL_BRICK, self.COIN_BRICK, self.LIFE_BRICK, self.SPECIAL_BRICK, self.SPECIAL_QUESTION_BLOCK, self.COIN_QUESTION_BLOCK]

    def getBlockTiles(self):
        return [self.GROUND, self.PYRAMID_BLOCK, self.USED_BLOCK, self.NORMAL_BRICK, self.COIN_BRICK, self.LIFE_BRICK, self.SPECIAL_BRICK, self.SPECIAL_QUESTION_BLOCK, self.COIN_QUESTION_BLOCK, self._PIPEUL, self._PIPEUR, self._PIPESL, self._PIPESR, self.PIPE_FLOWER, self.BULLET_BILL]

    def getBlockNonSpecialTiles(self):
        return [self.GROUND, self.PYRAMID_BLOCK, self.USED_BLOCK, self._PIPEUL, self._PIPEUR, self._PIPESL, self._PIPESR]

    def getNonBlockingTiles(self):
        return [self.COIN, self.COIN_HIDDEN_BLOCK, self.LIFE_HIDDEN_BLOCK, self.PLATFORM_BACKGROUND]

    def getCollectablesTiles(self):
        return [self.COIN, self.COIN_BRICK, self.LIFE_BRICK, self.SPECIAL_BRICK, self.SPECIAL_QUESTION_BLOCK, self.COIN_QUESTION_BLOCK, self.COIN_HIDDEN_BLOCK, self.LIFE_HIDDEN_BLOCK]

    def getWingedEnemyVersion(self, enemy, winged):
        if not winged:
            if enemy == self.GOOMBA_WINGED:
                return self.GOOMBA
            elif enemy == self.RED_KOOPA_WINGED:
                return self.RED_KOOPA
            elif enemy == self.GREEN_KOOPA_WINGED:
                return self.GREEN_KOOPA
            elif enemy == self.SPIKY_WINGED:
                return self.SPIKY
        else:
            if enemy == self.GOOMBA:
                return self.GOOMBA_WINGED
            elif enemy == self.RED_KOOPA:
                return self.RED_KOOPA_WINGED
            elif enemy == self.GREEN_KOOPA:
                return self.GREEN_KOOPA_WINGED
            elif enemy == self.SPIKY:
                return self.SPIKY_WINGED
        return enemy

    def getEnemyCharacters(self, wings=None):
        if wings is None:
            return [self.GOOMBA_WINGED, self.RED_KOOPA_WINGED, self.GREEN_KOOPA_WINGED, self.SPIKY_WINGED,
                    self.GOOMBA, self.RED_KOOPA, self.GREEN_KOOPA, self.SPIKY]
        elif wings is True:
            return [self.GOOMBA_WINGED, self.RED_KOOPA_WINGED, self.GREEN_KOOPA_WINGED, self.SPIKY_WINGED]
        else:
            return [self.GOOMBA, self.RED_KOOPA, self.GREEN_KOOPA, self.SPIKY]

    def __init__(self, levelWidth, levelHeight):
        self.map = np.zeros((levelHeight, levelWidth), dtype=int)

    def clone(self):
        new_level = TuxLevelMap(self.getWidth(), self.getHeight())
        for x in range(self.getWidth()):
            for y in range(self.getHeight()):
                new_level.map[y,x] = self.map[y,x]

    def getWidth(self):
        return self.map.shape[1]

    def getHeight(self):
        return self.map.shape[0]

    def getBlock(self, x, y):
        currentX = x
        currentY = y
        if x < 0:
            currentX = 0
        if y < 0:
            currentY = 0
        if x > self.getWidth()-1:
            x = self.getWidth()-1
        if y > self.getHeight()-1:
            y = self.getHeight()-1

        return self.map[y,x]

    def setBlock(self, x, y, value):
        if (x < 0 or y < 0 or x > self.getWidth()-1 or y > self.getHeight()-1):
            return
        else:
            self.map[y,x] = value

    def setRectangle(self, startX, startY, width, height, value):
        for x in range(width):
            for y in range(height):
                self.setBlock(startX + x, startY + y, value)

    def clearMap(self):
        self.setRectangle(0, 0, self.getWidth(), self.getHeight(), self.EMPTY)

    def getMap(self):
        self.arrange_map()

        tilemap = np.maximum.reduce([self.map, np.zeros((self.getHeight(), self.getWidth()), dtype=int)])  # items are negative values
        charmap = np.minimum.reduce([self.map, np.zeros((self.getHeight(), self.getWidth()), dtype=int)])  # items are negative values
        map_result = ""
        for line in tilemap:
            map_result += ' '.join(str(tile) for tile in line)
            map_result += '\n'

        entity_result = ""
        for y, line in enumerate(charmap):
            for x, char in enumerate(line):
                if char == -1:
                    print('Unsupported block at x, y = {}, {}'.format(x, y))
                if char in self.ENTITIES:
                    entity_result += '(' + self.ENTITIES[char] + '\n'
                    entity_result += '      (x ' + str(x*32) + ')\n'
                    entity_result += '      (y ' + str(y*32) + ')\n'
                    entity_result += '    )'
                    pass

        return map_result, entity_result

    def arrange_map(self):
        for (y, x), value in np.ndenumerate(self.map):
            # Pipe replacement with correct side
            if value in (self._PIPEUL, self._PIPEUR, self._PIPESL, self._PIPESR):
                top_is_free = (self.map[y-1,x] not in (self._PIPEUL, self._PIPEUR, self._PIPESL, self._PIPESR))
                right_is_free = (self.map[y,x+1] not in (self._PIPEUL, self._PIPEUR, self._PIPESL, self._PIPESR))
                if top_is_free and not right_is_free:
                    self.map[y,x] = self._PIPEUL
                elif top_is_free and right_is_free:
                    self.map[y,x] = self._PIPEUR
                elif not top_is_free and not right_is_free:
                    self.map[y,x] = self._PIPESL
                elif not top_is_free and right_is_free:
                    self.map[y,x] = self._PIPESR
