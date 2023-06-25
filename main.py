import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set the width and height of the display window
window_width = 800
window_height = 600
display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# Set the game's clock
clock = pygame.time.Clock()

# Set the size of the snake's body and the speed of the game
snake_block_size = 20
snake_speed = 15

# Set the font style and size for displaying the score
font_style = pygame.font.SysFont(None, 50)

# Function to display the current score
def your_score(score):
    value = font_style.render("Your Score: " + str(score), True, WHITE)
    display.blit(value, [0, 0])

# Function to display the high score
def high_score(score):
    value = font_style.render("High Score: " + str(score), True, WHITE)
    display.blit(value, [0, 50])

def our_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, GREEN, [x[0], x[1], snake_block_size, snake_block_size])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [window_width / 6, window_height / 3])

def game_loop():
    game_over = False
    game_end = False

    # Initial position of the snake
    x1 = window_width / 2
    y1 = window_height / 2

    # Change in position of the snake
    x1_change = 0
    y1_change = 0

    # Create the snake body as a list
    snake_List = []
    Length_of_snake = 1

    # Generate a random position for the food
    foodx = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
    foody = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0

    # Load and display the high score
    try:
        with open("highscore.txt", "r") as file:
            highscore = file.read()
            if highscore == '':
                highscore = 0
            high_score(int(highscore))
    except FileNotFoundError:
        highscore = 0
        high_score(highscore)
        
    # Initialize the high score variable
    high_score_value = int(highscore)

    while not game_over:

        while game_end == True:
            display.fill(BLACK)
            message("You lost! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            # Check for key presses
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Check for key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block_size
                    x1_change = 0

        # Check if the snake hits the boundaries of the window
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_end = True

        # Update the position of the snake
        x1 += x1_change
        y1 += y1_change
        display.fill(BLACK)
        pygame.draw.rect(display, BLUE, [foodx, foody, snake_block_size, snake_block_size])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_end = True

        our_snake(snake_block_size, snake_List)
        your_score(Length_of_snake - 1)
        high_score(high_score_value)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block_size) / 20.0) * 20.0
            foody = round(random.randrange(0, window_height - snake_block_size) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    # Update the high score if necessary
    if Length_of_snake - 1 > high_score_value:
        high_score_value = Length_of_snake - 1

    # Save the high score to a file
    with open("highscore.txt", "w") as file:
        file.write(str(high_score_value))

    pygame.quit()
    quit()

game_loop()
