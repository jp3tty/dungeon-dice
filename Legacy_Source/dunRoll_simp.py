import random

def roll_dice(sides=6):
    """Rolls a dice with the specified number of sides."""
    return random.randint(1, sides)

def dungeon_roll():
    """Simulates a dungeon roll."""

    print("Rolling the dice...")
    result = roll_dice(20)

    if result == 1:
        print("Critical failure! You fall into a pit.")
    elif result <= 5:
        print("Failure! You encounter a trap.")
    elif result <= 10:
        print("Partial success. You find a small treasure.")
    elif result <= 15:
        print("Success! You defeat a monster.")
    elif result <= 19:
        print("Great success! You discover a secret passage.")
    else:
        print("Critical success! You find a legendary artifact.")

if __name__ == "__main__":
    dungeon_roll()