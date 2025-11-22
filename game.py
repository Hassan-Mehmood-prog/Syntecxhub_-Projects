import random
import time

# Make playsound optional so the game can run without the package installed.
try:
    from playsound import playsound
except Exception:
    # fallback - no-op playsound
    def playsound(file):
        return None

# Make colorama optional; provide simple fallbacks that don't crash if missing.
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except Exception:
    class _Fallback:
        def __getattr__(self, name):
            return ""

    Fore = _Fallback()
    Style = _Fallback()

class NumberGuessingGame:

    def __init__(self):
        self.best_score = None

    def play_sound(self, file):
        try:
            playsound(file)
        except:
            pass  # ignore sound errors if file missing

    def difficulty(self):
        print(Fore.CYAN + "\nSelect Difficulty Level:")
        print(Fore.YELLOW + "1. Easy (1-20)")
        print("2. Medium (1-50)")
        print("3. Hard (1-100)")

        while True:
            choice = input(Fore.GREEN + "Enter choice (1/2/3): ")

            if choice == "1":
                return 20
            elif choice == "2":
                return 50
            elif choice == "3":
                return 100
            else:
                print(Fore.RED + "Invalid choice! Try again.")

    def start_game(self):
        limit = self.difficulty()
        number = random.randint(1, limit)
        attempts = 0

        print(Fore.MAGENTA + f"\nGuess the number between 1 and {limit}!")
        print(Fore.CYAN + "--------------------------------------")

        while True:
            try:
                guess = int(input(Fore.GREEN + "\nEnter your guess: "))
                attempts += 1

                if guess < number:
                    print(Fore.YELLOW + "Too low!")
                    self.play_sound("sounds/wrong.wav")

                elif guess > number:
                    print(Fore.YELLOW + "Too high!")
                    self.play_sound("sounds/wrong.wav")

                else:
                    print(Fore.GREEN + f"\n🎉 Correct! You guessed it in {attempts} attempts!")
                    self.play_sound("sounds/correct.wav")
                    return attempts

            except ValueError:
                print(Fore.RED + "Invalid input! Enter a number.")

    def show_best_score(self):
        if self.best_score is None:
            print(Fore.BLUE + "No best score yet — play the game!")
        else:
            print(Fore.BLUE + f"🔥 Best Score: {self.best_score} attempts")

    def start(self):
        while True:
            print(Fore.CYAN + "\n===== NUMBER GUESSING GAME =====")
            print("1. Start New Game")
            print("2. Show Best Score")
            print("3. Exit")

            choice = input(Fore.GREEN + "\nEnter your choice: ")

            if choice == "1":
                attempts = self.start_game()

                if self.best_score is None or attempts < self.best_score:
                    self.best_score = attempts
                    print(Fore.GREEN + "🎯 New Best Score!")
                
                time.sleep(1)

            elif choice == "2":
                self.show_best_score()

            elif choice == "3":
                print(Fore.MAGENTA + "\nThanks for playing!")
                break

            else:
                print(Fore.RED + "Invalid choice! Try again.\n")
