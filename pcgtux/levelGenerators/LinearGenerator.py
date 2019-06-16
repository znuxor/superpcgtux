import random
import pcgtux.engine.core.TuxLevelGenerator as TuxLevelGenerator

GROUND_PADDING = 5
GROUND_LENGTH = 8
GAP_LENGTH = 6
GAP_PROB = 0.1
PIPE_PROB = 0.75
GROUND_PIPE_LENGTH = 10
PIPE_HEIGHT = 6
COLLECTIBLE_PROB = 0.75
GROUND_COLLECTIBLE_LENGTH = 6
GROUND_ENEMY_LENGTH = 2


class LinearGenerator(TuxLevelGenerator.TuxLevelGenerator):

    def placePipe(self, model, x, y, height):
        pipeType = model.PIPE
        if self.rnd.random() < 0.2:
            pipeType = model.PIPE_FLOWER

        model.setRectangle(x, y-height+1, 2, height, pipeType)

    def placeInterestingArrangement(self, model, x, y, width):
        for i in range(width//2):
            itype = self.rnd.choice(model.getBumpableTiles())
            model.setBlock(x+i, y, itype)
            model.setBlock(x+width-1-i, y, itype)

        if width%2 == 1 and self.rnd.random() < 0.25:
            itype = self.rnd.choice(model.getBumpableTiles())
            model.setBlock(x+width//2, y, itype)

        if y > 4 and self.rnd.random() < 0.25:
            self.placeInterestingArrangement(model, x + width//4, y - 3 - self.rnd.randrange(0, 3), width // 2)

    def placeEnemy(self, model, x1, x2, y):
        winged = self.rnd.random() < 0.1
        enemyType = self.rnd.choice(model.getEnemyCharacters(False))
        enemyType = model.getWingedEnemyVersion(enemyType, winged)
        xStart = x1 + self.rnd.randrange(0, x2 - x1)
        length = 1 + self.rnd.randrange(0, 3)
        if length > x2 - x1 - 1:
            length = x2 - x1 - 1

            for i in range(length):
                if model.getBlock(xStart+i, y) == model.EMPTY:
                        model.setBlock(xStart+i, y, enemyType)

    def getGeneratedLevel(self, model):
        self.rnd = random.Random(3)
        model.clearMap()

        groundArea = []
        groundArea.append(0)
        groundLength = GROUND_LENGTH / 2 + self.rnd.randrange(0, GROUND_LENGTH / 2)
        gapLength = 0

        # add ground
        for x in range(model.getWidth()):
            if groundLength > 0 or gapLength == 0 or x < GROUND_PADDING or x > model.getWidth() - 1 - GROUND_PADDING:
                model.setBlock(x, model.getHeight()-1, model.GROUND)
                model.setBlock(x, model.getHeight()-2, model.GROUND)
                groundLength -= 1
                if groundLength <= 0 and self.rnd.random() < GAP_PROB:
                    gapLength = GAP_LENGTH / 2 + self.rnd.randrange(0, GAP_LENGTH/2)
                if len(groundArea) % 2 == 0:
                    groundArea.append(x)
            else:
                gapLength -= 1
                if gapLength <= 0:
                    groundLength = GROUND_LENGTH / 2 + self.rnd.randrange(0, GROUND_LENGTH/2)

                    if len(groundArea) %2 == 1:
                        groundArea.append(x)

        groundArea.append(model.getWidth() - 1)

        # add pipes
        newAreas = []
        for i in range(len(groundArea)//2):
            groundLength = groundArea[2*i+1] - groundArea[2*i]
            if groundLength > GROUND_PIPE_LENGTH and self.rnd.random() < PIPE_PROB:
                x = groundArea[2*i] + self.rnd.randrange(0, groundLength // 4) + 3
                self.placePipe(model, x, model.getHeight() - 3, self.rnd.randrange(PIPE_HEIGHT * 2 // 3) + PIPE_HEIGHT // 3)
                newAreas.append(groundArea[2*i])
                newAreas.append(x-1)
                newAreas.append(x+2)
                newAreas.append(groundArea[2*i + 1])

        # add interesting patterns
        groundArea = []
        for i in range(len(newAreas)//2):
            groundLength = newAreas[2*i+1] - newAreas[2*i]
            groundArea.append(newAreas[2*i])
            groundArea.append(model.getHeight()-3)
            groundArea.append(newAreas[2*i+1])
            groundArea.append(model.getHeight()-3)
            if groundLength > GROUND_COLLECTIBLE_LENGTH and self.rnd.random() < COLLECTIBLE_PROB:
                x = newAreas[2*i] + self.rnd.randrange(0, groundLength//3) + 1
                y = model.getHeight() - 5 - self.rnd.randrange(0, 3) + 1
                length = 1 + self.rnd.randrange(groundLength//3)
                self.placeInterestingArrangement(model, x, y, length)
                groundArea.append(x + 1)
                groundArea.append(y - 1)
                groundArea.append(x + length - 1)
                groundArea.append(y - 1)

        # add enemies
        for i in range(len(groundArea)//4):
            groundLength = groundArea[4*i+2] - groundArea[4*i]
            if groundLength > GROUND_ENEMY_LENGTH:
                self.placeEnemy(model, groundArea[4*i], groundArea[4*i+2], groundArea[4*i+1])

        model.setBlock(3, model.getHeight() - 3, model.MARIO_START)
        model.setBlock(model.getWidth() - 2, model.getHeight() - 3, model.PYRAMID_BLOCK)
        model.setBlock(model.getWidth() - 2, model.getHeight() - 4, model.MARIO_EXIT)
        return model.getMap()

    def getGeneratorName(self):
        return 'LinearGenerator'
