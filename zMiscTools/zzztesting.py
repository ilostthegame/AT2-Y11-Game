import pygame
from pygame.locals import *
import time
## DONT TOUCH MODULES

run = True
pygame.init()
screen = pygame.display.set_mode((500,500))
tile = pygame.Surface((64, 64))
tile.fill('red')

while run == True:
    # Event handler for QUIT
    for event in pygame.event.get(): 
        if event.type == QUIT:
            run = False
        elif event.type == KEYDOWN:
            print(event.unicode)

    screen.fill((255, 255, 255))
    screen.blit(tile, (0, 0, 64, 64))
    screen.blit(tile, (55, 100, 64, 64))
    pygame.display.flip()
                    
pygame.quit()

### GAME RUNNING STUFF

# class test2:
#     attr = None
#     def __init__(self):
#         self.attr = 'e'
    
#     def printx(self):
#         print(self.attr)



# ####

# # run = True
# # pygame.init()


# # screen = pygame.display.set_mode((500,500))
# # font = pygame.font.Font(None, 32)
# # x=pygame.Surface((100, 100))

# # text = font.render('eeee', True, (0,0,0))
# # x = text.get_rect()
# # x.topleft = (10,100)

# # while run == True:
# #     # Event handler for QUIT
# #     screen.fill((255, 255, 255))
# #     for event in pygame.event.get(): 
# #         if event.type == QUIT:
# #             run = False

# #     screen.blit(text, x)
# #     pygame.display.flip()
    
                    
# # pygame.quit()

# ### GAME RUNNING STUFF

# # class test2:
# #     attr = None
# #     def __init__(self):
# #         self.attr = 'e'
    
# #     def printx(self):
# #         print(self.attr)

# class CLASSs:
#     # Attributes
#     __one:list = None
#     __two = None

#     # Constructor
#     def __init__(self, one, two):
#         self.setOne(one)

#     # Getters
#     def getOne(self):
#         return self.__one
#     def getTwo(self):
#         return self.__two

#     # Setters
#     def setOne(self, one):
#         self.__one = one
#     def setTwo(self, two):
#         self.__two = two
    
#     # def e(self):
#     #     varone = self.getOne()
#     #     self.setOne(varone.append(1))

# #     def dostuff(self):
# #         """
# #         testing if a variable changes along with something
# #         """
# #         x = self.getOne()
# #         x = 3
# #         print(self.getOne())

# # neww = test('a', 'b')
# # neww.dostuff()

# new = CLASSs([2,3,4], 'e')
# new.e()
# print(new.getOne())
