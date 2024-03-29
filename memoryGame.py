import random
import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Memory Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize the font for the timer
timer_font = pygame.font.Font(None, 36)  # Adjust the size as needed

# Load card back image
card_back = pygame.image.load("card_back.png")

# Generate card images
card_images = []
for i in range(6):
    card_image = pygame.Surface((80, 120))
    card_image.fill(LIGHT_GRAY)
    pygame.draw.rect(card_image, WHITE, (10, 10, 60, 100), 2)
    text = pygame.font.Font(None, 48).render(str(i + 1), True, RED)
    card_image.blit(text, (20, 35))
    card_images.append(card_image)
    card_images.append(card_image)  # Duplicate each image

# Shuffle the card images
random.shuffle(card_images)

# Set up the game board
num_cols = 4
num_rows = 3
card_width = 100
card_height = 150
card_margin = 20
board = []
for row in range(num_rows):
    row_cards = []
    for col in range(num_cols):
        x = col * (card_width + card_margin) + card_margin
        y = row * (card_height + card_margin) + card_margin
        image_index = row * num_cols + col
        row_cards.append({"rect": pygame.Rect(x, y, card_width, card_height),
                           "image": card_images[image_index],
                           "visible": False})
    board.append(row_cards)

# Capture the start time of the game
start_time = pygame.time.get_ticks()

# Game loop
running = True
first_card = None
second_card = None
non_matching_timer = 0
clock = pygame.time.Clock()
while running:
    # Cap the frame rate
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for row in board:
                for card in row:
                    if card["rect"].collidepoint(mouse_x, mouse_y):
                        if not card["visible"]:
                            if first_card is None:
                                first_card = card
                                card["visible"] = True
                            elif second_card is None and card != first_card:
                                second_card = card
                                card["visible"] = True
                            else:
                                first_card["visible"] = False
                                second_card["visible"] = False
                                first_card = None
                                second_card = None
                            break

            if first_card is not None and second_card is not None:
                if first_card["image"] == second_card["image"]:
                    first_card = None
                    second_card = None
                else:
                    non_matching_timer = pygame.time.get_ticks()  # Start the timer

    # Check for non-matching cards to flip back
    if non_matching_timer != 0 and pygame.time.get_ticks() - non_matching_timer >= 1000:
        first_card["visible"] = False
        second_card["visible"] = False
        first_card = None
        second_card = None
        non_matching_timer = 0

    # Clear the window
    window.fill(DARK_GRAY)

    # Draw the cards
    for row in board:
        for card in row:
            if card["visible"]:
                window.blit(card["image"], card["rect"])
            else:
                window.blit(card_back, card["rect"])

    # Calculate elapsed time for the timer
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    timer_text = f"{minutes:02}:{seconds:02}"  # Format: MM:SS
    timer_surface = timer_font.render(timer_text, True, WHITE)
    timer_rect = timer_surface.get_rect(topright=(window_width - 20, 20))  # Position: top-right
    window.blit(timer_surface, timer_rect)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()