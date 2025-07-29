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
        
        # Check if we can use scrolls during the battle
        scrolls_available = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.SCROLL.value]
        
        # Display current party state
        print("\nYour Active Party and Treasures:")
        companions = []
        
        # Add party dice (excluding scrolls and champions)
        for i, die in enumerate(game_state.party_dice):
            if die != PartyDiceFace.SCROLL.value and die != PartyDiceFace.CHAMPION.value:  # Scrolls and Champions are not companions for dragon battles
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
        
        # Option to use scrolls before selecting companions
        if scrolls_available:
            print(f"\nYou have {len(scrolls_available)} Scroll(s) available during the dragon battle.")
            use_scroll = input("Would you like to use a Scroll to re-roll dice before selecting companions? (y/n): ").strip().lower()
            if use_scroll == 'y':
                DragonPhase.use_scroll_during_battle(game_state)
        
        print("\nYou must use exactly 3 different types of Companions to battle the Dragon.")
        print("(Scrolls and Champions are not companions and cannot be used to defeat the dragon)")
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
                # Find the actual die in the current party dice list and remove it
                if companion in game_state.party_dice:
                    die_idx = game_state.party_dice.index(companion)
                    game_state.use_party_die(die_idx)
                    print(f"{companion} moved to Graveyard.")
                else:
                    print(f"Warning: {companion} not found in party dice!")
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
    
    @staticmethod
    def use_scroll_during_battle(game_state):
        """Use a Scroll to re-roll dice during dragon battle."""
        scroll_indices = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.SCROLL.value]
        
        if not scroll_indices:
            print("No Scrolls available!")
            return
        
        # Select a scroll to use
        if len(scroll_indices) == 1:
            scroll_idx = scroll_indices[0]
        else:
            print("Select which Scroll to use:")
            for i, idx in enumerate(scroll_indices):
                print(f"{i+1}. Scroll at position {idx+1}")
            choice = input("Choose a Scroll (number): ").strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(scroll_indices):
                    scroll_idx = scroll_indices[choice_idx]
                else:
                    print("Invalid choice.")
                    return
            except ValueError:
                print("Invalid input.")
                return
        
        # Move scroll to graveyard
        game_state.use_party_die(scroll_idx)
        print("Used a Scroll! Select dice to re-roll (results will be random).")
        
        # Create a list of all available dice to re-roll
        print("\nAvailable Dice to Re-roll:")
        print("=== Dungeon Dice (excluding Dragon dice) ===")
        reroll_options = []
        # Add dungeon dice (excluding dragon dice)
        for i, die in enumerate(game_state.dungeon_dice):
            reroll_options.append(("dungeon", i, die))
            print(f"{len(reroll_options)}. Dungeon Die: {die}")
        
        print("\n=== Party Dice ===")
        # Add party dice (excluding the scroll we just used)
        for i, die in enumerate(game_state.party_dice):
            if i != scroll_idx:  # Don't show the scroll we just used
                reroll_options.append(("party", i, die))
                print(f"{len(reroll_options)}. Party Die: {die}")
        
        # Select dice to re-roll
        while True:
            reroll_input = input("\nEnter numbers of dice to re-roll (comma-separated, e.g. '1,3,5') or 'none': ").strip()
            
            if reroll_input.lower() == 'none':
                print("No dice re-rolled.")
                return
            
            try:
                reroll_indices = [int(idx.strip()) - 1 for idx in reroll_input.split(',')]
                # Validate indices
                if all(0 <= idx < len(reroll_options) for idx in reroll_indices):
                    # Group the re-rolls by type
                    dungeon_rerolls = []
                    party_rerolls = []
                    
                    for idx in reroll_indices:
                        die_type, original_idx, die_face = reroll_options[idx]
                        if die_type == "dungeon":
                            dungeon_rerolls.append(original_idx)
                        else:  # party
                            party_rerolls.append(original_idx)
                    
                    # Re-roll dungeon dice
                    dice_manager = DiceManager()
                    for idx in sorted(dungeon_rerolls, reverse=True):
                        removed_die = game_state.dungeon_dice.pop(idx)
                        print(f"\nRe-rolling Dungeon Die {removed_die}...")
                        new_die = dice_manager.roll_dungeon_dice(1)[0]
                        if new_die == DungeonDiceFace.DRAGON.value:
                            game_state.dragons_lair.append(new_die)
                            print(f"Rolled a Dragon! It goes to the Dragon's Lair.")
                        else:
                            game_state.dungeon_dice.append(new_die)
                            print(f"Rolled a {new_die}!")
                    
                    # Re-roll party dice
                    for idx in sorted(party_rerolls, reverse=True):
                        removed_die = game_state.party_dice.pop(idx)
                        print(f"\nRe-rolling Party Die {removed_die}...")
                        new_die = dice_manager.roll_party_dice(1)[0]
                        game_state.party_dice.append(new_die)
                        print(f"Rolled a {new_die}!")
                    
                    # Show final results
                    if game_state.dungeon_dice:
                        print("\nFinal Dungeon Dice:")
                        for i, die in enumerate(game_state.dungeon_dice, 1):
                            print(f"{i}. {die}")
                    
                    print("\nFinal Party Dice:")
                    for i, die in enumerate(game_state.party_dice, 1):
                        print(f"{i}. {die}")
                    
                    return
                else:
                    print("Some indices are out of range. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
            except IndexError:
                print("Invalid selection. Please try again.") 