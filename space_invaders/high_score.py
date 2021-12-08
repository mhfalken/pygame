# High score list by Michael Hansen 2021
# Programmed in Python pygame
import pygame
import os
import random

pygame.font.init()

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Font
HIGH_FONT = pygame.font.SysFont('comicsans', 20)
CH_WIDTH = 12
CH_HEIGHT = 32

hfilename = "hsl_si.hsl"

def WaitKey():
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        return


def ReadHFile(filename):
  hlist = []
  try:
    f = open(filename, "r")
  except:
    return hlist
  lines = f.readlines()
  for line in lines:
    l = line.split(" ", 1)
    hlist.append((int(l[0]), l[1][:-1]))
  f.close()
  return hlist


def WriteHFile(filename, hlist):
  f = open(filename, "w")
  for (s, n) in hlist:
    line = "%i %s\n" %(s, n)
    f.write(line)
  f.close()


def ReadLine(WIN, pos, maxlen=20):
  """ pos = (x, y), where to place input box
      maxlen, avarage box len
  """
  posx, posy = pos
  text = ""
  run = True
  boxmax = False
  for event in pygame.event.get():
    pass # Clean queue

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False # Spillet stopper
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          run = False
          break
        if event.key == pygame.K_BACKSPACE:
          text = text[:-1]
          continue
        if event.key >= pygame.K_a and event.key <= pygame.K_z or event.key in [32, 229, 230, 248]:  # æøå
          if not boxmax:
            if event.mod & pygame.KMOD_SHIFT:
              text += chr(event.key-0x20)   # a -> A
            else:
              text += chr(event.key)
          
        #print(str(text))

    # Update display (WIN)
    tt = HIGH_FONT.render(text, 1, WHITE)
    if tt.get_width() > CH_WIDTH*(maxlen-1):
      boxmax = True
    else:
      boxmax = False
    pygame.draw.rect(WIN, BLACK, (posx, posy, CH_WIDTH*maxlen, CH_HEIGHT))
    pygame.draw.rect(WIN, BLUE, (posx, posy, CH_WIDTH*maxlen, CH_HEIGHT), 1)
    WIN.blit(tt, (posx+1, posy))
    pygame.display.update()
  return text


def PrintHighScoreList(WIN, pos, list):
  """ list = [(score, name)] # sorted list
  """
  (posx, posy) = pos
  offset = CH_WIDTH*8
  tt = HIGH_FONT.render("High score list", 1, YELLOW)
  WIN.blit(tt, (posx+offset-tt.get_width()/3, posy))
  posy += 2*CH_HEIGHT

  color = (255, 100, 100)
  for (s, n) in list:
    tt = HIGH_FONT.render("%8i" %s, 1, color)
    WIN.blit(tt, (posx+offset-tt.get_width(), posy))
    tt = HIGH_FONT.render("%s" %n, 1, WHITE)
    WIN.blit(tt, (posx+offset+2*CH_WIDTH, posy))
    posy += CH_HEIGHT
    color = (color[0]-10, color[1]+10, color[2]+10)
  tt = HIGH_FONT.render("Programmed by Michael Hansen 2021", 1, (0, 255, 0))
  WIN.blit(tt, (posx, posy+CH_HEIGHT))
  pygame.display.update()


def NewScore(WIN, pos, hlist, score, maxEntries=10):
  """ Check to see if highscore
  """
  (posx, posy) = pos
  newIndex = len(hlist)
  for i in range(len(hlist)):
    (s, n) = hlist[i]
    if score > s:
      newIndex = i
      break
  if newIndex < maxEntries and score > 0:
    tt = HIGH_FONT.render("New highscore: %i" %score, 1, RED)
    WIN.blit(tt, (posx, posy+CH_HEIGHT*5))
    name = ReadLine(WIN, (posx + tt.get_width()+10, posy+CH_HEIGHT*5))
    pygame.display.update()
    if len(name) > 0:
      hlist.insert(newIndex, (score, name))
    hlist = hlist[0:maxEntries]
  WIN.fill(BLACK)
  PrintHighScoreList(WIN, pos, hlist)
  WaitKey()
  return hlist


def AddNewScore(WIN, pos, score):
  WIN.fill(BLACK)
  hlist = ReadHFile(hfilename)
  hlist = NewScore(WIN, pos, hlist, score)
  WriteHFile(hfilename, hlist)

# --------------------------------------------- #

"""
pygame.mixer.init()

WIN_WIDTH, WIN_HEIGHT = 600, 500
WIN1 = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

AddNewScore(WIN1, (100, 20), random.randint(10, 2000))
pygame.quit()
"""

