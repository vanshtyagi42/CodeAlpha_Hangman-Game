"""
              HANGMAN GAME - Professional Edition         
"""

import random
import os
import sys

#  CONSTANTS & CONFIGURATION

MAX_WRONG_GUESSES = 6

WORD_LIST = [
    "python",
    "algorithm",
    "program",
    "game",
    "fun"]

HANGMAN_STAGES = [
    """
      STAGE: 0 (ERROR - 0/6)
    """,
    """
     STAGE: 1 (ERROR - 1/6)
    """,
    """
    STAGE: 2 (ERROR - 2/6)
    """,
    """
    STAGE: 3 (ERROR - 3/6)
    """,
    """
    STAGE: 4 (ERROR - 4/6)
    """,
    """
    STAGE: 5 (ERROR - 5/6)
    """,
    """
    STAGE: 6 - OVER (6/6)
    """,
]
    
# Hangman stages (0 = safe ... 6 = dead)

#  UTILITY FUNCTIONS

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_header():
    print("          H A N G M A N - G A M E         ")
    print("           Professional Edition        ")
    print('\n')

def display_hangman(wrong_count: int):
    print(HANGMAN_STAGES[wrong_count])

def display_word(secret_word: str, guessed_letters: set) -> str:
    masked = []
    for letter in secret_word:
        if letter in guessed_letters:
            masked.append(f"{letter}")  # Green for correct
        else:
            masked.append("_")
    display = "  ".join(masked)
    print(f"\n  Word:  {display}\n")
    return display

def display_status(wrong_guesses: list, guessed_letters: set):
    remaining = MAX_WRONG_GUESSES - len(wrong_guesses)

    print(f"  Wrong guesses  : {', '.join(wrong_guesses) if wrong_guesses else 'None'}")
    print(f"  Lives remaining: {remaining}/{MAX_WRONG_GUESSES}")
    print(f"  All guessed    : {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
    print()

def get_player_guess(guessed_letters: set) -> str:
    
    while True:
        try:
            guess = input("  Enter a letter: ").strip().lower()

            if len(guess) != 1:
                print("  Please enter exactly ONE letter")
                continue
            if not guess.isalpha():
                print("  Only alphabetic characters allowed")
                continue
            if guess in guessed_letters:
                print(f"  '{guess}' was already guessed! Try a new one")
                continue

            return guess

        except (EOFError, KeyboardInterrupt):
            print("\n\n     Game interrupted. Goodbye!     \n")
            sys.exit(0)


def check_win(secret_word: str, guessed_letters: set) -> bool:
    
    return all(letter in guessed_letters for letter in secret_word)


def display_result(won: bool, secret_word: str, wrong_count: int):
    print()
    if won:
        print("    C O N G R A T U L A T I O N S    ")
        print(f"  You guessed the word: \"{secret_word.upper()}\"")
        print(f"  Wrong guesses made  : {wrong_count}/{MAX_WRONG_GUESSES}")
        accuracy = round(((MAX_WRONG_GUESSES - wrong_count) / MAX_WRONG_GUESSES) * 100)
        print(f"  Accuracy score      : {accuracy}%")
    else:
        print("    G A M E   O V E R    ")
        print(f"  The word was: \"{secret_word.upper()}\"")
        print("  Better luck next time")

def play_again() -> bool:
    while True:
        choice = input("    Play again? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("       Enter 'y' or 'n'   ")

#   GAME MAIN LOGIC

def run_game():
    secret_word = random.choice(WORD_LIST)   
    guessed_letters: set = set()             
    wrong_guesses: list = []                 

    while True: 
        clear_screen()
        display_header()
        display_hangman(len(wrong_guesses))
        display_word(secret_word, guessed_letters)
        display_status(wrong_guesses, guessed_letters)

        # Check win condition
        if check_win(secret_word, guessed_letters):
            display_result(won=True, secret_word=secret_word,
                           wrong_count=len(wrong_guesses))
            break

        # Check loss condition
        if len(wrong_guesses) >= MAX_WRONG_GUESSES:
            display_result(won=False, secret_word=secret_word,
                           wrong_count=len(wrong_guesses))
            break

        #Get and process guess
        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)           # strings + sets

        if guess in secret_word:             # if-else
            print(f"  '{guess}' is in the word!")
        else:
            wrong_guesses.append(guess)      # list append
            print(f"  '{guess}' is NOT in the word!")

        input("\n  Press ENTER to continue...")

#  ENTRY POINT

def main():
    clear_screen()
    display_header()
    print("  Welcome to Hangman — Professional Edition")
    print("  Guess the hidden word one letter at a time")
    print(f"  You have {MAX_WRONG_GUESSES} lives. Good luck!\n")
    input("  Press ENTER to start...")

    while True:
        run_game()
        if not play_again():
            clear_screen()
            print("\n     Thanks for playing!   \n")
            break


if __name__ == "__main__":
    main()
