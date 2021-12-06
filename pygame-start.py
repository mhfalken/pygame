# Standard control loop in pygame
# Made by Michael Hansen 2021
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


def main():
  ship = pygame.Rect(200, 300, 20, 5)
  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False # Spillet stopper

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          pass    # Her er trykket på SPACE tasten
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT]:
      pass      # Her er trykket på VENSTRE-PILE tasten

    # Update display (WIN)
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, YELLOW, (ship.x, ship.y, ship.width, ship.height))  # Tegner den gule firkant
    pygame.display.update()


# --------------------------------------------- #
main()
pygame.quit()




"""
# Grafik
SHIP_IMAGE = pygame.image.load('ship.png')
SHIP_SCALE = pygame.transform.scale(SHIP_IMAGE, (20, 20))
SHIP_ROTATE = pygame.transform.rotate(SHIP_SCALE, 90)
WIN.blit(SHIP_IMAGE, ship)

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

# Lister
liste = []            # Lav en tom liste
liste.append(item)    # Tilføj element
liste.remove(item)    # Fjern element
len(liste)            # Antal elementer i listen
for item in liste:    # Løb listen igennem
  pass

# Tilfældigt tal
random.randint(0, 100)  # [0-100]

# Delay
pygame.time.delay(2000)  # Vent 2000 ms (2 sekunder)

# Misc
os.path.join('effects', 'ship.png')

"""
