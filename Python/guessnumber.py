# ============================================
#   🎲 Number Guessing Game - Python Learning
# ============================================
# Concepts covered:
#   ✅ Random module     ✅ While loops
#   ✅ If/else logic     ✅ Functions
#   ✅ Input validation  ✅ Score tracking

import random


def get_difficulty():
    """Let the player choose a difficulty level"""
    print("\n🎯 Choose your difficulty:")
    print("  1. 🟢 Easy   - Guess 1 to 10   (10 attempts)")
    print("  2. 🟡 Medium - Guess 1 to 50   (7 attempts)")
    print("  3. 🔴 Hard   - Guess 1 to 100  (5 attempts)")

    levels = {
        "1": ("Easy",   10,  10),
        "2": ("Medium", 50,  7),
        "3": ("Hard",   100, 5),
    }

    while True:
        choice = input("\n👉 Enter 1, 2, or 3: ").strip()
        if choice in levels:
            return levels[choice]
        print("⚠️  Invalid choice! Please enter 1, 2, or 3.")


def get_guess(low, high):
    """Safely get a valid guess from the player"""
    while True:
        try:
            guess = int(input(f"\n🤔 Your guess ({low}-{high}): "))
            if low <= guess <= high:
                return guess
            print(f"⚠️  Please enter a number between {low} and {high}.")
        except ValueError:
            print("⚠️  That's not a number! Try again.")


def give_hint(guess, secret, attempts_left):
    """Give a helpful hint based on how close the guess is"""
    diff = abs(guess - secret)

    if diff == 0:
        return ""
    elif diff <= 2:
        warmth = "🔥 SUPER HOT!"
    elif diff <= 5:
        warmth = "♨️  Very warm!"
    elif diff <= 10:
        warmth = "🌤  Getting warm..."
    elif diff <= 20:
        warmth = "❄️  Cold..."
    else:
        warmth = "🧊 Freezing!"

    direction = "⬆️  Go HIGHER!" if guess < secret else "⬇️  Go LOWER!"
    return f"  {direction}  {warmth}  (Attempts left: {attempts_left})"


def play_game(scores):
    """Main game logic"""
    level_name, max_number, max_attempts = get_difficulty()
    secret = random.randint(1, max_number)
    attempts = 0

    print(f"\n{'='*45}")
    print(f"  🎲 {level_name} Mode! Guess a number between 1 and {max_number}")
    print(f"  You have {max_attempts} attempts. Good luck! 🍀")
    print(f"{'='*45}")

    while attempts < max_attempts:
        attempts_left = max_attempts - attempts
        guess = get_guess(1, max_number)
        attempts += 1

        if guess == secret:
            score = round((max_attempts - attempts + 1) / max_attempts * 100)
            print(f"\n🎉 CORRECT! The number was {secret}!")
            print(f"🏆 You got it in {attempts} attempt(s)!")
            print(f"⭐ Score: {score} points")
            scores.append(score)
            return True
        else:
            hint = give_hint(guess, secret, attempts_left - 1)
            print(hint)

    print(f"\n😢 Out of attempts! The secret number was {secret}.")
    scores.append(0)
    return False


def show_scoreboard(scores):
    """Display the player's score history"""
    if not scores:
        print("\n📋 No games played yet.")
        return
    print("\n📊 --- SCOREBOARD ---")
    for i, s in enumerate(scores, 1):
        bar = "⭐" * (s // 10)
        print(f"  Game {i}: {s:>3} pts  {bar}")
    print(f"  🏅 Best score : {max(scores)} pts")
    print(f"  📈 Average    : {sum(scores) // len(scores)} pts")


def main():
    print("\n" + "="*45)
    print("   🎲  WELCOME TO THE NUMBER GUESSING GAME")
    print("="*45)
    print("  Can you guess the secret number?")

    scores = []

    while True:
        print("\n📋 MAIN MENU")
        print("  1. 🎮 Play Game")
        print("  2. 📊 View Scoreboard")
        print("  3. 🚪 Exit")

        choice = input("\n👉 Enter 1, 2, or 3: ").strip()

        if choice == "1":
            play_game(scores)
        elif choice == "2":
            show_scoreboard(scores)
        elif choice == "3":
            show_scoreboard(scores)
            print("\n👋 Thanks for playing! Keep learning Python! 🐍\n")
            break
        else:
            print("⚠️  Invalid choice!")


# --- Entry point ---
if __name__ == "__main__":
    main()