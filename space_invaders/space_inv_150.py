import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = ( 255, 255, 0)
ALIEN_C = (255, 100, 200)
S_BULLET_C = (255, 0, 0)
E_BULLET_C = (255, 0, 255)

# Images
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 30
SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load(os.path.join('effects', 'ship1.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

EXPLOSION1 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'explosion1.png')), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

ALIEN_WIDTH, ALIEN_HEIGHT = 30, 30
ALIEN1 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien1.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))
ALIEN2 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien2.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))
ALIEN3 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien3.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))

# Sounds
SHIP_FIRE_SOUND = pygame.mixer.Sound(os.path.join('effects', 'laser1.ogg'))
EXPLOSION1_SOUND = pygame.mixer.Sound(os.path.join('effects', 'explosion1.ogg'))


FPS = 60
WIN_WIDTH, WIN_HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCORE_FONT = pygame.font.SysFont('comicsans', 20)


def main():
  dead = False
  ship = pygame.Rect(WIN_WIDTH/2, WIN_HEIGHT - 50, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  shipBullets = []
  enemyBullets = []
  aliens = []
  for i in range(10):
    alien = pygame.Rect(50+i*40, 50, ALIEN_WIDTH, ALIEN_HEIGHT)
    aliens.append((alien, ALIEN1))
    alien = pygame.Rect(50+i*40, 90, ALIEN_WIDTH, ALIEN_HEIGHT)
    aliens.append((alien, ALIEN2))
    alien = pygame.Rect(50+i*40, 130, ALIEN_WIDTH, ALIEN_HEIGHT)
    aliens.append((alien, ALIEN3))
  alienMoveX = 1
  score = 0

  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(shipBullets) < 3:
          bullet = pygame.Rect(ship.x+ship.width/2-2, ship.y-10, 4, 10)
          shipBullets.append(bullet)
          SHIP_FIRE_SOUND.play()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and ship.x > 10:
        ship.x -= 4
    if keys_pressed[pygame.K_RIGHT] and ship.x < (WIN_WIDTH - ship.width - 10):
        ship.x += 4

    # Move aliens
    if len(aliens) > 0:
      if alienMoveX > 0:
        if aliens[-1][0].x > WIN_WIDTH - 50:
          alienMoveX = -alienMoveX-0.3
          for (a, i) in aliens:
            a.y += 10      
      else:
        if aliens[0][0].x < 50:
          alienMoveX = -alienMoveX+0.3
          for (a, i) in aliens:
            a.y += 10
            if a.y > WIN_HEIGHT-10:
              aliens.remove((a, i))

      for (a, i) in aliens:
        a.x += alienMoveX
        if random.randint(0, 10000) < (20 - 4*len(enemyBullets)):
          enemyBullets.append(pygame.Rect(a.x+a.width/2-2, a.y+a.height, 4, 10))
        if a.colliderect(ship):
          EXPLOSION1_SOUND.play()
          run = False
          dead = True

    # Move ship bullets
    for b in shipBullets:
      b.y -= 5
      if b.y < 0:
        shipBullets.remove(b)
      else:
        for (a, i) in aliens:
          if a.colliderect(b):
            # Kill alien
            EXPLOSION1_SOUND.play()
            aliens.remove((a, i))
            shipBullets.remove(b)
            score += 10
    
    # Move enemy bullets
    for b in enemyBullets:
      b.y += 7
      if b.y > WIN_HEIGHT:
        enemyBullets.remove(b)
      else:
        if ship.colliderect(b):
          EXPLOSION1_SOUND.play()
          run = False
          dead = True

    if len(aliens) == 0:
      run = False

    # Update display (WIN)
    WIN.fill(BLACK)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(score_text, (20, 5))

    if dead:
      WIN.blit(EXPLOSION1, ship)
    else:
      WIN.blit(SPACESHIP, ship)

    for b in shipBullets:
      pygame.draw.rect(WIN, S_BULLET_C, b)
    for a in aliens:
      WIN.blit(a[1], a[0])
    for b in enemyBullets:
      pygame.draw.rect(WIN, E_BULLET_C, b)

    pygame.display.update()

main()
pygame.time.delay(2000)
pygame.quit()


