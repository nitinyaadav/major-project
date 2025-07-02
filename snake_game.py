import pygame
import random
import os

pygame.mixer.init()
pygame.init()
difficulty_speed = 5
# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("SnakesWithHarry")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
import tkinter as tk
from tkinter import simpledialog

# Global variable to store difficulty speed
difficulty_speed = 5

def choose_difficulty():
    global difficulty_speed
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask for difficulty level
    level = simpledialog.askstring("Select Difficulty", "Choose Level: Easy / Medium / Hard").lower()

    if level == "easy":
        difficulty_speed = 4
    elif level == "medium":
        difficulty_speed = 7
    elif level == "hard":
        difficulty_speed = 10
    else:
        difficulty_speed = 5  # Default to medium if invalid input


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 210, 229))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))
    score = 0
    init_velocity = difficulty_speed
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                       choose_difficulty()  # Ask for difficulty again
                       gameloop()           # Restart the game with new difficulty # Avoid recursive stack overflow
                       return  # Avoid recursive stack overflow

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    elif event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            # Food Collision
            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 10
                food_x = random.randint(20, int(screen_width / 2))
                food_y = random.randint(20, int(screen_height / 2))
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score}  Hiscore: {hiscore}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Collision with self
            if head in snk_list[:-1]:
                game_over = True

            # Collision with wall
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

choose_difficulty()  # Call before welcome()
welcome()
