import random
from collections import Counter

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


class MonsterManager:
    def __init__(self, party_rolls, dungeon_rolls):
        self.party_rolls = party_rolls
        self.dungeon_rolls = dungeon_rolls
        self.dragon_pile = 0
        self.defeated_monsters = {
            'Goblin': 0,
            'Skeleton': 0,
            'Ooze': 0,
            'Dragon': 0
        }
    
    def count_monsters(self):
        return Counter(self.dungeon_rolls)
    
    def defeat_monsters(self):
        """
        Attempt to defeat monsters based on party composition.
        
        Returns:
            bool: True if monsters can be defeated, False otherwise
        """
        # Count available heroes and monsters
        hero_counts = Counter(h for h in self.party_rolls if h != 'Scroll')
        monster_counts = self.count_monsters()
        
        # Track which monsters we've attempted to defeat
        monsters_to_defeat = monster_counts.copy()
        
        # Track used heroes
        used_heroes = Counter()
        
        # Dragon handling
        dragon_count = monster_counts['Dragon']
        if dragon_count > 0:
            self.dragon_pile += dragon_count
            del monsters_to_defeat['Dragon']
        
        # Monster defeat rules
        defeat_rules = {
            'Fighter': {'Skeleton': 1, 'Ooze': 1, 'Goblin': float('inf')},
            'Cleric': {'Goblin': 1, 'Ooze': 1, 'Skeleton': float('inf')},
            'Mage': {'Goblin': 1, 'Skeleton': 1, 'Ooze': float('inf')},
            'Thief': {'Goblin': 1, 'Skeleton': 1, 'Ooze': 1},
            'Champion': {'Goblin': float('inf'), 'Skeleton': float('inf'), 'Ooze': float('inf')}
        }
        
        # Attempt to defeat monsters
        for hero_type, hero_count in hero_counts.items():
            for monster_type, monster_count in list(monsters_to_defeat.items()):
                if monster_type == 'Potion' or monster_type == 'Treasure':
                    del monsters_to_defeat[monster_type]
                    continue
                
                # Check if this hero type can defeat the monster
                if monster_type in defeat_rules[hero_type]:
                    max_defeat = defeat_rules[hero_type][monster_type]
                    
                    # Determine how many monsters can be defeated
                    defeated = min(monster_count, max_defeat * hero_count)
                    
                    # Update monster counts and used heroes
                    monsters_to_defeat[monster_type] -= defeated
                    used_heroes[hero_type] += (defeated / max_defeat)
                    
                    # Remove monster type if all defeated
                    if monsters_to_defeat[monster_type] <= 0:
                        del monsters_to_defeat[monster_type]
        
        # Check if all monsters are defeated
        return len(monsters_to_defeat) == 0
    
    def handle_dragon(self):
        """
        Attempt to defeat the dragon when 3 dragon dice are collected.
        
        Returns:
            bool: True if dragon is defeated, False otherwise
        """
        if self.dragon_pile >= 3:
            # Check if there are at least 3 different hero types
            hero_types = set(h for h in self.party_rolls if h != 'Scroll')
            return len(hero_types) >= 3
        return False


class DungeonDice:
    MONSTER_TYPES = ['Goblin', 'Skeleton', 'Ooze', 'Dragon', 'Potion', 'Treasure']
    
    def __init__(self):
        self.current_level = 0
        self.current_rolls = []
        self.dungeon_state = {
            'current_level': 0,
            'monsters_defeated': 0,
            'potions_found': 0,
            'treasures_collected': 0,
            'total_monsters': 0,
            'dragon_pile': 0
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
    def choose_action(party_rolls, dungeon_rolls):
        """
        Prompt the player for their next action at the end of a turn.
        
        Args:
            party_rolls (list): Rolls for the party dice
            dungeon_rolls (list): Rolls for the dungeon dice
        
        Returns:
            str: The player's chosen action
        """
        # Create monster manager to check if monsters can be defeated
        monster_manager = MonsterManager(party_rolls, dungeon_rolls)
        
        while True:
            print("\n--- Turn Options ---")
            
            # Check if monsters can be defeated
            if monster_manager.defeat_monsters():
                print("1. Continue to next level")
            else:
                print("1. CANNOT CONTINUE (Monsters not defeated)")
            
            print("2. Use a potion")
            print("3. Check party status")
            print("4. Flee the dungeon")
            
            # Check for dragon
            if monster_manager.dragon_pile >= 3:
                print("5. FIGHT THE DRAGON")
            
            choice = input("Enter your choice: ").strip()
            
            # Validate choice based on monster defeat status
            if choice == '1' and not monster_manager.defeat_monsters():
                print("Cannot continue. Defeat the monsters first!")
                continue
            
            if choice in ['1', '2', '3', '4'] or (choice == '5' and monster_manager.dragon_pile >= 3):
                actions = {
                    '1': "Continue to next level",
                    '2': "Use a potion",
                    '3': "Check party status",
                    '4': "Flee the dungeon",
                    '5': "Fight the dragon"
                }
                print(f"You chose: {actions[choice]}")
                return choice
            else:
                print("Invalid choice. Please enter a valid option.")


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
            
            # Player chooses action after each turn
            player_choice = PlayerTurn.choose_action(party_rolls, dungeon_rolls)
            
            # Basic action handling (can be expanded)
            if player_choice == '4':
                print("You have chosen to flee the dungeon!")
                return
    
    print("\n=== DUNGEON ADVENTURE COMPLETE ===")


def main():
    play_dungeon_game()


if __name__ == "__main__":
    main()