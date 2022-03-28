import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen with height and width
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480

# Enemy
# before
""" 
    enemyImg =pygame.image.load('enemy.png')
    enemyX = random.randint(0, 801)
    enemyY = random.randint(50, 150)
    enemyX_change = 5
    enemyY_change = 50
"""
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 5
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 801))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Multiple enemies


# Bullet
# Ready- Can not see bullet on screen
# Fire - Bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Scores
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    # Render then blit
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)
game_overX = 200
game_overY = 200


def game_over_text(x, y):
    over = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (x, y))


def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (X + 16, Y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance <= 27:
        return True
    else:
        return False


def enemy(A, B, i):
    screen.blit(enemyImg[i], (A, B))


# Mechanise the spaceship
playerX_change = 0


def player(x, y):
    # Draw image on screen
    # Need to draw after load
    screen.blit(playerImg, (x, y))


# Game loop
# Add event to check if * is checked

running = True
while running:
    # Background screen
    screen.fill((0, 150, 250))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed, check if it's right or left key.
        # Key Down check any key pressed.

        if event.type == pygame.KEYDOWN:
            print("Keystroke is pressed")
            if event.key == pygame.K_LEFT:
                print("Left Arrow is pressed")
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get current X coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

                    # sound not music because duration is short
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print(f"Key has been released")
                playerX_change = 0

    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # Enemy
    for i in range(num_of_enemies):
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

        # Game over
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text(game_overX,game_overY)
            break



            # Collision
        collision = isCollision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score_value += 1

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)

    # This is necessary to update the loop
    pygame.display.update()
