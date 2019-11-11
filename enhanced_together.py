import os
import random
from colored import fore, style
import sys
import time
import copy
import getch
import simpleaudio as sa


def print_slow(str, t):
    """Print strings letter by letter, with given speed."""
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(t)


def display_menu():
    """Display the Tic-tac-Toe title, the menu and ask for the player's choice."""
    with open("main_screen.txt", mode="r", encoding="utf-8") as f:
        main_screen = f.read()
        print_slow(fore.DEEP_PINK_1B + main_screen + style.RESET, 0.001)
    main_menu_line1 = fore.GOLD_1 + "Main menu:".center(170)
    main_menu_line2 = "1 - Player vs. player".center(170)
    main_menu_line3 = "2 - Player vs. computer".center(228)
    print("\n")
    print_slow(main_menu_line1, 0.01)
    print("\n")
    print_slow(main_menu_line2, 0.01)
    print_slow(main_menu_line3, 0.01)
    print("\n")
    print_slow("Who would you like to play against?".center(174) + style.RESET, 0.01)
    print("\n")
    choice = getch.getch()
    return choice


def draw_tictac_board(board):
    """Refresh the screen and draw the board with appropriate colors."""
    bo_c = copy.deepcopy(board)
    for i in range(len(board)):
        if board[i] == "X":
            bo_c[i] = fore.SKY_BLUE_1 + "X" + style.RESET
        elif board[i] == "O":
            bo_c[i] = fore.GOLD_1 + "O" + style.RESET

    os.system("clear")
    print(bo_c[0], fore.DEEP_PINK_1B + " |" + style.RESET, bo_c[1], fore.DEEP_PINK_1B + "|" + style.RESET, bo_c[2])
    print(fore.DEEP_PINK_1B + "-----------" + style.RESET)
    print(bo_c[3], fore.DEEP_PINK_1B + " |" + style.RESET, bo_c[4], fore.DEEP_PINK_1B + "|" + style.RESET, bo_c[5])
    print(fore.DEEP_PINK_1B + "-----------" + style.RESET)
    print(bo_c[6], fore.DEEP_PINK_1B + " |" + style.RESET, bo_c[7], fore.DEEP_PINK_1B + "|" + style.RESET, bo_c[8])


def choose_number(board):
    """Ask for input from the player where to put 'X' or 'O' and ensure the validity of the input."""
    while True:
        try:
            print_slow(fore.CHARTREUSE_3A + "Pick a number: " + style.RESET, 0.02)
            a = int(getch.getch())
            if a > 0 and a < 10:
                return a
            else:
                print(fore.CHARTREUSE_3A + 'Haha, no....' + style.RESET)
        except ValueError:
            print(fore.CHARTREUSE_3A + "C'mon... Gimme a number " + style.RESET)


def place_X_or_O(board, character):
    """Place the player's 'X' or 'O' into the board's chosen (unoccupied) cell."""
    time.sleep(0.5)
    while True:
        if character == "X":
            print(fore.SKY_BLUE_1 + f"\n{character}, it's your turn." + style.RESET)
        else:
            print(fore.GOLD_1 + f"\n{character}, it's your turn." + style.RESET)
        n = choose_number(board)
        if board[n-1] == 'X' or board[n-1] == 'O':
            print('That space is occupied! ')
        else:
            board[n-1] = character
            break


def check_same_char(tuple, z):
    """Compare the values of a three-item sequence and return true if they are the same."""
    if tuple[0] == tuple[1] == tuple[2] == z:
        return True


def check_win_comb(board, z):
    """Check if any of the winning board combinations are present in the current state of the game."""
    win_comb = [[board[0], board[1], board[2]], [board[3], board[4], board[5]],
                [board[6], board[7], board[8]], [board[0], board[3], board[6]],
                [board[1], board[4], board[7]], [board[2], board[5], board[8]],
                [board[0], board[4], board[8]], [board[2], board[4], board[6]]]
    for i in range(len(win_comb)):
        if check_same_char(win_comb[i], z):
            return True


def run_multiplayer_game(board):
    """Run the game for two players."""
    while True:
        draw_tictac_board(board)
        place_X_or_O(board, "X")
        draw_tictac_board(board)
        if check_win_comb(board, 'X'):
            print(fore.SKY_BLUE_1 + "\nX Wins!" + style.RESET)
            play_sound("Applause.wav")
            break
        elif all(i != ' ' for i in board):
            print(fore.DEEP_PINK_1B + "\nThe game ends in a tie!" + style.RESET)
            break
        place_X_or_O(board, "O")
        draw_tictac_board(board)
        if check_win_comb(board, 'O'):
            print(fore.GOLD_1 + "\nO Wins!" + style.RESET)
            play_sound("Applause.wav")
            break
        elif all(i != ' ' for i in board):
            print(fore.DEEP_PINK_1B + "\nThe game ends in a tie!" + style.RESET)
            break


def run_singleplayer_game(board):
    """Run the game for single player against the computer."""
    player_wins_messages = ["Player_Wins_1.wav", "Player_Wins_2.wav", "Player_Wins_3.wav", "Player_Wins_4.wav"]
    computer_wins_messages = ["AI_Wins_1.wav", "AI_Wins_2.wav", "AI_Wins_3.wav", "AI_Wins_4.wav"]
    tie_game_messages = ["Tie_Game_1.wav", "Tie_Game_2.wav", "Tie_Game_3.wav", "Tie_Game_4.wav"]

    while True:
        draw_tictac_board(board)
        place_X_or_O(board, "X")
        draw_tictac_board(board)
        if check_win_comb(board, 'X'):
            print(fore.SKY_BLUE_1 + "\nX Wins!" + style.RESET)
            random_message(player_wins_messages)
            break
        elif all(i != ' ' for i in board):
            print(fore.DEEP_PINK_1B + "\nThe game ends in a tie!" + style.RESET)
            random_message(tie_game_messages)
            break
        time.sleep(0.5)
        AI(board)
        draw_tictac_board(board)
        if check_win_comb(board, 'O'):
            print(fore.GOLD_1 + "\nO Wins!" + style.RESET)
            random_message(computer_wins_messages)
            break
        elif all(i != ' ' for i in board):
            print(fore.DEEP_PINK_1B + "\nThe game ends in a tie!" + style.RESET)
            random_message(tie_game_messages)
            break


def AI_tactics(board, char):
    """Evaluate potential choices for the computer

    The function loops through all winning board combinations and checks if there are two equal values
    in a line / column / diagonal and whether the thrid cell is free to place an 'O' into. If yes, the
    given board cell is overwritten accordingly.
    """

    win_comb = [[board[0], board[1], board[2]], [board[3], board[4], board[5]],
                [board[6], board[7], board[8]], [board[0], board[3], board[6]],
                [board[1], board[4], board[7]], [board[2], board[5], board[8]],
                [board[0], board[4], board[8]], [board[2], board[4], board[6]]]
    for i in range(len(win_comb)):
        if win_comb[i][0] == win_comb[i][1] == char and win_comb[i][2] == " ":
            if i == 0:
                board[2] = "O"
            elif i == 1:
                board[5] = "O"
            elif i == 2 or i == 5 or i == 6:
                board[8] = "O"
            elif i == 3 or i == 7:
                board[6] = "O"
            else:
                board[7] = "O"
            return True
        elif win_comb[i][1] == win_comb[i][2] == char and win_comb[i][0] == " ":
            if i == 0 or i == 3 or i == 6:
                board[0] = "O"
            elif i == 1:
                board[3] = "O"
            elif i == 2:
                board[6] = "O"
            elif i == 5 or i == 7:
                board[2] = "O"
            else:
                board[1] = "O"
            return True
        elif win_comb[i][2] == win_comb[i][0] == char and win_comb[i][1] == " ":
            if i == 0:
                board[1] = "O"
            elif i == 1 or i == 4 or i == 6 or i == 7:
                board[4] = "O"
            elif i == 2:
                board[7] = "O"
            elif i == 3:
                board[3] = "O"
            elif i == 3:
                board[3] = "O"
            else:
                board[5] = "O"
            return True
    return False


def AI(board):
    """Main AI function

    It checks if the computer can win, if not, it checks whether it can stop the player from winning,
    and if neither of these conditions are true, it places its 'O' into a random cell.
    """

    if AI_tactics(board, "O"):
        return board
    elif AI_tactics(board, "X"):
        return board
    else:
        while True:
            rand_num = random.randrange(9)
            if board[rand_num] == " ":
                board[rand_num] = "O"
                return board


def play_sound(sound_file):
    """Play wav sounds"""
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def random_message(message_list):
    """Choose a sound message randomly when player / computer wins."""
    rand_num_for_sound = random.randrange(4)
    play_sound(message_list[rand_num_for_sound])


def main():
    reset = "y"
    while reset == "y":
        os.system('clear')
        board = [' ' for i in range(9)]
        versus = display_menu()
        if versus == "1":
            run_multiplayer_game(board)
        else:
            run_singleplayer_game(board)
        print_slow(fore.CHARTREUSE_3A + "Would you like to restart the game? Press 'y' or other button: " + style.RESET,
                   0.02)
        reset = getch.getch()


main()
