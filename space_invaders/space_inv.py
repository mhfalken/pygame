import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Space Invaders")

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

ALIEN_WIDTH, ALIEN_HEIGHT = 30, 30
ALIEN1 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien1.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))
ALIEN2 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien2.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))
ALIEN3 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'alien3.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))
UFO1 = pygame.transform.scale(pygame.image.load(os.path.join('effects', 'ufo1.png')), (ALIEN_WIDTH, ALIEN_HEIGHT))

EXPLOSIONS = []
for i in range(16):
  EXPLOSIONS.append(pygame.transform.scale(pygame.image.load(os.path.join('effects', 'ex%i.png' %(i+1))), (ALIEN_WIDTH, ALIEN_HEIGHT)))


# Sounds
SHIP_FIRE_SOUND = pygame.mixer.Sound(os.path.join('effects', 'laser1.ogg'))
EXPLOSION1_SOUND = pygame.mixer.Sound(os.path.join('effects', 'explosion1.ogg'))

# Fonts
SCORE_FONT = pygame.font.SysFont('comicsans', 20)

FPS = 60
WIN_WIDTH, WIN_HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

class EnemyInfo:
  def __init__(self, pygameRect, image):
    self.pgr = pygameRect   # pygame.Rect(...)
    self.image = image      # pygame.image ...
    self.px = self.pgr.x    # float
    self.py = self.pgr.y    # float
    self.SetTargetP(self.pgr.x, self.pgr.y, 1)

  def SetTargetP(self, targetX, targetY, speed):
    self.tx = targetX
    self.ty = targetY
    scale = abs(self.tx-self.pgr.x)/speed
    if scale < 1:
      scale = 1
    self.moveX = (self.tx-self.pgr.x)/scale
    self.moveY = (self.ty-self.pgr.y)/scale


# Global variables
score = 0
dead = False
round = 1

def main():
  global score, dead, round
  ship = pygame.Rect(WIN_WIDTH/2, WIN_HEIGHT - 50, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  shipBullets = []
  enemyBullets = []
  aliens = []
  ufos = []
  explosions = []
  shieldCnt = 2
  shieldActive = 0
  shieldHit = 0

  for i in range(10):
    alien = pygame.Rect(50+i*40, 50, ALIEN_WIDTH, ALIEN_HEIGHT)
    aliens.append((alien, ALIEN1))
    if round > 1:
      alien = pygame.Rect(50+i*40, 90, ALIEN_WIDTH, ALIEN_HEIGHT)
      aliens.append((alien, ALIEN2))
    if round > 2:
      alien = pygame.Rect(50+i*40, 130, ALIEN_WIDTH, ALIEN_HEIGHT)
      aliens.append((alien, ALIEN3))
  alienMoveX = 1

  if round > 1:
    info = EnemyInfo(pygame.Rect(20, 30, ALIEN_WIDTH, ALIEN_HEIGHT), UFO1)
    ufos.append(info)

  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(shipBullets) < 4:
          bullet = pygame.Rect(ship.x+ship.width/2-2, ship.y-10, 4, 10)
          shipBullets.append(bullet)
          SHIP_FIRE_SOUND.play()
        if event.key == pygame.K_s and shieldCnt > 0 and shieldActive < 25:
          shieldCnt -= 1
          shieldActive = FPS*4

    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and ship.x > 10:
        ship.x -= 4
    if (keys_pressed[pygame.K_RIGHT]  or keys_pressed[pygame.K_d]) and ship.x < (WIN_WIDTH - ship.width - 10):
        ship.x += 4

    # Move aliens
    if len(aliens) > 0:
      if alienMoveX > 0:
        if aliens[-1][0].x > WIN_WIDTH - 50:
          alienMoveX = -alienMoveX-0.3
          for (a, i) in aliens:
            a.y += 10      
      else:
        if aliens[0][0].x < 30:
          alienMoveX = -alienMoveX+0.3
          for (a, i) in aliens:
            a.y += 10
            if a.y > WIN_HEIGHT-10:
              aliens.remove((a, i))

      for (a, i) in aliens:
        a.x += alienMoveX
        if random.randint(0, 10000) < (12 - 5*len(enemyBullets)):
          enemyBullets.append(pygame.Rect(a.x+a.width/2-2, a.y+a.height, 4, 10))
        if a.colliderect(ship):
          EXPLOSION1_SOUND.play()
          run = False
          dead = True

    # Move UFOs
    for (info) in ufos:
      u = info.pgr
      info.px += info.moveX
      info.py += info.moveY
      u.x = info.px
      u.y = info.py
      if abs(info.tx-u.x) < 10:
        info.SetTargetP(random.randint(0, WIN_WIDTH), info.ty + random.randint(10, 30), random.randint(3,6))
      if u.y > WIN_HEIGHT:
        ufos.remove(info)
      if u.colliderect(ship):
        EXPLOSION1_SOUND.play()
        if shieldActive == 0:
          run = False
          dead = True
        else:
          shieldHit = 4
          explosions.append((info.pgr, 0))
          ufos.remove(info)

      if abs(u.x-ship.x) < 10 and len(enemyBullets) < 3 and random.randint(0, 10) > 8:
        enemyBullets.append(pygame.Rect(u.x+u.width/2-2, u.y+u.height, 4, 10))

    # Move enemy bullets
    for b in enemyBullets:
      b.y += 7
      if b.y > WIN_HEIGHT:
        enemyBullets.remove(b)
      else:
        if ship.colliderect(b):
          if shieldActive == 0:
            # Dead
            EXPLOSION1_SOUND.play()
            run = False
            dead = True
          else:
            shieldHit = 4
            enemyBullets.remove(b)

    # Move ship bullets
    for b in shipBullets:
      bulletUsed = 0
      b.y -= 5
      if b.y < 0:
        shipBullets.remove(b)
      else:
        for (a, i) in aliens:
          if a.colliderect(b):
            # Kill alien
            EXPLOSION1_SOUND.play()
            explosions.append((a, 0))
            aliens.remove((a, i))
            shipBullets.remove(b)
            score += 10
            bulletUsed = 1
            break
        if bulletUsed == 0:
          for info in ufos:
            if info.pgr.colliderect(b):
              # Kill ufo
              EXPLOSION1_SOUND.play()
              explosions.append((info.pgr, 0))
              ufos.remove(info)
              shipBullets.remove(b)
              score += 50
              if len(ufos) < min(3, len(aliens)):
                info = EnemyInfo(pygame.Rect(random.randint(20, WIN_WIDTH), 100, ALIEN_WIDTH, ALIEN_HEIGHT), UFO1)
                ufos.append(info)
                info = EnemyInfo(pygame.Rect(random.randint(20, WIN_WIDTH), 100, ALIEN_WIDTH, ALIEN_HEIGHT), UFO1)
                ufos.append(info)
              break
    
    if len(aliens) == 0 and len(ufos) == 0:
      run = False

    # Update display (WIN)
    WIN.fill(BLACK)
    score_text = SCORE_FONT.render("Score: %s   Shields %i" %(score, shieldCnt), 1, WHITE)
    WIN.blit(score_text, (20, 5))
    text = SCORE_FONT.render("FPS: %i" %(clock.get_fps()), 1, WHITE)
    WIN.blit(text, (WIN_WIDTH-text.get_width()-20, 5))

    if dead:
      WIN.blit(EXPLOSIONS[3], ship)
    else:
      if shieldActive > 0:
        if shieldHit > 0:
          pygame.draw.circle(WIN, RED, (ship.x+ship.width/2, ship.y+ship.width/2-2), ship.width/2)
          shieldHit -= 1
        else:
          pygame.draw.circle(WIN, YELLOW, (ship.x+ship.width/2, ship.y+ship.width/2-2), ship.width/2)
        shieldActive -= 1
      if shieldActive < 30 and shieldActive%8 < 4:
        pygame.draw.circle(WIN, BLACK, (ship.x+ship.width/2, ship.y+ship.width/2-2), ship.width/2-3)
      WIN.blit(SPACESHIP, ship)

    expl = []
    for (a, i) in explosions:
      WIN.blit(EXPLOSIONS[i], a)
      explosions.remove((a, i))
      if i < 15:
        expl.append((a, i+1))
    explosions = expl

    for b in shipBullets:
      pygame.draw.rect(WIN, S_BULLET_C, b)
    for a in aliens:
      WIN.blit(a[1], a[0])
    for info in ufos:
      WIN.blit(info.image, info.pgr)
    for b in enemyBullets:
      pygame.draw.rect(WIN, E_BULLET_C, b)

    pygame.display.update()

while dead == False:
  main()
  round += 1

pygame.draw.rect(WIN, (100, 100, 100), (200, 200, 200, 100))
if dead:
  text = SCORE_FONT.render("YOU ARE DEAD", 1, RED)
else:
  text = SCORE_FONT.render("YOU WON", 1, YELLOW)
WIN.blit(text, (WIN_WIDTH/2-text.get_width()/2, WIN_HEIGHT/2 - 40))

text = SCORE_FONT.render("Final score: " + str(score), 1, WHITE)
WIN.blit(text, (WIN_WIDTH/2-text.get_width()/2, WIN_HEIGHT/2))
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()


