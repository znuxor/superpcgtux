import random
import pcgtux.engine.core.TuxLevelGenerator as TuxLevelGenerator

GROUND_Y_LOCATION = 13
GROUND_PROB = 0.4
OBSTACLES_LOCATION = 10
OBSTACLES_PROB = 0.1
COLLECTIBLE_LOCATION = 3
COLLECTIBLE_PROB = 0.05
ENMEY_PROB = 0.1
FLOOR_PADDING = 3


class RandomGenerator(TuxLevelGenerator.TuxLevelGenerator):

    def getGeneratedLevel(self, model):
        self.random = random.Random(3)
        model.clearMap()

        for x in range(model.getWidth()):
            for y in range(model.getHeight()):
                model.setBlock(x, y, model.EMPTY)
                if y > GROUND_Y_LOCATION:
                    if self.random.random() < GROUND_PROB:
                        model.setBlock(x, y, model.GROUND)
                elif y > OBSTACLES_LOCATION:
                    if self.random.random() < OBSTACLES_PROB:
                        model.setBlock(x, y, model.PYRAMID_BLOCK)
                    elif self.random.random() < ENMEY_PROB:
                        model.setBlock(x, y, self.random.choice(model.getEnemyCharacters()))
                elif y > COLLECTIBLE_LOCATION:
                    if self.random.random() < COLLECTIBLE_PROB:
                        model.setBlock(x, y, self.random.choice(model.getCollectablesTiles()))

        model.setRectangle(0, 14, FLOOR_PADDING, 2, model.GROUND)
        model.setRectangle(model.getWidth()-1-FLOOR_PADDING, 14, FLOOR_PADDING, 2, model.GROUND)
        model.setBlock(FLOOR_PADDING//2, 13, model.MARIO_START)
        model.setBlock(model.getWidth() - 1 - FLOOR_PADDING//2, 13, model.MARIO_EXIT)
        return model.getMap()

    def getGeneratorName(self):
        return 'RandomLevelGenerator'
