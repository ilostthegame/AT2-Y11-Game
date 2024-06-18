import pygame
from pygame.locals import *
import time
## DONT TOUCH MODULES

# run = True
# pygame.init()

# screen = pygame.display.set_mode((500,500))
# font = pygame.font.Font(None, 32)
# x=pygame.Surface((100, 100))

# text = font.render('eeee', True, (0,0,0))
# x = text.get_rect()
# x.topleft = (10,100)

# while run == True:
#     # Event handler for QUIT
#     screen.fill((255, 255, 255))
#     for event in pygame.event.get(): 
#         if event.type == QUIT:
#             run = False

#     screen.blit(text, x)
#     pygame.display.flip()
    
                    
# pygame.quit()

### GAME RUNNING STUFF

class test2:
    attr = None
    def __init__(self):
        self.attr = 'e'
    
    def printx(self):
        print(self.attr)

class test:
    # Attributes
    __one = None
    __two = None

    # Constructor
    def __init__(self, one, two):
        self.setTwo(two)
        print(self.getTwo().attr)
        self.getTwo().printx()
        

    # Getters
    def getOne(self):
        return self.__one
    def getTwo(self):
        return self.__two

    # Setters
    def setOne(self, one):
        self.__one = one
        print(self.__two)
    def setTwo(self, two):
        self.__two = two

e = test2()
x = test('hi', e)
t = test2()
print(t.attr)
