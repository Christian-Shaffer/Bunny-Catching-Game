import pygame
from sys import exit
import random
import os

# Basic data about game
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Bunny Catcher')
clock = pygame.time.Clock()
game_active = True
start_time = 0
score = 0
level = 1
bunny_speed = 3
health = 3
bg_music_path = os.path.join(
    'Catching Bunnies Game', 'Audio track', 'Small-Town.mp3')
bg_music = pygame.mixer.Sound(bg_music_path)
bg_music.set_volume(0.05)
bg_music.play(loops=-1)

# Background image data
background_path = os.path.join(
    'Catching Bunnies Game', 'Graphics', 'background.jpg')
background_image = pygame.image.load(background_path)
background_image = pygame.transform.scale(background_image, (800, 400))

# Hearts image data
full_heart_path = os.path.join(
    'Catching Bunnies Game', 'Graphics', 'full_heart.png')
full_heart = pygame.image.load(full_heart_path)
full_heart = pygame.transform.scale(full_heart, (52, 48))

empty_heart_path = os.path.join(
    'Catching Bunnies Game', 'Graphics', 'empty_heart.png')
empty_heart = pygame.image.load(empty_heart_path)
empty_heart = pygame.transform.scale(empty_heart, (52, 48))

# Font to be used on the on-screen text
my_font = pygame.font.Font(None, 36)

# Basket sprite data
basket_path = os.path.join('Catching Bunnies Game', 'Graphics', 'basket.png')
basket_image = pygame.image.load(basket_path)
basket_image = pygame.transform.scale(basket_image, (75, 75))
basket_rect = basket_image.get_rect(center=(400, 310))

# Bunny sprite data
bunny_path = os.path.join('Catching Bunnies Game', 'Graphics', 'bunny.png')
bunny_image = pygame.image.load(bunny_path)
bunny_image = pygame.transform.scale(bunny_image, (84, 47))
bunny_rect = bunny_image.get_rect()
bunny_rect.x = random.randint(0, 800 - bunny_rect.width)
bunny_rect.y = 0


def get_highscore():  # Getting highscore data
    try:
        with open('highscore.txt', 'r') as f:
            highscore = int(f.read())
    except FileNotFoundError:
        highscore = 0
    return highscore


def update_highscore(new_highscore):  # Updating highscore function
    with open('highscore.txt', 'w') as f:
        f.write(str(new_highscore))


def start_screen(message):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:  # Any key press will break the loop
                return

        screen.fill((94, 129, 162))  # Pretty blue color
        game_name = my_font.render(
            'Bunny Catcher', True, (0, 0, 0))  # Black color
        screen.blit(game_name, (300, 50))

        large_bunny_image = pygame.transform.scale(bunny_image, (335, 182))
        screen.blit(large_bunny_image, (230, 100))

        highscore = get_highscore()

        if message is not None and message > highscore:
            update_highscore(message)
            highscore = message

        if message is None:
            message_text = my_font.render(
                'Press any key to start', True, (0, 0, 0))  # Black color
        else:
            message_text = my_font.render(
                f'Your Score: {message}. Highscore: {highscore}', True, (0, 0, 0))  # Black color

        text_width = message_text.get_width()
        screen.blit(message_text, ((800 - text_width) / 2, 300))

        pygame.display.update()
        clock.tick(60)


# Calling start screen before the game itself starts
start_screen(None)

# Game loop
while True:
    while game_active == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Moving the basket left and right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_rect.x > 0:
            basket_rect.x -= 8
        if keys[pygame.K_RIGHT] and basket_rect.x < 725:
            basket_rect.x += 8

        # Drawing the background, basket, and bunny on screen
        screen.blit(background_image, (0, 0))
        screen.blit(basket_image, basket_rect)
        screen.blit(bunny_image, bunny_rect)

        # Render the score
        score_text = my_font.render(
            f'Score: {score}', True, (0, 0, 0))  # Black color
        screen.blit(score_text, (10, 10))

        # Render the level
        level_text = my_font.render(
            f'Level: {level}', True, (0, 0, 0))  # Black color
        screen.blit(level_text, (360, 10))

        # Render the hearts depending on the health
        if health == 3:
            screen.blit(full_heart, (640, 0))
            screen.blit(full_heart, (690, 0))
            screen.blit(full_heart, (740, 0))
        elif health == 2:
            screen.blit(empty_heart, (640, 0))
            screen.blit(full_heart, (690, 0))
            screen.blit(full_heart, (740, 0))
        elif health == 1:
            screen.blit(empty_heart, (640, 0))
            screen.blit(empty_heart, (690, 0))
            screen.blit(full_heart, (740, 0))
        elif health == 0:
            screen.blit(empty_heart, (640, 0))
            screen.blit(empty_heart, (690, 0))
            screen.blit(empty_heart, (740, 0))
            game_active = False

        # Make the bunny fall down
        bunny_rect.y += bunny_speed

        # Getting points from catching the bunny
        if bunny_rect.colliderect(basket_rect):
            bunny_rect.x = random.randint(0, 800 - bunny_rect.width)
            bunny_rect.y = 0
            score += 1
            if score % 10 == 0:
                level += 1
                bunny_speed += 0.2

        # Resetting the bunny when it misses
        elif bunny_rect.y > 400:
            bunny_rect.x = random.randint(0, 800 - bunny_rect.width)
            bunny_rect.y = 0
            health -= 1

        # Updating the game per frame and making it 60 fps
        pygame.display.update()
        clock.tick(60)

    # When the player loses (game_active becomes False), call the start_screen() function with the score
    if not game_active:
        start_screen(score)

        # Reset the game data
        game_active = True
        score = 0
        level = 1
        bunny_speed = 3
        health = 3

        # Reset the bunny position
        bunny_rect.x = random.randint(0, 800 - bunny_rect.width)
        bunny_rect.y = 0
