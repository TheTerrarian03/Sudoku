from turtle import update
import pygame, pygame.draw, random


pygame.font.init()

class Block:
    def __init__(self, pixelsPerBlock, coord, value=0, correct=False):
        # thickBorder can be: tl t  tr l  n  r  bl b  br a  lr tb
        #        which means: ┌  ─  ┐  │  x  │  └  ─  ┘  [] || =
        self.ppb = pixelsPerBlock
        self.pos = coord
        self.value = value
        self.correct = correct
        self.valueWrong = False
        self.valuePossible = False
        self.fNormal = pygame.font.SysFont("Courier New", self.ppb-10)
        self.fBold = pygame.font.SysFont("Courier New", self.ppb-10, bold=True)
        self.textOffSet = [0, 0]
        self.tb = ""
        self.starred = False
    
    def setVal(self, newVal):
        self.value = newVal
    
    def getVal(self):
        return self.value
    
    def setCorrect(self, isCorrect):
        self.correct = isCorrect
    
    def getCorrect(self):
        return self.correct
    
    def setPossible(self, isPossible):
        self.valuePossible = isPossible
    
    def getPossible(self):
        return self.valuePossible
    
    def setWrong(self, isWrong):
        self.valueWrong = isWrong
    
    def getWrong(self):
        return self.valueWrong
    
    def setBorder(self, newBorder):
        self.tb = newBorder
    
    def switchStarred(self):
        if self.starred:
            self.starred = False
        else:
            self.starred = True

    def draw(self, dispSurface):
        # some variable setting
        left = self.pos[0]*self.ppb
        right = (self.pos[0]*self.ppb) + self.ppb
        top = self.pos[1]*self.ppb
        bottom = (self.pos[1]*self.ppb) + self.ppb
        # color setting
        if self.valueWrong:
            textColor = (175, 0, 0)
        else:
            textColor = (0, 0, 0)
        
        if self.starred:
            bgColor = (255, 215, 0)
        elif self.valueWrong:
            bgColor = (225, 150, 150)
        elif self.correct:
            bgColor = (125, 225, 125)
        elif self.valuePossible:
            bgColor = (175, 225, 175)
        else:
            bgColor= None
        # drawing background
        if bgColor:
            pygame.draw.rect(dispSurface, bgColor, (left, top, self.ppb, self.ppb))
        # drawing border lines
        pygame.draw.line(dispSurface, (0, 0, 0), (left, top), (right, top), width=3 if ("t" in self.tb or self.tb == "a") else 1)  # TOP
        pygame.draw.line(dispSurface, (0, 0, 0), (left, top), (left, bottom), width=3 if ("l" in self.tb or self.tb == "a") else 1)  # LEFT
        pygame.draw.line(dispSurface, (0, 0, 0), (left, bottom), (right, bottom), width=3 if ("b" in self.tb or self.tb == "a") else 1)  # BOTTOM
        pygame.draw.line(dispSurface, (0, 0, 0), (right, bottom), (right, top), width=3 if ("r" in self.tb or self.tb == "a") else 1)  # RIGHT
        # drawing text for value
        if self.value != 0:
            if self.correct:
                text1 = self.fBold.render(str(self.value), False, textColor)
            else:
                text1 = self.fNormal.render(str(self.value), False, textColor)
            dispSurface.blit(text1, (left+self.textOffSet[0], top+self.textOffSet[1]))
        # text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
        # screen.blit(text1, (i * dif + 15, j * dif + 15))

class Board:
    def __init__(self, dimensions, defaultValues, pixelsPerSquare):
        self.squares = dimensions[:-1]
        self.maxNum = dimensions[4]
        self.pps = pixelsPerSquare
        self.blocks = []
        self.res = [(self.squares[0] * self.squares[2] * self.pps), (self.squares[1] * self.squares[3] * self.pps)]
        self.disp = pygame.display.set_mode((self.res[0], self.res[1]))
        self.selected = [True, 0, 0]

        for y in range(self.squares[2] * self.squares[3]):
            for x in range(self.squares[0] * self.squares[2]):
                self.blocks.append(Block(self.pps, (x, y)))
        
        for i in range(len(self.blocks)):
            # text off set setting
            self.blocks[i].textOffSet = [12, 4]
            # setting values and correctness
            self.blocks[i].setVal(defaultValues[i])
            if defaultValues[i] != 0:
                self.blocks[i].setCorrect(True)
            # setting borders
            # print(f"Block Index: {i}, Block Coord: {self.blocks[i].pos}, Block Value: {self.blocks[i].value}, X mod: {self.blocks[i].pos[0] % dimensions[2]}, Y mod: {self.blocks[i].pos[1] % dimensions[3]}")
            xMod = (self.blocks[i].pos[0] % dimensions[2]) + 1
            yMod = (self.blocks[i].pos[1] % dimensions[3]) + 1
            if (xMod == 1) and (yMod == 1):  # tl
                self.blocks[i].setBorder("tl")
            elif (xMod == dimensions[0]) and (yMod == 1):  # tr
                self.blocks[i].setBorder("tr")
            elif (xMod == 1) and (yMod == dimensions[1]):  # bl
                self.blocks[i].setBorder("bl")
            elif (xMod == dimensions[0]) and (yMod == dimensions[1]):  # br
                self.blocks[i].setBorder("br")
            elif (1 < xMod < dimensions[0]) and (yMod == 1):  # t
                self.blocks[i].setBorder("t")
            elif (1 < xMod < dimensions[0]) and (yMod == dimensions[1]):  # b
                self.blocks[i].setBorder("b")
            elif (xMod == 1) and (1 < yMod < dimensions[1]):  # l
                self.blocks[i].setBorder("l")
            elif (xMod == dimensions[0]) and (1 < yMod < dimensions[1]):  # r
                self.blocks[i].setBorder("r")
    
    def convToIndex(self, x, y):
        for i in range(len(self.blocks)):
            if self.blocks[i].pos == (x, y):
                return i
        return 0
    
    def convToCoord(self, index):
        try:
            return self.blocks[index].pos
        except IndexError:
            return 0

    def setBlockNum(self, index, newValue):
        self.blocks[index].setVal(newValue)

    def trySetNum(self, newVal):
        if not (self.blocks[self.convToIndex(self.selected[1], self.selected[2])].correct):
            self.blocks[self.convToIndex(self.selected[1], self.selected[2])].setVal(newVal)
            if newVal == 0:
                self.blocks[self.convToIndex(self.selected[1], self.selected[2])].starred = False
    
    def setStarred(self):
        self.blocks[self.convToIndex(self.selected[1], self.selected[2])].switchStarred()

    def AdjustAllOffsets(self, changeX=0, changeY=0):
        for block in self.blocks:
            block.textOffSet = [block.textOffSet[0]+changeX, block.textOffSet[1]+changeY]
    
    def adjustSelected(self, xChange, yChange):
        self.selected[1] += xChange
        if self.selected[1] < 0:
            self.selected[1] = 0
        elif self.selected[1] > (self.squares[2]*self.squares[0]):
            self.selected[1] = (self.squares[2]*self.squares[0])
        
        self.selected[2] += yChange
        if self.selected[2] < 0:
            self.selected[2] = 0
        elif self.selected[2] > (self.squares[3]*self.squares[1]):
            self.selected[2] = (self.squares[3]*self.squares[1])

    def clearBoardToDefaults(self):
        for block in self.blocks:
            if not block.getCorrect():
                block.setVal(0)
                block.starred = False

    def checkForErrors(self):
        # a variable to hold how many errors, will be returned at end
        totalWrong = ""
        # first, set all blocks to be not wrong
        for block in self.blocks:
            block.setWrong(False)
        # check each inner square for doubles
        for outerX in range(self.squares[2]):
            for outerY in range(self.squares[3]):
                # print(outerX, outerY)
                currentNums = ""  # variable to hold a simple string of all the numbers in that square
                wrongNums = ""
                for innerY in range(self.squares[0]):
                    for innerX in range(self.squares[1]):
                        currentNums += str(self.blocks[self.convToIndex(innerX+((outerX)*self.squares[0]), innerY+((outerY)*self.squares[1]))].getVal())
                # print(currentNums)
                for i in range(1, self.maxNum+1):
                    if currentNums.count(str(i)) > 1:
                        # print(f"OVER! {i}")
                        wrongNums += str(i)
                for innerY in range(self.squares[0]):
                    for innerX in range(self.squares[1]):
                        if str(self.blocks[self.convToIndex(innerX+((outerX)*self.squares[0]), innerY+((outerY)*self.squares[1]))].getVal()) in wrongNums:
                            self.blocks[self.convToIndex(innerX+((outerX)*self.squares[0]), innerY+((outerY)*self.squares[1]))].setWrong(True)
        
        totalWrong += wrongNums

        # check for each row
        for row in range(self.squares[3]*self.squares[1]):
            currentNums = ""
            wrongNums = ""
            for col in range(self.squares[2]*self.squares[0]):
                currentNums += str(self.blocks[self.convToIndex(col, row)].getVal())
            for i in range(1, self.maxNum+1):
                if currentNums.count(str(i)) > 1:
                    # print(f"OVER! {i}")
                    wrongNums += str(i)
            for col in range(self.squares[2]*self.squares[0]):
                if str(self.blocks[self.convToIndex(col, row)].getVal()) in wrongNums:
                    self.blocks[self.convToIndex(col, row)].setWrong(True)

        totalWrong += wrongNums

        # check for each column
        for col in range(self.squares[2]*self.squares[0]):
            currentNums = ""
            wrongNums = ""
            for row in range(self.squares[3]*self.squares[1]):
                currentNums += str(self.blocks[self.convToIndex(col, row)].getVal())
            for i in range(1, self.maxNum+1):
                if currentNums.count(str(i)) > 1:
                    # print(f"OVER! {i}")
                    wrongNums += str(i)
            for row in range(self.squares[3]*self.squares[1]):
                if str(self.blocks[self.convToIndex(col, row)].getVal()) in wrongNums:
                    self.blocks[self.convToIndex(col, row)].setWrong(True)
        
        totalWrong += wrongNums
        return [len(totalWrong), totalWrong]
    
    def checkForCompletedParts(self):
        # first, make all squares' valuePossible to False
        for block in self.blocks:
            block.setPossible(False)
        # check for each inner square for one of each number, from 1 to self.maxNum
        for outerX in range(self.squares[2]):
            for outerY in range(self.squares[3]):
                currentNums = ""  # variable to hold a simple string of all the numbers in that square
                hasZeros = False
                for innerY in range(self.squares[0]):
                    for innerX in range(self.squares[1]):
                        currentNums += str(self.blocks[self.convToIndex(innerX+((outerX)*self.squares[0]), innerY+((outerY)*self.squares[1]))].getVal())
                for i in range(1, self.maxNum+1):
                    if currentNums.count(str(i)) == 0:
                        hasZeros = True
                if not hasZeros:
                    for innerY in range(self.squares[0]):
                        for innerX in range(self.squares[1]):
                            self.blocks[self.convToIndex(innerX+((outerX)*self.squares[0]), innerY+((outerY)*self.squares[1]))].setPossible(True)
        
        # check for each row
        for row in range(self.squares[3]*self.squares[1]):
            currentNums = ""
            hasZeros = False
            for col in range(self.squares[2]*self.squares[0]):
                currentNums += str(self.blocks[self.convToIndex(col, row)].getVal())
            for i in range(1, self.maxNum+1):
                if currentNums.count(str(i)) == 0:
                    hasZeros = True
            if not hasZeros:
                for col in range(self.squares[2]*self.squares[0]):
                    self.blocks[self.convToIndex(col, row)].setPossible(True)
        
        # check for each column
        for col in range(self.squares[2]*self.squares[0]):
            currentNums = ""
            hasZeros = False
            for row in range(self.squares[3]*self.squares[1]):
                currentNums += str(self.blocks[self.convToIndex(col, row)].getVal())
            for i in range(1, self.maxNum+1):
                if currentNums.count(str(i)) == 0:
                    hasZeros = True
            if not hasZeros:
                for row in range(self.squares[3]*self.squares[1]):
                    self.blocks[self.convToIndex(col, row)].setPossible(True)

    def checkForAllCompleted(self):
        anyWrong = False
        anyZero = False
        for block in self.blocks:
            if block.getWrong():
                anyWrong = True
            if block.getVal() == 0:
                anyZero = True
        
        top = 0
        bottom = self.res[1]
        left = 0
        right = self.res[0]
        if not anyWrong and not anyZero:
            pygame.draw.line(self.disp, (0, 200, 0), (left, top), (right, top), width=5)  # TOP
            pygame.draw.line(self.disp, (0, 200, 0), (left, top), (left, bottom), width=5)  # LEFT
            pygame.draw.line(self.disp, (0, 200, 0), (left, bottom), (right, bottom), width=5)  # BOTTOM
            pygame.draw.line(self.disp, (0, 200, 0), (right, bottom), (right, top), width=5)  # RIGHT
            return True
        return False

    def solve(self, updateFPS, method="RANDOM"):
        def checkBreak():
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True  
        
        clock = pygame.time.Clock()

        if method == "RANDOM":
            solved = False
            while not solved:
                for block in self.blocks:
                    if not block.getCorrect():
                        block.setVal(random.randrange(1, self.maxNum+1))
                    
                    if checkBreak():
                        break
                
                completed = self.draw()
                if completed:
                    solved = True
                else:
                    print(self.checkForErrors())
                
                pygame.display.update()
                clock.tick(updateFPS)

    def draw(self):
        # background
        pygame.draw.rect(self.disp, (225, 225, 225), (0, 0, self.res[0], self.res[1]))
        # each block
        for block in self.blocks:
            block.draw(self.disp)
        # selected box border
        if self.selected[0]:
            # variables
            left = self.selected[1]*self.pps
            right = (self.selected[1]*self.pps) + self.pps
            top = self.selected[2]*self.pps
            bottom = (self.selected[2]*self.pps) + self.pps
            # lines
            pygame.draw.line(self.disp, (50, 50, 255), (left, top), (right, top), width=3)  # TOP
            pygame.draw.line(self.disp, (50, 50, 255), (left, top), (left, bottom), width=3)  # LEFT
            pygame.draw.line(self.disp, (50, 50, 255), (left, bottom), (right, bottom), width=3)  # BOTTOM
            pygame.draw.line(self.disp, (50, 50, 255), (right, bottom), (right, top), width=3)  # RIGHT
            # completed outline
            self.checkForErrors()
            self.checkForCompletedParts()
            return self.checkForAllCompleted()
