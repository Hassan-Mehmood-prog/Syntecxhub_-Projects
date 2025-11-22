
from colorama import init as colorama_init, Fore, Back, Style
import math
import sys
import os

# Initialize colorama (makes ANSI colors work on Windows)
colorama_init(autoreset=True)

# ---------- Calculation functions (pure/testable) ----------
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


# Optional helper to parse numeric input (keeps calculate() cleaner)
def parse_number(s: str) -> float:
    """
    Parse a string into float (accepts ints and floats).
    Raises ValueError on invalid input.
    """
    s = s.strip()
    # Allow leading + sign
    if s.startswith('+'):
        s = s[1:]
    # Use float conversion (will raise ValueError if invalid)
    return float(s)


# ---------- UI / Utility helpers ----------
def clear_terminal():
    """Clear terminal screen in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')


def styled(text: str, *, fg=None, bg=None, bold=False) -> str:
    """Return styled text using colorama presets."""
    parts = []
    if fg:
        parts.append(fg)
    if bg:
        parts.append(bg)
    if bold:
        parts.append(Style.BRIGHT)
    parts.append(str(text))
    parts.append(Style.RESET_ALL)
    return ''.join(parts)


def header():
    print(styled("=" * 40, fg=Fore.CYAN))
    print(styled("  STYLED SIMPLE CALCULATOR", fg=Fore.CYAN, bold=True))
    print(styled("=" * 40, fg=Fore.CYAN))


def print_menu():
    print()
    print(styled("Menu:", fg=Fore.MAGENTA, bold=True))
    print(styled("  1) Calculate", fg=Fore.YELLOW))
    print(styled("  2) Clear Screen", fg=Fore.YELLOW))
    print(styled("  3) Exit", fg=Fore.YELLOW))
    print()


# ---------- Main calculation flow ----------
def perform_calculation():
    """
    Interactively gets input from the user, validates it, performs operation, and prints styled result.
    Separated logic (parse_number + operation functions) so unit tests can import them.
    """
    try:
        raw_a = input(styled("Enter first number: ", fg=Fore.GREEN, bold=True))
        a = parse_number(raw_a)
    except ValueError:
        print(styled("Invalid number for first input. Try again.", fg=Fore.RED))
        return

    op = input(styled("Enter operator (+, -, *, /) or 'clear': ", fg=Fore.GREEN, bold=True)).strip()

    if op.lower() == "clear":
        # user wants to clear without continuing calculation
        print(styled("Cleared — returning to menu.", fg=Fore.CYAN))
        return

    if op not in {"+", "-", "*", "/"}:
        print(styled(f"Invalid operator '{op}'. Allowed: + - * /", fg=Fore.RED))
        return

    try:
        raw_b = input(styled("Enter second number: ", fg=Fore.GREEN, bold=True))
        b = parse_number(raw_b)
    except ValueError:
        print(styled("Invalid number for second input. Try again.", fg=Fore.RED))
        return

    # Map operator to function
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    func = operations.get(op)
    try:
        result = func(a, b)
    except ZeroDivisionError as zde:
        print(styled(str(zde), fg=Fore.RED, bold=True))
        return

    print(styled(f"Result: {a} {op} {b} = {result}", fg=Fore.GREEN, bold=True))


def main():
    while True:
        clear_terminal()
        header()
        print_menu()
        choice = input(styled("Choose an option (1-3): ", fg=Fore.CYAN, bold=True)).strip()

        if choice == "1":
            perform_calculation()
            input(styled("\nPress Enter to continue...", fg=Fore.MAGENTA))
        elif choice == "2":
            clear_terminal()
        elif choice == "3":
            print(styled("Goodbye!", fg=Fore.CYAN))
            break
        else:
            print(styled("Invalid choice. Please select 1, 2 or 3.", fg=Fore.RED))
            input(styled("\nPress Enter to continue...", fg=Fore.MAGENTA))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + styled('Exiting (keyboard interrupt).', fg=Fore.CYAN))
