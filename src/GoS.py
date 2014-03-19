###################################################
# File:         GoS.py
# Author:       Jacob Calvert
# Date:         03/14/2014
# Description:  This file is the entry point for
# my implementation of the Game of Sticks with an
# AI component.
# Hosted:       https://github.com/jacobcalvert/GameOfSticks.git
###################################################
import GameModes

MAIN_MENU = 1       # menu enums
PLAYAGAIN_MENU = 2  # menu enums


def menu(which):
    """
    menu(which) prints the selected menu
    """
    if which is MAIN_MENU:
        print("MENU")
        print("  1) Human VS Human")
        print("  2) Human VS AI")
        print("  3) AI VS AI")
    elif which is PLAYAGAIN_MENU:
        print("Play Again? 0=no 1=yes")


def get_selection(T, lower, upper, prompt, error):
    """
        get_selection - abstracted way to prompt for and get bounded
        inputs. Used in mode selection, stick selection etc. returns a
        tuple => (success, value)
    """
    val = 0
    try:
        val = T(input(prompt))
    except Exception as err:
        error += " " + str(err)

    if val is not None and val <= upper and val >=lower:
        return (True, val)
    else:
        print(error % (val, lower, upper))
        return (False, None)


def main():
    """
    main - this is the entry point for my Game of Stick impl.
    we essentially start a while loop and as long as the user wants
    to keep playing, we don't exit the loop.
    """
    print("Welcome to the Game of Sticks!!")
    exit_game = 1
    while exit_game != 0:
        menu(MAIN_MENU)
        ret_val, game_index = get_selection(int, 1, 3, "Which mode do you choose?", "Error, %d is not in range [%d, %d]")
        if not ret_val:
            continue
        ret_val2 , sticks = get_selection(int,10,100,"How many sticks?","Number %d is not in range [%d, %d]")
        while not ret_val2:
            ret_val2 , sticks = get_selection(int,10,100,"How many sticks?","Number %d is not in range [%d, %d]")
        if ret_val and ret_val2:
            game_type = GameModes.get_game_mode(game_index)
            if game_type == GameModes.HumanVAI:
                ret_val, train_ai = get_selection(int,0,1,"Train AI? 0=no 1=yes","%d not in [%d, %d]")
                while not ret_val:
                     ret_val, train_ai = get_selection(int,0,1,"Train AI? 0=no 1=yes","%d not in [%d, %d]")
                if train_ai == 1:
                    game_obj = game_type(sticks, True)
                    game_obj.game_loop()
                else:
                    game_obj = game_type(sticks)
                    game_obj.game_loop()
            else:
                game_obj = game_type(sticks)
                game_obj.game_loop()
            menu(PLAYAGAIN_MENU)
            ret_val, exit_game = get_selection(int,0,1,"","Selection %d is not in range [%d, %d]")
            while not ret_val:
                menu(PLAYAGAIN_MENU)
                ret_val, exit_game = get_selection(int,0,1,"","Selection %d is not in range [%d, %d]")

main()