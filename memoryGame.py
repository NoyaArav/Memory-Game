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
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Generate card images
card_images = []
for i in range(8):
    card_image = pygame.Surface((80, 120))
    card_image.fill(GRAY)
    pygame.draw.rect(card_image, WHITE, (10, 10, 60, 100), 2)
    text = pygame.font.Font(None, 48).render(str(i + 1), True, RED)
    card_image.blit(text, (20, 35))
    card_images.append(card_image)
    card_images.append(card_image)  # Duplicate each image

# Shuffle the card images
random.shuffle(card_images)

# Set up the game board
num_cols = 4
num_rows = 4
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

# Game loop
running = True
first_card = None
second_card = None
while running:
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
                    pygame.time.delay(1000)  # Delay for 1 second

    # Clear the window
    window.fill(GRAY)

    # Draw the cards
    for row in board:
        for card in row:
            if card["visible"]:
                window.blit(card["image"], card["rect"])
            else:
                pygame.draw.rect(window, WHITE, card["rect"])

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()