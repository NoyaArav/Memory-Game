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
LIGHT_PINK = (255, 192, 203)  # Light pink color
PINK1 = (255, 136, 202)
FUCHSIA = (255, 92, 170)
PURPLE = (219, 116, 243)

# Initialize the font for the timer, button, and message
timer_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)
message_font = pygame.font.Font(None, 200)

# Load card back image
card_back = pygame.image.load("card_back.png")

# Load sound effects
match_sound = pygame.mixer.Sound("match_sound.wav")
gameOver_sound = pygame.mixer.Sound("game_over_applause.wav")


# Pre-game player selection
one_player_button = pygame.Rect(window_width // 2 - 150, window_height // 2 - 60, 100, 50)
two_player_button = pygame.Rect(window_width // 2 + 50, window_height // 2 - 60, 100, 50)
num_players = 0
current_player = 1

# Pre-game loop for player selection
while num_players == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if one_player_button.collidepoint(mouse_x, mouse_y):
                num_players = 1
            elif two_player_button.collidepoint(mouse_x, mouse_y):
                num_players = 2

    window.fill(LIGHT_PINK)
    pygame.draw.rect(window, FUCHSIA, one_player_button)
    pygame.draw.rect(window, FUCHSIA, two_player_button)
    one_player_text = button_font.render("1 Player", True, WHITE)
    two_player_text = button_font.render("2 Players", True, WHITE)
    window.blit(one_player_text, one_player_button.move(20, 10))
    window.blit(two_player_text, two_player_button.move(10, 10))
    pygame.display.update()
    
    

# Set up the "Reset" button
button_width = 100
button_height = 50
button_x = window_width - button_width - 20
button_y = 80
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Initialize the clock
clock = pygame.time.Clock()

def reset_game():
    global card_images, board, start_time, first_card, second_card, non_matching_timer, all_matched, final_time, show_message

    # Generate new card images
    card_images = []
    for i in range(6):
        card_image = pygame.Surface((80, 120))
        card_image.fill(LIGHT_GRAY)
        pygame.draw.rect(card_image, WHITE, (10, 10, 60, 100), 2)
        text = pygame.font.Font(None, 48).render(str(i + 1), True, PINK1)
        card_image.blit(text, (20, 35))
        card_images.append(card_image)
        card_images.append(card_image)  # Duplicate each image

    # Shuffle the card images
    random.shuffle(card_images)

    # Reset the game board
    board = []
    for row in range(num_rows):
        row_cards = []
        for col in range(num_cols):
            x = col * (card_width + card_margin) + card_margin
            y = row * (card_height + card_margin) + card_margin +60
            image_index = row * num_cols + col
            row_cards.append({"rect": pygame.Rect(x, y, card_width, card_height),
                               "image": card_images[image_index],
                               "visible": False})
        board.append(row_cards)

    # Reset game variables
    start_time = pygame.time.get_ticks()
    first_card = None
    second_card = None
    non_matching_timer = 0
    all_matched = False
    final_time = 0
    show_message = False

# Set up the game board
num_cols = 4
num_rows = 3
card_width = 100
card_height = 150
card_margin = 20
reset_game()

def check_all_matched():
    for row in board:
        for card in row:
            if not card["visible"]:
                return False
    return True

# Game loop
running = True
message_y = window_height  # Initialize message to be off-screen
while running:
    # Cap the frame rate
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):
                reset_game()
            else:
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
                    match_sound.play()  # Play the match sound
                    if num_players == 2: # Optionally, let the current player continue if they found a match.
                        pass  # current_player stays the same
                else:
                    # If the cards do not match and it's a 2-player game, switch turns
                    if num_players == 2:
                        current_player = 2 if current_player == 1 else 1
                    non_matching_timer = pygame.time.get_ticks()  # Start the timer

    # Check for non-matching cards to flip back
    if non_matching_timer != 0 and pygame.time.get_ticks() - non_matching_timer >= 1000:
        first_card["visible"] = False
        second_card["visible"] = False
        first_card = None
        second_card = None
        non_matching_timer = 0

    # Check if all cards are matched
    all_matched = check_all_matched()
    if all_matched and final_time == 0:
        final_time = pygame.time.get_ticks() - start_time
        show_message = True

    # Clear the window
    window.fill(DARK_GRAY)

    # Draw the cards
    for row in board:
        for card in row:
            if card["visible"]:
                window.blit(card["image"], card["rect"])
            else:
                window.blit(card_back, card["rect"])

    # Draw the "Reset" button
    pygame.draw.rect(window, LIGHT_PINK, button_rect)
    button_text = button_font.render("Reset", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    window.blit(button_text, button_text_rect)

    # Calculate elapsed time for the timer
    elapsed_time = final_time if final_time != 0 else pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    timer_text = f"{minutes:02}:{seconds:02}"  # Format: MM:SS
    timer_surface = timer_font.render(timer_text, True, WHITE)
    timer_rect = timer_surface.get_rect(topright=(window_width - 20, 20))  # Position: top-right
    window.blit(timer_surface, timer_rect)

    # Draw the "Well done!" message and "Play Again" button
    if show_message:
        message_text = message_font.render("Well done!", True, PURPLE)
        message_rect = message_text.get_rect(center=(window_width // 2, message_y))
        message_y -= 1  # Move the message up 5 pixels each frame
        gameOver_sound.play()
        
        # Move the message up until it reaches the top of the screen
        if message_y > 0:
            message_y -= 5  # Move the message up 5 pixels each frame
        else:
            # Reset message_y to the bottom when it reaches the top
            message_y = window_height
        
        window.blit(message_text, message_rect)

        play_again_button_rect = pygame.Rect(window_width // 2 - 75, message_y + 100, 150, 50)
        pygame.draw.rect(window, LIGHT_PINK, play_again_button_rect)
        play_again_text = button_font.render("Play Again", True, BLACK)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
        window.blit(play_again_text, play_again_text_rect)

        if play_again_button_rect.collidepoint(mouse_x, mouse_y):
            reset_game()
            show_message = False  # Hide message after reset

    if num_players == 2:
        player_turn_text = f"Player {current_player}'s Turn"
        turn_surface = timer_font.render(player_turn_text, True, WHITE)
        turn_rect = turn_surface.get_rect(center=(window_width // 2, 30))  # Position this at the top center
        window.blit(turn_surface, turn_rect)
    
    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()