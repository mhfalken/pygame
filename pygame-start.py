# Standard control loop in pygame
# Made by Michael Hansen 2021-23
import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game window
FPS = 60
WIN_WIDTH, WIN_HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SHIP_WIDTH = 20
SHIP_HEIGHT = 20

def main():
  ship = pygame.Rect(200, 300, SHIP_WIDTH, SHIP_HEIGHT)
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False # Spillet stopper

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          pass    # Her er trykket paa SPACE tasten
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_RIGHT]:
      ship.x += 1      # Her er trykket paa HOEJRE-PILE tast

    # Update display (WIN)
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, YELLOW, ship)  # Tegner den gule firkant
    pygame.display.update()


# --------------------------------------------- #
main()
pygame.quit()



"""
# Grafik
SHIP_IMAGE = pygame.image.load('ship.png')
SHIP_IMAGE = pygame.transform.scale(SHIP_IMAGE, (20, 20))
SHIP_IMAGE = pygame.transform.rotate(SHIP_IMAGE, 90)
SHIP_IMAGE = pygame.transform.flip(SHIP_IMAGE, True, True)
WIN.blit(SHIP_IMAGE, ship)

# Baggrundsbillede
WIN.blit(BACKGROUND_IMAGE, (0, 0))

# Tekst
SCORE_FONT = pygame.font.SysFont('comicsans', 20)
text = SCORE_FONT.render("Score: %i" %(score), 1, WHITE)
WIN.blit(text, (20, 5))

# Lyd
HIT_SOUND = pygame.mixer.Sound('explosion.mp3')
HIT_SOUND.play()

# Detekt kollision
if ship.colliderect(alien):
  pass

# Mus
if event.type == pygame.MOUSEBUTTONDOWN:
  (k1, k2, k3) = pygame.mouse.get_pressed()   # Museknapper: Venstre, midt, hoejre
  (x, y) = pygame.mouse.get_pos()             # Curser position (x, y)
  if k1 == True:
    pass

# Lister
liste = []            # Lav en tom liste
liste.append(item)    # Tilfoej element
liste.remove(item)    # Fjern element
len(liste)            # Antal elementer i listen
for item in liste:    # Loeb listen igennem
  pass

# Class
class EnemyClass:
  speed = 1
  def __init__(self, pygameRect, image):
    self.rect = pygameRect   # pygame.Rect(...)
    self.image = image       # pygame.image ...

enemy = EnemyClass(pygame.Rect(200, 200, 20, 5), ENEMY_IMAGE)
enemy.speed = 2

pygame.draw.rect(WIN, RED, enemy.rect)  # Vis som firkant
WIN.blit(enemy.image, enemy.rect)       # Vis som image


# Tilfaeldigt tal
random.randint(0, 100)  # [0-100]

# Delay
pygame.time.delay(2000)  # Vent 2000 ms (2 sekunder)

# Misc
os.path.join('effects', 'ship.png')

"""

