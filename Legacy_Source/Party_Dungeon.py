import random

class PartyDice:
    HERO_TYPES = ['Fighter', 'Cleric', 'Mage', 'Thief', 'Champion', 'Scroll']
    
    @classmethod
    def roll_party_dice(cls, num_dice=7):
        return [random.choice(cls.HERO_TYPES) for _ in range(num_dice)]
    
    @classmethod
    def count_party_composition(cls, rolls):
        return {hero: rolls.count(hero) for hero in cls.HERO_TYPES}
    
    @classmethod
    def print_roll_results(cls, rolls):
        print("Party Dice Roll Results:")
        print("-" * 25)
        
        for i, roll in enumerate(rolls, 1):
            print(f"Die {i}: {roll}")
        
        print("\nParty Composition:")
        print("-" * 25)
        
        composition = cls.count_party_composition(rolls)
        for hero, count in composition.items():
            if count > 0:
                print(f"{hero}: {count}")


class DungeonDice:
    MONSTER_TYPES = ['Goblin', 'Skeleton', 'Orc', 'Dragon', 'Potion', 'Treasure']
    
    def __init__(self):
        self.current_level = 0
        self.current_rolls = []
        self.dungeon_state = {
            'current_level': 0,
            'monsters_defeated': 0,
            'potions_found': 0,
            'treasures_collected': 0,
            'total_monsters': 0
        }
    
    def roll_dungeon_dice(self, current_level):
        """
        Roll dungeon dice based on the current dungeon level and update state.
        """
        if current_level < 1 or current_level > 10:
            raise ValueError("Dungeon level must be between 1 and 10")
        
        self.current_level = current_level
        self.current_rolls = [random.choice(self.MONSTER_TYPES) for _ in range(current_level)]
        
        # Update dungeon state
        self.dungeon_state['current_level'] = current_level
        self.dungeon_state['total_monsters'] = current_level
        self.dungeon_state['monsters_defeated'] = 0
        self.dungeon_state['potions_found'] = self.current_rolls.count('Potion')
        self.dungeon_state['treasures_collected'] = self.current_rolls.count('Treasure')
        
        return self.current_rolls
    
    def count_dungeon_composition(self):
        """
        Count the number of each monster type, potions, and treasures.
        """
        return {monster: self.current_rolls.count(monster) for monster in self.MONSTER_TYPES}
    
    def print_dungeon_roll_results(self):
        """
        Print the results of the dungeon dice rolls and current dungeon state.
        """
        print(f"\nDungeon Level {self.current_level} Dice Roll Results:")
        print("-" * 35)
        
        # Print individual dice results
        for i, roll in enumerate(self.current_rolls, 1):
            print(f"Die {i}: {roll}")
        
        print("\nDungeon Composition:")
        print("-" * 25)
        
        # Print composition counts
        composition = self.count_dungeon_composition()
        for monster, count in composition.items():
            if count > 0:
                print(f"{monster}: {count}")
        
        print("\nCurrent Dungeon State:")
        print("-" * 25)
        for key, value in self.dungeon_state.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

class PlayerTurn:
    @staticmethod
    def choose_action():
        """
        Prompt the player for their next action at the end of a turn.
        
        Returns:
            str: The player's chosen action
        """
        while True:
            print("\n--- Turn Options ---")
            print("1. Continue to next level")
            print("2. Use a potion")
            print("3. Check party status")
            print("4. Flee the dungeon")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice in ['1', '2', '3', '4']:
                actions = {
                    '1': "Continue to next level",
                    '2': "Use a potion",
                    '3': "Check party status",
                    '4': "Flee the dungeon"
                }
                print(f"You chose: {actions[choice]}")
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

def play_dungeon_game():
    """
    Simulate a full dungeon game with 3 rounds.
    """
    print("=== DUNGEON ADVENTURE BEGINS ===")
    
    # Roll initial party dice
    party_rolls = PartyDice.roll_party_dice()
    PartyDice.print_roll_results(party_rolls)
    
    # Initialize dungeon dice
    dungeon_dice = DungeonDice()
    
    # Play 3 rounds
    for round_num in range(1, 4):
        print(f"\n--- ROUND {round_num} ---")
        
        # Play through 10 levels in this round
        for level in range(1, 11):
            print(f"\nEntering Dungeon Level {level}")
            
            # Roll dungeon dice for this level
            dungeon_rolls = dungeon_dice.roll_dungeon_dice(level)
            dungeon_dice.print_dungeon_roll_results()
    
    print("\n=== DUNGEON ADVENTURE COMPLETE ===")


def main():
    play_dungeon_game()


if __name__ == "__main__":
    main()