from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from hero import HeroRank
from treasure import TreasureType
import random

class RegroupPhase:
    @staticmethod
    def execute(game_state, hero_card):
        """Execute the regroup phase."""
        print("\n" + "="*50)
        print("🔄 REGROUP PHASE 🔄".center(50))
        print("="*50)
        
        # Display current game state
        print("\nGame State:")
        print("Party Dice:")
        # Count dice types in the party
        dice_counts = {}
        for die in game_state.party_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
        
        # Add treasure companions to the party dice display
        treasure_companions = game_state.get_usable_companions()
        for idx, token in treasure_companions:
            companion_type = token.get_companion_type()
            dice_counts[companion_type] = dice_counts.get(companion_type, 0) + 1
        
        for die_type, count in dice_counts.items():
            print(f"- {die_type}: {count} dice")
        
        # Calculate total companions including treasure companions
        total_companions = len(game_state.party_dice) + len(treasure_companions)
        print(f"Total Companions: {total_companions}")
        print(f"Total Scrolls: {dice_counts.get('Scroll', 0)}")
        
        # Show treasure companions separately for clarity
        if treasure_companions:
            print("\nTreasure Companions:")
            for idx, token in treasure_companions:
                print(f"- {token.name} (acts as {token.get_companion_type()})")
        
        print("\nGraveyard:")
        if not game_state.graveyard:
            print("- Empty")
        else:
            # Count dice types in the graveyard
            graveyard_counts = {}
            for die in game_state.graveyard:
                graveyard_counts[die] = graveyard_counts.get(die, 0) + 1
            
            for die_type, count in graveyard_counts.items():
                print(f"- {die_type}: {count} dice")
        
        print("\nDungeon Dice:")
        # Count dungeon dice types
        dungeon_counts = {}
        for die in game_state.dungeon_dice:
            dungeon_counts[die] = dungeon_counts.get(die, 0) + 1
        
        monster_count = sum(count for die_type, count in dungeon_counts.items() 
                          if die_type in ['Goblin', 'Skeleton', 'Ooze', 'Dragon'])
        print(f"Total Monsters: {monster_count}")
        print(f"Total Chests: {dungeon_counts.get('Chest', 0)}")
        print(f"Total Potions: {dungeon_counts.get('Potion', 0)}")
        
        print(f"\n🐉 Dragon's Lair: {len(game_state.dragons_lair)} dragon dice")
        
        print(f"\n💎 Collected Treasures:")
        treasures = game_state.get_available_treasures()
        if treasures:
            for treasure in treasures:
                print(f"  ▫️ {treasure.name} - {treasure.get_description()}")
        else:
            print("  ▫️ None")
        
        print(f"\n📊 Resources:")
        print(f"  ▫️ Treasure Tokens: {game_state.treasure_tokens}")
        print(f"  ▫️ Experience Tokens: {game_state.experience_tokens}")
        
        print(f"\nCurrent Level: {game_state.level}\n")
        
        print("Choose your Regroup action:")
        print("1) Retire to the Tavern (End delve and gain Experience)")
        print("2) Seek Glory (Challenge the next dungeon level)")
        
        while True:
            try:
                choice = input("Choose action (number): ").strip()
                if choice == "1":
                    return RegroupPhase.retire_to_tavern(game_state, forced_retirement=False)
                elif choice == "2":
                    return RegroupPhase.seek_glory(game_state)
                else:
                    print("Invalid choice. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    @staticmethod
    def retire_to_tavern(game_state, forced_retirement):
        """End the delve and collect experience."""
        # Show congratulatory message and party status first
        print("\n" + "="*50)
        print("🎉 CONGRATULATIONS! THE DUNGEON HAS BEEN CLEARED! 🎉".center(50))
        print("="*50)
        
        print("\nFinal Party Status:")
        print("Active Party:")
        dice_counts = {}
        for die in game_state.party_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
        for die_face, count in dice_counts.items():
            print(f"- {die_face}: {count} dice")
        
        print("\nGraveyard:")
        if not game_state.graveyard:
            print("- Empty")
        else:
            # Count dice types in the graveyard
            graveyard_counts = {}
            for die in game_state.graveyard:
                graveyard_counts[die] = graveyard_counts.get(die, 0) + 1
            
            for die_type, count in graveyard_counts.items():
                print(f"- {die_type}: {count} dice")
        
        # Show available treasures
        print("\nAvailable Treasures:")
        treasures = game_state.get_available_treasures()
        if treasures:
            for treasure in treasures:
                print(f"- {treasure.name}")
                print(f"  Effect: {treasure.get_description()}")
        else:
            print("- None")
            
        print("\n" + "="*50)
        print("RETURNING TO TAVERN".center(50))
        print("="*50)
        
        if forced_retirement:
            print("\nLegendary retirement at level 10!")
            exp_gained = 10
        else:
            print("\nYou retire to the tavern, ending this delve.")
            exp_gained = game_state.level
            
        # Gain experience based on current level
        game_state.experience_tokens += exp_gained
        print(f"You gain {exp_gained} Experience tokens for reaching level {game_state.level}!")
        print(f"Total Experience tokens: {game_state.experience_tokens}")
        
        # Return all dungeon dice to available pool
        if game_state.dragons_lair:
            print(f"\nReturning {len(game_state.dragons_lair)} Dragon dice to the available pool.")
            game_state.dragons_lair = []
        
        # End this delve
        return False
    
    @staticmethod
    def seek_glory(game_state):
        """Continue to the next dungeon level."""
        # Increase dungeon level
        game_state.level += 1
        print(f"\nProceeding to dungeon level {game_state.level}...")
        
        # Calculate available dice
        total_dungeon_dice = 7  # Total dice in the game
        available_dice = total_dungeon_dice - len(game_state.dragons_lair)
        dice_to_roll = min(game_state.level, available_dice)
        
        print(f"\nWARNING! The Dungeon Lord will roll {dice_to_roll} Dungeon dice.")
        print("Once rolled, you must defeat all monsters and possibly the Dragon,")
        print("or you must Flee, gaining NO Experience for this delve!")
        print("There is no turning back once the Dungeon dice are cast!")
        
        proceed = input("\nDo you wish to proceed? (y/n): ").lower().strip()
        if proceed != 'y':
            print("Wise choice. You retire to the tavern.")
            return RegroupPhase.retire_to_tavern(game_state, forced_retirement=False)
        
        # Roll dungeon dice
        game_state.dungeon_dice = []  # Clear previous dice
        
        dice_manager = DiceManager()
        new_dice = dice_manager.roll_dungeon_dice(dice_to_roll)
        
        # Handle dragon dice separately
        for die in new_dice:
            if die == DungeonDiceFace.DRAGON.value:
                game_state.dragons_lair.append(die)
                print("A Dragon appears! The die moves to the Dragon's Lair.")
            else:
                game_state.dungeon_dice.append(die)
        
        if game_state.dragons_lair:
            print(f"\nDragon's Lair now contains {len(game_state.dragons_lair)} dice!")
        
        # Continue delving
        return True 