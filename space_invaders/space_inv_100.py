import pygame
import os
pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = ( 255, 255, 0)
ALIEN_C = (255, 100, 100)

FPS = 60
WIN_WIDTH, WIN_HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

SCORE_FONT = pygame.font.SysFont('comicsans', 20)


def main():
  ship = pygame.Rect(WIN_WIDTH/2, WIN_HEIGHT - 50, 20, 20)
  shipBullets = []
  aliens = []
  for i in range(10):
    alien = pygame.Rect(50+i*40, 50, 20, 20)
    aliens.append(alien)
    alien = pygame.Rect(50+i*40, 80, 20, 20)
    aliens.append(alien)
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
        if event.key == pygame.K_SPACE:
          bullet = pygame.Rect(ship.x+ship.width/2-2, ship.y-10, 4, 10)
          shipBullets.append(bullet)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and ship.x > 10:
        ship.x -= 4
    if keys_pressed[pygame.K_RIGHT] and ship.x < (WIN_WIDTH - ship.width - 10):
        ship.x += 4

    # Move aliens
    if len(aliens) > 0:
      if alienMoveX > 0:
        if aliens[-1].x > WIN_WIDTH - 50:
          alienMoveX = -alienMoveX-0.3
          for a in aliens:
            a.y += 10      
      else:
        if aliens[0].x < 50:
          alienMoveX = -alienMoveX+0.3
          for a in aliens:
            a.y += 10
            if a.y > WIN_HEIGHT-10:
              aliens.remove(a)

      for a in aliens:
        a.x += alienMoveX
        if a.colliderect(ship):
          run = False

    # Move bullets
    for b in shipBullets:
      b.y -= 5
      if b.y < 0:
        shipBullets.remove(b)
      else:
        for a in aliens:
          if a.colliderect(b):
            # Kill alien
            aliens.remove(a)
            score += 10
    
    if len(aliens) == 0:
      run = False

    # Update display (WIN)
    WIN.fill(BLACK)
    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    WIN.blit(score_text, (20, 5))

    pygame.draw.rect(WIN, YELLOW, ship)
    for b in shipBullets:
      pygame.draw.rect(WIN, RED, b)
    for a in aliens:
      pygame.draw.rect(WIN, ALIEN_C, a)

    pygame.display.update()

main()
pygame.time.delay(2000)
pygame.quit()


