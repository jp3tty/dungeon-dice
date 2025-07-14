from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from treasure import TreasureActions, TreasureType
from dungeon_dice_game import clear_screen

class DragonPhase:
    @staticmethod
    def execute(game_state, hero_card):
        """Execute the Dragon Phase."""
        clear_screen()
        if len(game_state.dragons_lair) < 3:
            print("\n--- DRAGON PHASE ---")
            print("Not enough dragons in the lair to attract attention. Proceeding to Regroup Phase...")
            return True
            
        print("\n--- DRAGON PHASE ---")
        print("The Dragon has arrived! You must do battle!")
        print(f"There are {len(game_state.dragons_lair)} dice in the Dragon's Lair.")
        
        while True:
            print("\nDragon Phase Actions:")
            print("1) Battle the Dragon")
            print("2) Use Treasure")
            print("3) Flee from the Dragon")
            
            choice = input("Choose action (number): ").strip()
            
            if choice == "1":
                if DragonPhase.battle_dragon(game_state):
                    return True
            elif choice == "2":
                result = TreasureActions.use_treasure(game_state)
                if result == "END_DELVE":
                    return False
                elif not game_state.dragons_lair:  # Ring of Invisibility was used
                    print("The Dragon has vanished! Proceeding to Regroup Phase...")
                    return True
            elif choice == "3":
                print("You flee from the Dragon!")
                return False
            else:
                print("Invalid choice. Please enter a number 1-3.")
    
    @staticmethod
    def battle_dragon(game_state):
        """Battle the Dragon using companions and treasures."""
        clear_screen()
        # Display current party state
        print("\nYour Active Party and Treasures:")
        companions = []
        
        # Add party dice
        for i, die in enumerate(game_state.party_dice):
            companions.append(("party", i, die))
            print(f"{len(companions)}. Party Die: {die}")
        
        # Add usable treasure companions
        treasure_companions = game_state.get_usable_companions()
        for i, (idx, token) in enumerate(treasure_companions):
            companions.append(("treasure", idx, token))
            print(f"{len(companions)}. Treasure: {token.name} (acts as {token.get_companion_type()})")
        
        if not companions:
            print("No companions available to battle the Dragon!")
            return False
        
        print("\nYou must use exactly 3 different types of Companions to battle the Dragon.")
        print("Select your companions one at a time:")
        
        selected_companions = []
        selected_indices = []
        used_types = set()
        
        for i in range(3):
            print(f"\nSelecting Companion {i+1}/3:")
            # Show available companions that haven't been selected yet
            available_companions = []
            for idx, (source, orig_idx, companion) in enumerate(companions):
                if idx not in selected_indices:
                    companion_type = companion.get_companion_type() if source == "treasure" else companion
                    if companion_type not in used_types:
                        available_companions.append((idx, source, orig_idx, companion, companion_type))
                        print(f"{len(available_companions)}. {'Treasure: ' if source == 'treasure' else ''}"
                              f"{companion.name if source == 'treasure' else companion}")
            
            if not available_companions:
                print("Not enough different companion types to battle the Dragon!")
                print("You must flee the dungeon!")
                return False
            
            print(f"{len(available_companions)+1}. Cancel selection")
            
            choice = input("Choose companion (number): ").strip()
            try:
                choice_idx = int(choice) - 1
                if choice_idx == len(available_companions):
                    print("Selection cancelled. You must flee!")
                    return False
                if 0 <= choice_idx < len(available_companions):
                    idx, source, orig_idx, companion, companion_type = available_companions[choice_idx]
                    selected_companions.append((source, orig_idx, companion))
                    selected_indices.append(idx)
                    used_types.add(companion_type)
                    print(f"Selected {companion.name if source == 'treasure' else companion}!")
                else:
                    print("Invalid choice. You must flee!")
                    return False
            except ValueError:
                print("Invalid input. You must flee!")
                return False
        
        # Use all selected companions
        print("\nYour party confronts the Dragon!")
        for source, idx, companion in selected_companions:
            if source == "party":
                game_state.use_party_die(idx)
                print(f"{companion} moved to Graveyard.")
            else:  # treasure
                game_state.use_treasure(idx)
                print(f"{companion.name} used and returned to treasure pool.")
        
        # Victory!
        print("Victory! The Dragon is defeated!")
        
        # Return Dragon dice to available pool
        dragon_count = len(game_state.dragons_lair)
        game_state.dragons_lair = []
        print(f"{dragon_count} Dragon dice returned to the available pool.")
        
        # Claim rewards
        game_state.treasure_tokens += 1
        game_state.experience_tokens += 1
        print("You claim the Dragon's hoard: 1 Treasure token")
        print("You gain 1 Experience token for your bravery!")
        
        # Draw treasure token
        token = game_state.draw_treasure()
        if token:
            print(f"You found: {token.name}")
            print(f"Effect: {token.get_description()}")
        
        return True 