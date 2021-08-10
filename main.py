import pygame
from pygame import mixer
import random

score = 0
speed = 5

background_img = pygame.image.load("3d-hyperspace-background-with-warp-tunnel-effect.png")

player_img = pygame.image.load("rocket.png")
player_x = 370
player_y = 500
x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = 10
num_of_enemies = 10
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("ufo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(speed)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = player_x
bullet_y = player_y
bullet_y_change = 0
fire = False


# Show score
def show_score(x, y):
    score_value = font.render("Your score:" + str(score), True, (255, 0, 0))
    screen.blit(score_value, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def bullet(x, y):
    global fire
    fire = True
    screen.blit(bullet_img, (x + 16, y + 16))


def is_collision(bulletx, bullety, enemyx, enemyy):
    distance = (((enemyy - bullety) ** 2) + ((enemyx - bulletx) ** 2)) ** 1/2
    return distance < 40


def game_over():
    game = font.render("GAME OVER\n YOUR SCORE: " + str(score), True, (200, 200, 200))
    screen.blit(game, (200, 300))


pygame.init()

# background music
mixer.music.load("background.mp3")
mixer.music.play(-1)

# Collision sound
collision_sound = mixer.Sound("explosion.wav")

game_over_fnt = pygame.font.Font("grasping.ttf", 60)

font = pygame.font.Font('Homework.otf', 40)
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load("moon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Shoot UFO")

run = True
while run:
    # print(player_x, x_change)

    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (-1) * speed

            if event.key == pygame.K_RIGHT:
                x_change = speed

            if event.key == pygame.K_SPACE:
                if not fire:
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    fire = True
                    bullet_x = player_x

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0

    player_x += x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(num_of_enemies):
        # Game ending
        if enemy_y[i] >= player_y - 40:
            for j in range(num_of_enemies):
                enemy_y[j] = 1000
            game_over()
            break

        enemy_x[i] += enemy_x_change[i]

        if enemy_x[i] <= 0:
            enemy_x_change[i] = speed
            enemy_y[i] += enemy_y_change
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = (-1) * speed
            enemy_y[i] += enemy_y_change

        if is_collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i]):
            score += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 200)
            bullet_y = player_y
            fire = False
            collision_sound.play()
            print(score)

        enemy(enemy_x[i], enemy_y[i], i)

    if fire:
        bullet_y_change = (-1) * speed
        bullet_y += bullet_y_change
        bullet(bullet_x, bullet_y)

    if bullet_y < 0:
        fire = False
        bullet_y = player_y

    player(player_x, player_y)
    show_score(10, 10)

    pygame.display.update()
