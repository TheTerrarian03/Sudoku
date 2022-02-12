import classes as cs
import pygame


sheet2x2Data = [2, 0,
              0, 4]
sheet2x2Dims = [2, 2, 1, 1, 4]
sheet4x4Data = [1, 0, 2, 0,
                0, 0, 0, 0,
                3, 0, 4, 0,
                0, 0, 0, 3]
sheet4x4Dims = [2, 2, 2, 2, 4]
sheet6x6Data = [1, 6, 5, 0, 0, 4,
              0, 2, 5, 0, 1, 0,
              3, 0, 4, 0, 0, 0,
              0, 0, 0, 0, 0, 1,
              0, 0, 0, 0, 0, 0,
              6, 0, 0, 0, 0, 3]
sheet6x6Dims = [3, 2, 2, 3, 6]  # innerWid, innerHi, outerWid, outerHi, maxNum
sheet9x9Data = [3, 0, 0, 8, 0, 1, 0, 0, 2,
                2, 0, 1, 0, 3, 0, 6, 0, 4,
                0, 0, 0, 2, 0, 4, 0, 0, 0,
                8, 0, 9, 0, 0, 0, 1, 0, 6,
                0, 6, 0, 0, 0, 0, 0, 5, 0,
                7, 0, 2, 0, 0, 0, 4, 0, 9,
                0, 0, 0, 5, 0, 9, 0, 0, 0,
                9, 0, 4, 0, 8, 0, 7, 0, 5,
                6, 0, 0, 1, 0, 7, 0, 0, 3]
sheet9x9Dims = [3, 3, 3, 3, 9]

board = cs.Board(sheet4x4Dims, sheet4x4Data, 50)
running = True
clearCountDown = 0

clock = pygame.time.Clock()
fps = 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ### arrows
            # horizontal
            if event.key == pygame.K_LEFT:
                board.adjustSelected(-1, 0)
            elif event.key == pygame.K_RIGHT:
                board.adjustSelected(1, 0)
            # vertical
            if event.key == pygame.K_UP:
                board.adjustSelected(0, -1)
            elif event.key == pygame.K_DOWN:
                board.adjustSelected(0, 1)
            
            ### entering values
            if event.key == pygame.K_0 or event.key == pygame.K_KP0 or event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                board.trySetNum(0)
            elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                board.trySetNum(1)
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                board.trySetNum(2)
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                board.trySetNum(3)
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                board.trySetNum(4)
            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                board.trySetNum(5)
            elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                board.trySetNum(6)
            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                board.trySetNum(7)
            elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                board.trySetNum(8)
            elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                board.trySetNum(9)
            
            ### other special keystrokes and functions
            if event.key == pygame.K_s:
                board.setStarred()
            if event.key == pygame.K_c:
                if clearCountDown > 0:
                    board.clearBoardToDefaults()
                    clearCountDown = 0
                else:
                    clearCountDown = 30
            if event.key == pygame.K_SPACE:
                board.solve(100000, method="RANDOM")

    board.draw()
    pygame.display.update()
    if clearCountDown > 0:
        clearCountDown -= 1
    clock.tick(fps)
