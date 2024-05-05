
import pygame
import sys, subprocess
import string, os
import random
pygame.init()


def spawn_program_and_die(program, exit_code=0):
    """
    Start an external program and exit the script
    with the specified return code.

    Takes the parameter program, which is a list
    that corresponds to the argv of your command.
    """
    # Start the external program
    # subprocess.Popen(program)
    os.startfile(program)

    # We have started the program, and can suspend this interpreter
    # sys.exit(exit_code)


# Constants
WIDTH, HEIGHT = 1400, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uno Game")

card_images = {}
colors = ['red', 'green', 'blue', 'yellow']
for color in colors:
    for value in range(10):
        card_images[f'{color}_{value}'] = pygame.image.load(f'{color}_{value}.png').convert_alpha()
    card_images[f'{color}_plus2'] = pygame.image.load(f'{color}_plus2.png').convert_alpha()

card_images['random'] = pygame.image.load('random.png').convert_alpha()

highest_streak = 0
try:
    with open("highest_streak.txt", "r") as file:
        highest_streak = int(file.read())
except FileNotFoundError:
    pass

# Game variables
player_wins = 0
computer_wins = 0
player_streak = 0
total_moves = 0
last_played = False
score_uno = 0
deck = []


# Functions
def reset_game(reset_streak=True):
    global deck, player_hand, computer_hand, discard_pile, player_turn, winner, total_moves
    deck = [{'color': color, 'value': value} for color in colors for value in range(10)]
    random.shuffle(deck)
    player_hand = [deck.pop() for _ in range(7)]
    computer_hand = [deck.pop() for _ in range(7)]
    discard_pile = [deck.pop()]
    player_turn = True
    winner = None
    total_moves = 0

    if reset_streak:
        player_streak = 0


reset_game()


class Button:
    def __init__(self, text, x, y, width, height, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Create Next Game button
next_game_button = Button("Next Game", 0, HEIGHT / 2, 150, 50, BLACK, WHITE)

minesweeper_button = Button("Minesweeper", WIDTH - 190, HEIGHT / 2, 150, 50, BLACK, WHITE)


def save_highest_streak():
    with open("highest_streak.txt", "w") as file:
        file.write(str(highest_streak))

def draw_card(card, x, y):
    if card == 'random':
        screen.blit(card_images[card], (x, y))
    else:
        screen.blit(card_images[f"{card['color']}_{card['value']}"], (x, y))


def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_game():
    screen.fill(WHITE)

    minesweeper_button.draw(screen)

    # Draw discard pile
    draw_card(discard_pile[-1], WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2)

    # Draw random card area
    draw_card('random', WIDTH // 4 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2)

    # Draw player's hand
    for i, card in enumerate(player_hand):
        draw_card(card, i * CARD_WIDTH, HEIGHT - CARD_HEIGHT)

    for i, card in enumerate(computer_hand):
        draw_card(card, i * CARD_WIDTH, 0)

    # Draw winner text
    if winner:
        draw_text(f"{winner} wins!", 40, BLACK, WIDTH // 2 + 200, HEIGHT // 2)

    # Draw player and computer win counts
    draw_text(f"Player wins: {player_wins}", 20, BLACK, WIDTH // 2, HEIGHT - 200)
    draw_text(f"Computer wins: {computer_wins}", 20, BLACK, WIDTH // 2, 200)

    # Draw player streak
    draw_text(f"Current streak: {player_streak}", 20, BLACK, WIDTH // 2 + 200, 250)
    draw_text(f"Highest streak: {highest_streak}", 20, BLACK, WIDTH // 2 + 200, 300)

    # Draw total moves
    draw_text(f"Total moves: {total_moves}", 20, BLACK, WIDTH // 2 + 200, 350)
    score_uno = check_points_from_minesweeper()
    if score_uno <= 0:
        colour_for_coins = RED
    elif score_uno < 5:
        colour_for_coins = ORANGE
    else:
        colour_for_coins = GREEN
    draw_text(f"Minesweeper coins: {score_uno}", 25, colour_for_coins, WIDTH - 120, HEIGHT / 2 + 70)
    # Draw next game button if there is a winner
    if winner:
        next_game_button.draw(screen)

    pygame.display.flip()


def card_clicked(x, y):
    if WIDTH // 4 - CARD_WIDTH // 2 <= x <= WIDTH // 4 + CARD_WIDTH // 2 and HEIGHT // 2 - CARD_HEIGHT // 2 <= y <= HEIGHT // 2 + CARD_HEIGHT // 2:
        return 'random'
    for i, card in enumerate(player_hand):
        if i * CARD_WIDTH <= x <= (i + 1) * CARD_WIDTH and HEIGHT - CARD_HEIGHT <= y <= HEIGHT:
            return i
    return None


def can_place_card(selected_card):
    top_card = discard_pile[-1]
    score_uno = check_points_from_minesweeper()
    if (selected_card['color'] == top_card['color'] and score_uno > 0) or (selected_card['value'] == top_card['value'] and score_uno > 0):
        return True
    return False

def computer_play():
    global player_turn, winner, player_streak, last_played
    # for card in computer_hand:
    for i, card in enumerate(computer_hand):
        if can_place_card(card):
            discarded_card = computer_hand.pop(i)
            discard_pile.append(discarded_card)
            return discarded_card
    if deck:
        drawn_card = deck.pop()
        computer_hand.append(drawn_card)
        return drawn_card
    return None

# Game loop
clock = pygame.time.Clock()
running = True
player_turn = True
winner = None

def check_points_from_minesweeper():
    try:
        with open("score_uno.txt", "r") as file:
            score_uno = int(file.read())

            return score_uno
    except FileNotFoundError:
        pass

def update_points_from_minesweeper():
    score_uno = check_points_from_minesweeper()
    score_uno -= 1
    with open("score_uno.txt", "w") as file:
        file.write(str(score_uno))

while running:
    top_card = discard_pile[-1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if minesweeper_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:
                spawn_program_and_die('.\\dist\\Main.exe') #Due to shortage of ammunition it doesn't die
            if winner and next_game_button.is_clicked(pygame.mouse.get_pos()) and event.button == 1:
                reset_game()
            elif player_turn:
                top_card = discard_pile[-1]
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    selected_card_index = card_clicked(x, y)
                    if selected_card_index == 'random':
                        if not deck:
                            random.shuffle(deck)
                        drawn_card = deck.pop()
                        player_hand.append(drawn_card)
                        player_turn = False
                        total_moves += 1
                        update_points_from_minesweeper()


                    elif selected_card_index is not None:
                        selected_card = player_hand[selected_card_index]
                        if can_place_card(selected_card):
                            player_hand.remove(selected_card)
                            discard_pile.append(selected_card)
                            player_turn = False
                            total_moves += 1
                            update_points_from_minesweeper()
                            if total_moves > 20:
                                deck = [{'color': color, 'value': value} for color in colors for value in range(10)]
                                for color in colors:
                                    deck.append({'color': color, 'value': 'plus2'})
                                random.shuffle(deck)

    if not winner:
        if not player_hand:
            winner = "Player"
            player_wins += 1
            player_streak += 1
            highest_streak = max(player_streak, highest_streak)

        elif not computer_hand:
            winner = "Computer"
            computer_wins += 1
            player_streak = 0

    if not player_turn and not winner:
        discarded_card = computer_play()
        if discarded_card:
            player_turn = True

    check_points_from_minesweeper()
    draw_game()

save_highest_streak()

pygame.quit()
sys.exit()
