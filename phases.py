from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from hero import HeroRank
from treasure import TreasureType
import random

class TreasureActions:
    @staticmethod
    def use_treasure(game_state):
        """Handle using a treasure token."""
        treasures = game_state.get_available_treasures()
        if not treasures:
            print("No treasures available!")
            return False
            
        print("\nAvailable Treasures:")
        game_state.display_treasure_info()
        print(f"{len(treasures)+1}. Cancel")
        
        choice = input("Choose treasure to use (number): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(treasures):
                return False
            if 0 <= choice_idx < len(treasures):
                token = treasures[choice_idx]
                
                # Handle different treasure types
                if token.type == TreasureType.RING_OF_INVISIBILITY:
                    # Return dragons to pool without defeating them
                    dragon_count = len(game_state.dragons_lair)
                    game_state.dragons_lair = []
                    print(f"Ring of Invisibility used! {dragon_count} Dragon dice returned to pool.")
                    game_state.use_treasure(choice_idx)
                    return True
                    
                elif token.type == TreasureType.ELIXIR:
                    if not game_state.graveyard:
                        print("No dice in Graveyard to revive!")
                        return False
                    
                    print("\nChoose a die face for the revived Party die:")
                    for i, face in enumerate(PartyDiceFace):
                        print(f"{i+1}. {face.value}")
                    
                    face_choice = input("Choose face (number): ").strip()
                    try:
                        face_idx = int(face_choice) - 1
                        if 0 <= face_idx < len(PartyDiceFace):
                            # Remove a die from graveyard
                            game_state.graveyard.pop()
                            # Add new die with chosen face
                            chosen_face = list(PartyDiceFace)[face_idx].value
                            game_state.party_dice.append(chosen_face)
                            print(f"Elixir used! Added a {chosen_face} to your active party!")
                            game_state.use_treasure(choice_idx)
                            return True
                    except ValueError:
                        print("Invalid input.")
                        return False
                        
                elif token.type == TreasureType.DRAGON_BAIT:
                    # Transform all monsters into dragons
                    monster_count = 0
                    for i, die in enumerate(game_state.dungeon_dice):
                        if die in [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]:
                            game_state.dragons_lair.append(DungeonDiceFace.DRAGON.value)
                            monster_count += 1
                    
                    # Remove transformed monsters
                    game_state.dungeon_dice = [die for die in game_state.dungeon_dice 
                                             if die not in [DungeonDiceFace.GOBLIN.value, 
                                                          DungeonDiceFace.SKELETON.value, 
                                                          DungeonDiceFace.OOZE.value]]
                    
                    print(f"Dragon Bait used! {monster_count} monsters transformed into Dragons!")
                    game_state.use_treasure(choice_idx)
                    return True
                    
                elif token.type == TreasureType.TOWN_PORTAL:
                    # Gain experience equal to level and end delve
                    exp_gained = game_state.level
                    game_state.experience_tokens += exp_gained
                    print(f"Town Portal used! Gained {exp_gained} Experience tokens!")
                    game_state.use_treasure(choice_idx)
                    return "END_DELVE"
                    
                else:  # Companion-like treasures are handled in their respective phases
                    print("This treasure must be used during combat or specific phases.")
                    return False
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False

class MonsterPhase:
    @staticmethod
    def execute(game_state, hero_card):
        """Execute the Monster Phase."""
        print("\n" + "="*50)
        print("🗡️  MONSTER PHASE  🗡️".center(50))
        print("="*50)
        
        # Display current state
        MonsterPhase.print_state(game_state)
        hero_card.display_card_info()
        
        # Process monster encounters
        monsters = [die for die in game_state.dungeon_dice if die in 
                  [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
        
        if not monsters:
            print("\n🌟 Lucky! No monsters encountered in this phase! 🌟")
            return True
        
        print(f"\n⚔️  You've encountered {len(monsters)} fearsome monster(s)! ⚔️")
        
        # Phase actions
        while monsters and (game_state.party_dice or game_state.get_usable_companions()):
            print("\n📋 Available Monster Phase Actions:")
            print("🎲 A) Use a Scroll to re-roll dice")
            print("🤝 B) Use Companions to defeat monsters")
            print("💎 C) Use Treasure")
            print("⚡ D) Use Hero Ultimate Ability")
            
            choice = input("\nChoose action (letter): ").strip().upper()
            
            if choice == "A":
                if MonsterPhase.use_scroll(game_state):
                    # Update monster list as dice may have changed
                    monsters = [die for die in game_state.dungeon_dice if die in 
                              [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
                    MonsterPhase.print_state(game_state)
            elif choice == "B":
                # First show companion options
                print("\nChoose companion type to use:")
                print("1) Use a Champion (can defeat multiple monsters of same type)")
                print("2) Use other companions (Fighters, Clerics, Mages, Thieves)")
                print("3) Done using companions")
                sub_choice = input("Choose option (number): ").strip()
                
                if sub_choice == "1":
                    MonsterPhase.use_champion(game_state, monsters, hero_card, True)  # Always pass specialty_active as True
                elif sub_choice == "2":
                    MonsterPhase.use_companions(game_state, monsters, hero_card, True)  # Always pass specialty_active as True
                elif sub_choice == "3":
                    # Check if we can defeat remaining monsters
                    if monsters:
                        if MonsterPhase.can_defeat_monsters(game_state, monsters, hero_card, True):  # Always pass specialty_active as True
                            print("\nYour remaining party can defeat all monsters!")
                            print("Automatically using companions to defeat monsters...")
                            # Use companions to defeat remaining monsters
                            MonsterPhase.use_companions_for_remaining_monsters(game_state, monsters, hero_card, True)  # Always pass specialty_active as True
                            return True
                        else:
                            print("\nYou must flee the Dungeon! The monsters are too powerful!")
                            print("The delve is over immediately, and no experience (XP) is gained.")
                            return False
                    else:
                        print("All monsters have been defeated!")
                        return True
                else:
                    print("Invalid choice. Please choose 1, 2, or 3.")
                    continue
                
                # Update monster list
                monsters = [die for die in game_state.dungeon_dice if die in 
                          [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
                MonsterPhase.print_state(game_state)
            elif choice == "C":
                result = TreasureActions.use_treasure(game_state)
                if result == "END_DELVE":
                    return False
                # Update monster list after treasure use
                monsters = [die for die in game_state.dungeon_dice if die in 
                          [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
                MonsterPhase.print_state(game_state)
            elif choice == "D":
                # Use hero's ultimate ability
                if hero_card.use_ultimate(game_state):
                    # Update monster list after ultimate use
                    monsters = [die for die in game_state.dungeon_dice if die in 
                              [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
                    MonsterPhase.print_state(game_state)
            else:
                print("Invalid choice. Please enter a letter A-D.")
                continue
            
            # After each action, check if all monsters are defeated
            if not monsters:
                print("All monsters have been defeated!")
                return True
        
        # Final assessment - can all monsters be defeated?
        if not monsters:
            print("All monsters have been defeated!")
            return True
        else:
            if MonsterPhase.can_defeat_monsters(game_state, monsters, hero_card, True):  # Always pass specialty_active as True
                print("\nYour remaining party can defeat all monsters!")
                print("Automatically using companions to defeat monsters...")
                # Use companions to defeat remaining monsters
                MonsterPhase.use_companions_for_remaining_monsters(game_state, monsters, hero_card, True)  # Always pass specialty_active as True
                return True
            else:
                print("\nYou must flee the Dungeon! The monsters are too powerful!")
                print("The delve is over immediately, and no experience (XP) is gained.")
                return False
    
    @staticmethod
    def print_state(game_state):
        """Display the current state."""
        print("\n📊 Active Party Dice:")
        dice_counts = {}
        total_companions = 0
        for die in game_state.party_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
            if die != PartyDiceFace.SCROLL.value:  # Don't count scrolls as companions
                total_companions += 1
        for die_face, count in dice_counts.items():
            print(f"  ▫️ {die_face}: {count} dice")
        print(f"  Total Companions: {total_companions}")
        print(f"  Total Scrolls: {dice_counts.get(PartyDiceFace.SCROLL.value, 0)}")
        
        print("\n⚰️  Graveyard (Used Dice):")
        graveyard_counts = {}
        for die in game_state.graveyard:
            graveyard_counts[die] = graveyard_counts.get(die, 0) + 1
        if graveyard_counts:
            for die_face, count in graveyard_counts.items():
                print(f"  ▫️ {die_face}: {count} dice")
        else:
            print("  ▫️ Empty")
        
        print("\n🎲 Dungeon Encounter:")
        dungeon_counts = {}
        total_monsters = 0
        for die in game_state.dungeon_dice:
            dungeon_counts[die] = dungeon_counts.get(die, 0) + 1
            if die in [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]:
                total_monsters += 1
        for die_face, count in dungeon_counts.items():
            print(f"  ▫️ {die_face}: {count} dice")
        print(f"  Total Monsters: {total_monsters}")
        print(f"  Total Chests: {dungeon_counts.get(DungeonDiceFace.CHEST.value, 0)}")
        print(f"  Total Potions: {dungeon_counts.get(DungeonDiceFace.POTION.value, 0)}")
        
        if game_state.dragons_lair:
            print("\n🐉 Dragon's Lair:")
            print(f"  ▫️ Dragon: {len(game_state.dragons_lair)} dice")
    
    @staticmethod
    def use_scroll(game_state):
        """Use a Scroll to re-roll dice."""
        # Check if there are scrolls available
        scroll_indices = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.SCROLL.value]
        
        if not scroll_indices:
            print("No Scrolls available in your active party!")
            return False
        
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
                    return False
            except ValueError:
                print("Invalid input.")
                return False
        
        # Move scroll to graveyard
        game_state.use_party_die(scroll_idx)
        print("Used a Scroll! Select dice to re-roll (results will be random).")
        
        # Create a list of all available dice to re-roll
        print("\nAvailable Dice to Re-roll:")
        print("=== Dungeon Dice ===")
        reroll_options = []
        # Add dungeon dice
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
                return True
            
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
                    
                    return True
                else:
                    print("Some indices are out of range. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
            except IndexError:
                print("Invalid selection. Please try again.")
    
    @staticmethod
    def use_champion(game_state, monsters, hero_card, specialty_active):
        """Use a Champion to defeat monster(s)."""
        # Find champions in active party
        champion_indices = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.CHAMPION.value]
        
        if not champion_indices:
            print("No Champions available in your active party!")
            return False
        
        # Select a champion to use
        if len(champion_indices) == 1:
            champion_idx = champion_indices[0]
        else:
            print("Select which Champion to use:")
            for i, idx in enumerate(champion_indices):
                print(f"{i+1}. Champion at position {idx+1}")
            choice = input("Choose a Champion (number): ").strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(champion_indices):
                    champion_idx = champion_indices[choice_idx]
                else:
                    print("Invalid choice.")
                    return False
            except ValueError:
                print("Invalid input.")
                return False
        
        # Show monster type options
        print("\nChampion can defeat:")
        print("1. Any number of Goblins")
        print("2. Any number of Skeletons")
        print("3. Any number of Oozes")
        
        choice = input("Choose which type of monsters to defeat (1-3): ").strip()
        
        # Move champion to graveyard
        game_state.use_party_die(champion_idx)
        print(f"Champion moved to Graveyard.")
        
        if choice == "1":
            # Handle Goblins
            goblin_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.GOBLIN.value]
            if goblin_indices:
                print(f"\nChampion can defeat any number of Goblins!")
                if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                    print("Bard's specialty: Champion can defeat 1 extra monster!")
                print("Available Goblins:")
                for i, monster_idx in enumerate(goblin_indices):
                    print(f"{i+1}. Goblin at position {monster_idx+1}")
                
                # Ask how many Goblins to defeat
                while True:
                    num_goblins = input(f"How many Goblins to defeat (1-{len(goblin_indices)})? ").strip()
                    try:
                        num_goblins = min(len(goblin_indices), max(1, int(num_goblins)))
                        # If Bard's specialty is active, add 1 extra monster
                        if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                            num_goblins = min(len(goblin_indices), num_goblins + 1)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                
                # Remove Goblins (from highest index to lowest to avoid shifting issues)
                goblins_defeated = 0
                for monster_idx in sorted(goblin_indices[:num_goblins], reverse=True):
                    game_state.dungeon_dice.remove(DungeonDiceFace.GOBLIN.value)
                    monsters.pop(monster_idx)
                    goblins_defeated += 1
                
                print(f"{goblins_defeated} Goblin(s) defeated!")
                
                # Gain experience (1 per monster)
                game_state.experience_tokens += goblins_defeated
                print(f"Gained {goblins_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                return True
            else:
                print("No Goblins available for the Champion to defeat!")
                return False
                
        elif choice == "2":
            # Handle Skeletons
            skeleton_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.SKELETON.value]
            if skeleton_indices:
                print(f"\nChampion can defeat any number of Skeletons!")
                if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                    print("Bard's specialty: Champion can defeat 1 extra monster!")
                print("Available Skeletons:")
                for i, monster_idx in enumerate(skeleton_indices):
                    print(f"{i+1}. Skeleton at position {monster_idx+1}")
                
                # Ask how many Skeletons to defeat
                while True:
                    num_skeletons = input(f"How many Skeletons to defeat (1-{len(skeleton_indices)})? ").strip()
                    try:
                        num_skeletons = min(len(skeleton_indices), max(1, int(num_skeletons)))
                        # If Bard's specialty is active, add 1 extra monster
                        if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                            num_skeletons = min(len(skeleton_indices), num_skeletons + 1)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                
                # Remove Skeletons (from highest index to lowest to avoid shifting issues)
                skeletons_defeated = 0
                for monster_idx in sorted(skeleton_indices[:num_skeletons], reverse=True):
                    game_state.dungeon_dice.remove(DungeonDiceFace.SKELETON.value)
                    monsters.pop(monster_idx)
                    skeletons_defeated += 1
                
                print(f"{skeletons_defeated} Skeleton(s) defeated!")
                
                # Gain experience (1 per monster)
                game_state.experience_tokens += skeletons_defeated
                print(f"Gained {skeletons_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                return True
            else:
                print("No Skeletons available for the Champion to defeat!")
                return False
                
        elif choice == "3":
            # Handle Oozes
            ooze_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.OOZE.value]
            if ooze_indices:
                print(f"\nChampion can defeat any number of Oozes!")
                if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                    print("Bard's specialty: Champion can defeat 1 extra monster!")
                print("Available Oozes:")
                for i, monster_idx in enumerate(ooze_indices):
                    print(f"{i+1}. Ooze at position {monster_idx+1}")
                
                # Ask how many Oozes to defeat
                while True:
                    num_oozes = input(f"How many Oozes to defeat (1-{len(ooze_indices)})? ").strip()
                    try:
                        num_oozes = min(len(ooze_indices), max(1, int(num_oozes)))
                        # If Bard's specialty is active, add 1 extra monster
                        if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER:
                            num_oozes = min(len(ooze_indices), num_oozes + 1)
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                
                # Remove Oozes (from highest index to lowest to avoid shifting issues)
                oozes_defeated = 0
                for monster_idx in sorted(ooze_indices[:num_oozes], reverse=True):
                    game_state.dungeon_dice.remove(DungeonDiceFace.OOZE.value)
                    monsters.pop(monster_idx)
                    oozes_defeated += 1
                
                print(f"{oozes_defeated} Ooze(s) defeated!")
                
                # Gain experience (1 per monster)
                game_state.experience_tokens += oozes_defeated
                print(f"Gained {oozes_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                return True
            else:
                print("No Oozes available for the Champion to defeat!")
                return False
        else:
            print("Invalid choice!")
            return False
    
    @staticmethod
    def use_companions(game_state, monsters, hero_card, specialty_active):
        """Use specific companions to defeat monsters."""
        if not monsters:
            print("No monsters to defeat!")
            return False
            
        # Show available companions and treasures
        print("\nAvailable Companions and Treasures:")
        companions = []
        
        # Add party dice
        for i, die in enumerate(game_state.party_dice):
            if die != PartyDiceFace.SCROLL.value:  # Scrolls aren't used for direct combat
                companions.append(("party", i, die))
                print(f"{len(companions)}. Party Die: {die}")
        
        # Add usable treasure companions
        treasure_companions = game_state.get_usable_companions()
        for i, (idx, token) in enumerate(treasure_companions):
            companions.append(("treasure", idx, token))
            print(f"{len(companions)}. Treasure: {token.name} (acts as {token.get_companion_type()})")
        
        print(f"{len(companions)+1}. Cancel")
        
        if not companions:
            print("No companions available!")
            return False
        
        # Print monsters
        print("\nMonsters to Defeat:")
        for i, monster in enumerate(monsters):
            print(f"{i+1}. {monster}")
        
        # Select companion
        companion_idx = input("Select companion to use (number): ").strip()
        try:
            companion_idx = int(companion_idx) - 1
            if companion_idx == len(companions):
                return False
            if 0 <= companion_idx < len(companions):
                source, idx, companion = companions[companion_idx]
                
                # Get companion type
                companion_type = companion.get_companion_type() if source == "treasure" else companion
                
                # Special handling for Fighters vs Goblins
                if companion_type == PartyDiceFace.FIGHTER.value:
                    # First, show all available monster options
                    print("\nFighter can defeat:")
                    print("1. One Skeleton")
                    print("2. One Ooze")
                    print("3. Any number of Goblins")
                    
                    choice = input("Choose what to defeat (1-3): ").strip()
                    
                    if choice == "1":
                        # Check for Skeletons
                        skeleton_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.SKELETON.value]
                        if skeleton_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Skeleton
                            monster_idx = skeleton_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.SKELETON.value)
                            monsters.pop(monster_idx)
                            print("Fighter defeats 1 Skeleton!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Skeletons available for the Fighter to defeat!")
                            return False
                            
                    elif choice == "2":
                        # Check for Oozes
                        ooze_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.OOZE.value]
                        if ooze_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Ooze
                            monster_idx = ooze_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.OOZE.value)
                            monsters.pop(monster_idx)
                            print("Fighter defeats 1 Ooze!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Oozes available for the Fighter to defeat!")
                            return False
                            
                    elif choice == "3":
                        # Count available Goblins
                        goblin_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.GOBLIN.value]
                        if goblin_indices:
                            print(f"\nFighter can defeat any number of Goblins!")
                            print("Available Goblins:")
                            for i, monster_idx in enumerate(goblin_indices):
                                print(f"{i+1}. Goblin at position {monster_idx+1}")
                            
                            # Ask how many Goblins to defeat
                            while True:
                                num_goblins = input(f"How many Goblins to defeat (1-{len(goblin_indices)})? ").strip()
                                try:
                                    num_goblins = min(len(goblin_indices), max(1, int(num_goblins)))
                                    break
                                except ValueError:
                                    print("Invalid input. Please enter a number.")
                            
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove Goblins (from highest index to lowest to avoid shifting issues)
                            goblins_defeated = 0
                            for monster_idx in sorted(goblin_indices[:num_goblins], reverse=True):
                                game_state.dungeon_dice.remove(DungeonDiceFace.GOBLIN.value)
                                monsters.pop(monster_idx)
                                goblins_defeated += 1
                            
                            print(f"{goblins_defeated} Goblin(s) defeated!")
                            
                            # Gain experience (1 per monster)
                            game_state.experience_tokens += goblins_defeated
                            print(f"Gained {goblins_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Goblins available for the Fighter to defeat!")
                            return False
                    else:
                        print("Invalid choice!")
                        return False
                
                # Special handling for Clerics vs Skeletons
                elif companion_type == PartyDiceFace.CLERIC.value:
                    # First, show all available monster options
                    print("\nCleric can defeat:")
                    print("1. One Goblin")
                    print("2. One Ooze")
                    print("3. Any number of Skeletons")
                    
                    choice = input("Choose what to defeat (1-3): ").strip()
                    
                    if choice == "1":
                        # Check for Goblins
                        goblin_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.GOBLIN.value]
                        if goblin_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Goblin
                            monster_idx = goblin_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.GOBLIN.value)
                            monsters.pop(monster_idx)
                            print("Cleric defeats 1 Goblin!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Goblins available for the Cleric to defeat!")
                            return False
                            
                    elif choice == "2":
                        # Check for Oozes
                        ooze_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.OOZE.value]
                        if ooze_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Ooze
                            monster_idx = ooze_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.OOZE.value)
                            monsters.pop(monster_idx)
                            print("Cleric defeats 1 Ooze!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Oozes available for the Cleric to defeat!")
                            return False
                            
                    elif choice == "3":
                        # Count available Skeletons
                        skeleton_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.SKELETON.value]
                        if skeleton_indices:
                            print(f"\nCleric can defeat any number of Skeletons!")
                            print("Available Skeletons:")
                            for i, monster_idx in enumerate(skeleton_indices):
                                print(f"{i+1}. Skeleton at position {monster_idx+1}")
                            
                            # Ask how many Skeletons to defeat
                            while True:
                                num_skeletons = input(f"How many Skeletons to defeat (1-{len(skeleton_indices)})? ").strip()
                                try:
                                    num_skeletons = min(len(skeleton_indices), max(1, int(num_skeletons)))
                                    break
                                except ValueError:
                                    print("Invalid input. Please enter a number.")
                            
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove Skeletons (from highest index to lowest to avoid shifting issues)
                            skeletons_defeated = 0
                            for monster_idx in sorted(skeleton_indices[:num_skeletons], reverse=True):
                                game_state.dungeon_dice.remove(DungeonDiceFace.SKELETON.value)
                                monsters.pop(monster_idx)
                                skeletons_defeated += 1
                            
                            print(f"{skeletons_defeated} Skeleton(s) defeated!")
                            
                            # Gain experience (1 per monster)
                            game_state.experience_tokens += skeletons_defeated
                            print(f"Gained {skeletons_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Skeletons available for the Cleric to defeat!")
                            return False
                    else:
                        print("Invalid choice!")
                        return False
                
                # Special handling for Mages vs Oozes
                elif companion_type == PartyDiceFace.MAGE.value:
                    # First, show all available monster options
                    print("\nMage can defeat:")
                    print("1. One Goblin")
                    print("2. One Skeleton")
                    print("3. Any number of Oozes")
                    
                    choice = input("Choose what to defeat (1-3): ").strip()
                    
                    if choice == "1":
                        # Check for Goblins
                        goblin_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.GOBLIN.value]
                        if goblin_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Goblin
                            monster_idx = goblin_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.GOBLIN.value)
                            monsters.pop(monster_idx)
                            print("Mage defeats 1 Goblin!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Goblins available for the Mage to defeat!")
                            return False
                            
                    elif choice == "2":
                        # Check for Skeletons
                        skeleton_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.SKELETON.value]
                        if skeleton_indices:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove one Skeleton
                            monster_idx = skeleton_indices[0]
                            game_state.dungeon_dice.remove(DungeonDiceFace.SKELETON.value)
                            monsters.pop(monster_idx)
                            print("Mage defeats 1 Skeleton!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Skeletons available for the Mage to defeat!")
                            return False
                            
                    elif choice == "3":
                        # Count available Oozes
                        ooze_indices = [i for i, m in enumerate(monsters) if m == DungeonDiceFace.OOZE.value]
                        if ooze_indices:
                            print(f"\nMage can defeat any number of Oozes!")
                            print("Available Oozes:")
                            for i, monster_idx in enumerate(ooze_indices):
                                print(f"{i+1}. Ooze at position {monster_idx+1}")
                            
                            # Ask how many Oozes to defeat
                            while True:
                                num_oozes = input(f"How many Oozes to defeat (1-{len(ooze_indices)})? ").strip()
                                try:
                                    num_oozes = min(len(ooze_indices), max(1, int(num_oozes)))
                                    break
                                except ValueError:
                                    print("Invalid input. Please enter a number.")
                            
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove Oozes (from highest index to lowest to avoid shifting issues)
                            oozes_defeated = 0
                            for monster_idx in sorted(ooze_indices[:num_oozes], reverse=True):
                                game_state.dungeon_dice.remove(DungeonDiceFace.OOZE.value)
                                monsters.pop(monster_idx)
                                oozes_defeated += 1
                            
                            print(f"{oozes_defeated} Ooze(s) defeated!")
                            
                            # Gain experience (1 per monster)
                            game_state.experience_tokens += oozes_defeated
                            print(f"Gained {oozes_defeated} experience token(s)! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print("No Oozes available for the Mage to defeat!")
                            return False
                    else:
                        print("Invalid choice!")
                        return False
                
                # Regular monster selection for other companions
                monster_idx = input("Select monster to defeat (number): ").strip()
                try:
                    monster_idx = int(monster_idx) - 1
                    if 0 <= monster_idx < len(monsters):
                        monster = monsters[monster_idx]
                        
                        # Check if this companion can defeat this monster
                        can_defeat = False
                        
                        # Apply Minstrel/Bard specialty if active
                        if specialty_active and hero_card.name in ["Minstrel", "Bard"]:
                            if companion_type == PartyDiceFace.THIEF.value and monster == DungeonDiceFace.OOZE.value:
                                can_defeat = True
                                print("Minstrel/Bard specialty: Thief can defeat Ooze!")
                            elif companion_type == PartyDiceFace.MAGE.value and monster == DungeonDiceFace.GOBLIN.value:
                                can_defeat = True
                                print("Minstrel/Bard specialty: Mage can defeat Goblin!")
                        
                        # Standard defeat rules
                        if companion_type == PartyDiceFace.CLERIC.value and monster == DungeonDiceFace.SKELETON.value:
                            can_defeat = True
                        elif companion_type == PartyDiceFace.MAGE.value and monster == DungeonDiceFace.OOZE.value:
                            can_defeat = True
                        elif companion_type == PartyDiceFace.THIEF.value:
                            # Thief can defeat any single monster
                            can_defeat = True
                        elif companion_type == PartyDiceFace.CHAMPION.value:
                            # Champions should use the use_champion method instead
                            print("To use a Champion, select the 'Use a Champion' action instead.")
                            return False
                        
                        if can_defeat:
                            # Use the companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion_type} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            # Remove monster
                            game_state.dungeon_dice.remove(monster)
                            monsters.pop(monster_idx)
                            
                            print(f"Monster {monster} defeated!")
                            
                            # Gain experience
                            game_state.experience_tokens += 1
                            print(f"Gained 1 experience token! Total: {game_state.experience_tokens}")
                            return True
                        else:
                            print(f"This companion cannot defeat {monster}!")
                            return False
                    else:
                        print("Invalid monster selection.")
                        return False
                except ValueError:
                    print("Invalid input.")
                    return False
            else:
                print("Invalid companion selection.")
                return False
        except ValueError:
            print("Invalid input.")
            return False
    
    @staticmethod
    def can_defeat_monsters(game_state, monsters, hero_card, specialty_active):
        """Check if the remaining monsters can be defeated with available companions."""
        # Create copies to avoid modifying originals
        available_dice = game_state.party_dice.copy()
        remaining_monsters = monsters.copy()
        
        # Count companions by type
        fighters = available_dice.count(PartyDiceFace.FIGHTER.value)
        clerics = available_dice.count(PartyDiceFace.CLERIC.value)
        mages = available_dice.count(PartyDiceFace.MAGE.value)
        thieves = available_dice.count(PartyDiceFace.THIEF.value)
        champions = available_dice.count(PartyDiceFace.CHAMPION.value)
        
        # Champions first - they're most efficient
        if champions > 0:
            # Each champion can defeat all monsters of one type
            # Count monsters by type
            goblins = remaining_monsters.count(DungeonDiceFace.GOBLIN.value)
            skeletons = remaining_monsters.count(DungeonDiceFace.SKELETON.value)
            oozes = remaining_monsters.count(DungeonDiceFace.OOZE.value)
            
            # For each champion, remove all monsters of the type that has the most
            for _ in range(champions):
                max_count = max(goblins, skeletons, oozes)
                if max_count == 0:
                    break
                if goblins == max_count:
                    # Remove all goblins
                    remaining_monsters = [m for m in remaining_monsters if m != DungeonDiceFace.GOBLIN.value]
                    goblins = 0
                elif skeletons == max_count:
                    # Remove all skeletons
                    remaining_monsters = [m for m in remaining_monsters if m != DungeonDiceFace.SKELETON.value]
                    skeletons = 0
                elif oozes == max_count:
                    # Remove all oozes
                    remaining_monsters = [m for m in remaining_monsters if m != DungeonDiceFace.OOZE.value]
                    oozes = 0
            
            if not remaining_monsters:
                return True
        
        # Count monsters by type for remaining monsters
        goblins = remaining_monsters.count(DungeonDiceFace.GOBLIN.value)
        skeletons = remaining_monsters.count(DungeonDiceFace.SKELETON.value)
        oozes = remaining_monsters.count(DungeonDiceFace.OOZE.value)
        
        # Apply Minstrel/Bard specialty if active
        if specialty_active and hero_card.name in ["Minstrel", "Bard"]:
            # Thieves may be used as Mages and Mages may be used as Thieves
            # For simplicity in checking, we'll just make both able to defeat both monster types
            fighter_can_defeat = {"Goblin": float('inf'), "Skeleton": 1, "Ooze": 1}  # Fighters can defeat all Goblins or one Skeleton or one Ooze
            cleric_can_defeat = {"Skeleton": float('inf'), "Goblin": 1, "Ooze": 1}  # Clerics can defeat all Skeletons or one Goblin or one Ooze
            mage_can_defeat = {"Ooze": float('inf'), "Goblin": 1, "Skeleton": 1}  # Can defeat all Oozes or one Goblin or one Skeleton
            thief_can_defeat = {"Goblin": 1, "Skeleton": 1, "Ooze": 1}  # Can defeat any one monster
        else:
            fighter_can_defeat = {"Goblin": float('inf'), "Skeleton": 1, "Ooze": 1}  # Fighters can defeat all Goblins or one Skeleton or one Ooze
            cleric_can_defeat = {"Skeleton": float('inf'), "Goblin": 1, "Ooze": 1}  # Clerics can defeat all Skeletons or one Goblin or one Ooze
            mage_can_defeat = {"Ooze": float('inf'), "Goblin": 1, "Skeleton": 1}  # Can defeat all Oozes or one Goblin or one Skeleton
            thief_can_defeat = {"Goblin": 1, "Skeleton": 1, "Ooze": 1}  # Can defeat any one monster
        
        # Try to match companions to monsters optimally
        # First handle specialists who can defeat multiple monsters
        if fighters > 0:
            # Each fighter can defeat either all Goblins, one Skeleton, or one Ooze
            # We'll prioritize using fighters for Goblins if there are any
            if goblins > 0:
                goblins = 0  # One Fighter can defeat all Goblins
            elif skeletons > 0:
                skeletons = max(0, skeletons - fighters)  # Each remaining fighter can defeat one Skeleton
            elif oozes > 0:
                oozes = max(0, oozes - fighters)  # Each remaining fighter can defeat one Ooze

        if clerics > 0:
            # Each cleric can defeat either all Skeletons, one Goblin, or one Ooze
            # We'll prioritize using clerics for Skeletons if there are any
            if skeletons > 0:
                skeletons = 0  # One Cleric can defeat all Skeletons
            elif goblins > 0:
                goblins = max(0, goblins - clerics)  # Each remaining cleric can defeat one Goblin
            elif oozes > 0:
                oozes = max(0, oozes - clerics)  # Each remaining cleric can defeat one Ooze

        if mages > 0:
            # Each mage can defeat either all Oozes, one Goblin, or one Skeleton
            # We'll prioritize using mages for Oozes if there are any
            if oozes > 0:
                oozes = 0  # One Mage can defeat all Oozes
            elif goblins > 0:
                goblins = max(0, goblins - mages)  # Each remaining mage can defeat one Goblin
            elif skeletons > 0:
                skeletons = max(0, skeletons - mages)  # Each remaining mage can defeat one Skeleton
        
        # Count remaining monsters that need to be defeated
        remaining_count = goblins + skeletons + oozes
        
        # See if we have enough thieves to handle the rest
        # Each thief can defeat one of any type
        if thieves >= remaining_count:
            return True
        
        return False
    
    @staticmethod
    def use_companions_for_remaining_monsters(game_state, monsters, hero_card, specialty_active):
        """
        Automatically use companions to defeat remaining monsters.
        This is called when the player chooses to end the monster phase but can defeat all monsters.
        """
        # Create a copy of monsters to work with
        remaining_monsters = monsters.copy()
        
        # Use champions first (most efficient)
        champion_indices = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.CHAMPION.value]
        
        for idx in sorted(champion_indices, reverse=True):
            # Calculate how many monsters this champion can defeat
            monsters_to_defeat = len(remaining_monsters)  # Champions can defeat any number of same-type monsters
            
            # Move champion to graveyard
            game_state.use_party_die(idx)
            
            # Defeat monsters
            defeats = 0
            while defeats < monsters_to_defeat and remaining_monsters:
                monster = remaining_monsters[0]
                if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                    game_state.dungeon_dice.remove(monster)
                remaining_monsters.pop(0)
                print(f"Champion defeats {monster}!")
                defeats += 1
                
                # If using Bard (Master) specialty, Champions can defeat 1 extra monster of a different type
                if specialty_active and hero_card.name == "Bard" and hero_card.current_rank == HeroRank.MASTER and remaining_monsters:
                    next_monster = remaining_monsters[0]
                    if next_monster != monster:  # Only if it's a different type
                        if next_monster in game_state.dungeon_dice:
                            game_state.dungeon_dice.remove(next_monster)
                        remaining_monsters.pop(0)
                        print(f"Champion defeats {next_monster} (Bard's specialty: +1 monster)!")
                        defeats += 1
                        break  # Only one extra monster
            
            if not remaining_monsters:
                break

            # If we still have monsters, use specific companions
            if remaining_monsters:
                # Apply Minstrel/Bard specialty if active
                if specialty_active and hero_card.name in ["Minstrel", "Bard"]:
                    # Thieves may be used as Mages and Mages may be used as Thieves
                    fighter_can_defeat = {"Goblin": float('inf'), "Skeleton": 1, "Ooze": 1}
                    cleric_can_defeat = {"Skeleton": float('inf'), "Goblin": 1, "Ooze": 1}
                    mage_can_defeat = {"Ooze": float('inf'), "Goblin": 1}
                    thief_can_defeat = {"Goblin": 1, "Skeleton": 1, "Ooze": 1}
                else:
                    fighter_can_defeat = {"Goblin": float('inf'), "Skeleton": 1, "Ooze": 1}
                    cleric_can_defeat = {"Skeleton": float('inf'), "Goblin": 1, "Ooze": 1}
                    mage_can_defeat = {"Ooze": float('inf')}
                    thief_can_defeat = {"Goblin": 1, "Skeleton": 1, "Ooze": 1}

                # Sort monsters by most restrictive first
                # Goblins (only Fighter/Thief), Skeletons (only Cleric/Thief), Oozes (only Mage/Thief)
                sorted_monsters = []
                # Prioritize monsters that fewer heroes can defeat
                for monster_type in [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]:
                    for monster in remaining_monsters[:]:
                        if monster == monster_type:
                            sorted_monsters.append(monster)
                            remaining_monsters.remove(monster)
                
                # Process each monster
                for monster in sorted_monsters:
                    # Try to find the most appropriate hero to defeat this monster
                    defeated = False
                    
                    # Look for the appropriate specialists first
                    if monster == DungeonDiceFace.GOBLIN.value:
                        for i, die in enumerate(game_state.party_dice):
                            if die == PartyDiceFace.FIGHTER.value:
                                game_state.use_party_die(i)
                                if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                    game_state.dungeon_dice.remove(monster)
                                print(f"Fighter defeats {monster}!")
                                defeated = True
                                break
                    elif monster == DungeonDiceFace.SKELETON.value:
                        for i, die in enumerate(game_state.party_dice):
                            if die == PartyDiceFace.CLERIC.value:
                                game_state.use_party_die(i)
                                if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                    game_state.dungeon_dice.remove(monster)
                                print(f"Cleric defeats {monster}!")
                                defeated = True
                                break
                    elif monster == DungeonDiceFace.OOZE.value:
                        for i, die in enumerate(game_state.party_dice):
                            if die == PartyDiceFace.MAGE.value:
                                game_state.use_party_die(i)
                                if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                    game_state.dungeon_dice.remove(monster)
                                print(f"Mage defeats {monster} (using {hero_card.name}'s specialty)!")
                                defeated = True
                                break
                    
                    # If not defeated yet, consider specialty rules
                    if not defeated and specialty_active and hero_card.name in ["Minstrel", "Bard"]:
                        if monster == DungeonDiceFace.GOBLIN.value:
                            for i, die in enumerate(game_state.party_dice):
                                if die == PartyDiceFace.MAGE.value:
                                    game_state.use_party_die(i)
                                    if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                        game_state.dungeon_dice.remove(monster)
                                    print(f"Mage defeats {monster} (using {hero_card.name}'s specialty)!")
                                    defeated = True
                                    break
                        elif monster == DungeonDiceFace.OOZE.value:
                            for i, die in enumerate(game_state.party_dice):
                                if die == PartyDiceFace.THIEF.value:
                                    game_state.use_party_die(i)
                                    if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                        game_state.dungeon_dice.remove(monster)
                                    print(f"Thief defeats {monster} (using {hero_card.name}'s specialty)!")
                                    defeated = True
                                    break
                    
                    # If still not defeated, try a thief as last resort
                    if not defeated:
                        for i, die in enumerate(game_state.party_dice):
                            if die == PartyDiceFace.THIEF.value:
                                game_state.use_party_die(i)
                                if monster in game_state.dungeon_dice:  # Check if monster is still in dungeon dice
                                    game_state.dungeon_dice.remove(monster)
                                print(f"Thief defeats {monster}!")
                                defeated = True
                                break

class LootPhase:
    @staticmethod
    def execute(game_state):
        """Execute the Loot Phase."""
        print("\n" + "="*50)
        print("💎 LOOT PHASE 💎".center(50))
        print("="*50)
        
        # If Alchemist/Thaumaturge is active, convert all chests to potions
        if game_state.selected_hero_card.__class__.__name__ == "AlchemistThaumaturgeHero":
            chest_indices = [i for i, die in enumerate(game_state.dungeon_dice) 
                           if die == DungeonDiceFace.CHEST.value]
            if chest_indices:
                for idx in reversed(chest_indices):
                    game_state.dungeon_dice[idx] = DungeonDiceFace.POTION.value
                print(f"\n✨ The {game_state.selected_hero_card.name}'s alchemy transforms {len(chest_indices)} chest(s) into potions! ✨")
        
        # Count available chests and potions
        chests = game_state.dungeon_dice.count(DungeonDiceFace.CHEST.value)
        potions = game_state.dungeon_dice.count(DungeonDiceFace.POTION.value)
        
        print(f"\n📦 Available Loot:")
        print(f"  ▫️ Chests: {chests}")
        print(f"  ▫️ Potions: {potions}")
        LootPhase.print_state(game_state)
        
        # Allow actions while there are chests or potions
        while chests > 0 or potions > 0:
            print("\n📋 Loot Phase Actions:")
            actions = []
            if chests > 0:
                actions.append("Open Treasure Chests")
            if potions > 0:
                actions.append("Drink Healing Potions")
            actions.append("End Loot Phase")
            
            for i, action in enumerate(actions, 1):
                if "Chest" in action:
                    print(f"{i}. 📦 {action}")
                elif "Potion" in action:
                    print(f"{i}. 🧪 {action}")
                else:
                    print(f"{i}. 🚪 {action}")
            
            choice = input("\nChoose action (number): ").strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(actions):
                    selected_action = actions[choice_idx]
                    
                    if selected_action == "Open Treasure Chests":
                        chests = LootPhase.open_chests(game_state, chests)
                    elif selected_action == "Drink Healing Potions":
                        potions = LootPhase.quaff_potions(game_state, potions)
                    else:  # End Loot Phase
                        break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
            
            LootPhase.print_state(game_state)
        
        # Return unused Chests and Potions to available pool
        if chests > 0 or potions > 0:
            print("\n🔄 Returning unused items to available pool...")
            print(f"  ▫️ Returned {chests} Chest(s) and {potions} Potion(s)")
        
        return True
    
    @staticmethod
    def print_state(game_state):
        """Print the current game state."""
        print("\nGame State:")
        
        # Count and display party dice
        dice_counts = {}
        total_companions = 0
        for die in game_state.party_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
            if die != PartyDiceFace.SCROLL.value:  # Don't count scrolls as companions
                total_companions += 1
        print("Party Dice:")
        for die_face, count in dice_counts.items():
            print(f"- {die_face}: {count} dice")
        print(f"Total Companions: {total_companions}")
        print(f"Total Scrolls: {dice_counts.get(PartyDiceFace.SCROLL.value, 0)}")
        
        # Count and display graveyard dice
        graveyard_counts = {}
        for die in game_state.graveyard:
            graveyard_counts[die] = graveyard_counts.get(die, 0) + 1
        print("\nGraveyard:")
        if graveyard_counts:
            for die_face, count in graveyard_counts.items():
                print(f"- {die_face}: {count} dice")
        else:
            print("- Empty")
        
        # Count and display dungeon dice
        dungeon_counts = {}
        total_monsters = 0
        for die in game_state.dungeon_dice:
            dungeon_counts[die] = dungeon_counts.get(die, 0) + 1
            if die in [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]:
                total_monsters += 1
        print("\nDungeon Dice:")
        for die_face, count in dungeon_counts.items():
            print(f"- {die_face}: {count} dice")
        print(f"Total Monsters: {total_monsters}")
        print(f"Total Chests: {dungeon_counts.get(DungeonDiceFace.CHEST.value, 0)}")
        print(f"Total Potions: {dungeon_counts.get(DungeonDiceFace.POTION.value, 0)}")
        
        if game_state.dragons_lair:
            print("\nDragon's Lair:")
            print(f"- Dragon: {len(game_state.dragons_lair)} dice")
        
        print(f"\nTreasure Tokens: {game_state.treasure_tokens}")
        print(f"Experience Tokens: {game_state.experience_tokens}")
    
    @staticmethod
    def open_chests(game_state, available_chests):
        """Open chests using companions."""
        if not available_chests:
            print("No Chests available to open!")
            return 0
            
        if not game_state.party_dice:
            print("No companions available to open Chests!")
            return available_chests
            
        print("\nSelect a companion to open Chests:")
        print("Special Abilities:")
        print("- Thieves and Champions can open any number of Chests")
        print("- Other companions can open one Chest each")
        
        # Show available companions
        companions = []
        for i, die in enumerate(game_state.party_dice):
            companions.append((i, die))
            max_chests = "any number of" if die in [PartyDiceFace.THIEF.value, PartyDiceFace.CHAMPION.value] else "1"
            print(f"{i+1}. {die} (can open {max_chests} Chests)")
        print(f"{len(companions)+1}. Cancel")
        
        choice = input("Choose companion (number): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(companions):
                return available_chests
            if 0 <= choice_idx < len(companions):
                idx, companion = companions[choice_idx]
                
                # Determine how many chests can be opened
                if companion in [PartyDiceFace.THIEF.value, PartyDiceFace.CHAMPION.value]:
                    max_chests = available_chests
                    print(f"This {companion} can open up to {max_chests} Chests!")
                else:
                    max_chests = 1
                    print(f"This {companion} can open 1 Chest.")
                
                # Ask how many chests to open
                if max_chests > 1:
                    num_chests = input(f"How many Chests to open (1-{max_chests})? ").strip()
                    try:
                        num_chests = min(max_chests, max(1, int(num_chests)))
                    except ValueError:
                        print("Invalid input. Opening 1 Chest.")
                        num_chests = 1
                else:
                    num_chests = 1
                
                # Move companion to graveyard
                game_state.use_party_die(idx)
                print(f"{companion} moved to Graveyard.")
                
                # Open chests and gain treasure
                for _ in range(num_chests):
                    # Remove chest from dungeon dice
                    game_state.dungeon_dice.remove(DungeonDiceFace.CHEST.value)
                    available_chests -= 1
                    
                    # Draw a treasure token
                    treasure = game_state.treasure_manager.draw_treasure()
                    if treasure:
                        game_state.add_treasure(treasure)
                        print(f"\nYou found: {treasure.name}")
                        print(f"Effect: {treasure.get_description()}")
                        
                        # If it's a companion-type treasure, show it in the party section
                        if treasure.can_use_as_companion():
                            print(f"This treasure can be used as a {treasure.get_companion_type()} in your party!")
                    else:
                        # If no treasure tokens remain, gain experience instead
                        game_state.experience_tokens += 1
                        print("\nNo Treasure tokens remain! You gain an Experience token instead.")
                
                print(f"\nTotal Experience tokens: {game_state.experience_tokens}")
                
                return available_chests
            else:
                print("Invalid choice.")
                return available_chests
        except ValueError:
            print("Invalid input.")
            return available_chests
    
    @staticmethod
    def quaff_potions(game_state, available_potions):
        """Quaff potions to recover dice from the graveyard."""
        if not available_potions:
            print("No Potions available to quaff!")
            return 0
            
        if not game_state.party_dice:
            print("No Party dice available to quaff Potions!")
            return available_potions
            
        if not game_state.graveyard:
            print("No dice in Graveyard to recover!")
            return available_potions
            
        print("\nSelect a Party die to use for quaffing Potions:")
        print(f"You can quaff up to {available_potions} Potions.")
        print("Each Potion allows you to recover one die from the Graveyard.")
        
        # Show available party dice
        for i, die in enumerate(game_state.party_dice):
            print(f"{i+1}. {die}")
        print(f"{len(game_state.party_dice)+1}. Cancel")
        
        try:
            choice = input("Choose Party die (number): ").strip()
            choice_idx = int(choice) - 1
            if choice_idx == len(game_state.party_dice):
                return available_potions
            if 0 <= choice_idx < len(game_state.party_dice):
                # Ask how many potions to quaff
                max_potions = min(available_potions, len(game_state.graveyard))
                print(f"\nYou can recover up to {max_potions} dice from the Graveyard.")
                num_potions = input(f"How many Potions to quaff (1-{max_potions})? ").strip()
                try:
                    num_potions = min(max_potions, max(1, int(num_potions)))
                except ValueError:
                    print("Invalid input. Quaffing 1 Potion.")
                    num_potions = 1
                
                # Quaff potions
                for i in range(num_potions):
                    print(f"\nPotion {i+1}/{num_potions}:")
                    print("Choose a die face for the recovered Party die:")
                    for i, face in enumerate(PartyDiceFace):
                        print(f"{i+1}. {face.value}")
                    
                    face_choice = input("Choose face (number): ").strip()
                    try:
                        face_idx = int(face_choice) - 1
                        if 0 <= face_idx < len(PartyDiceFace):
                            # Remove a die from graveyard
                            game_state.graveyard.pop()
                            # Add new die with chosen face
                            chosen_face = list(PartyDiceFace)[face_idx].value
                            game_state.party_dice.append(chosen_face)
                            print(f"Added a {chosen_face} to your active party!")
                        else:
                            print("Invalid face choice. Using Fighter.")
                            game_state.graveyard.pop()
                            game_state.party_dice.append(PartyDiceFace.FIGHTER.value)
                    except ValueError:
                        print("Invalid input. Using Fighter.")
                        game_state.graveyard.pop()
                        game_state.party_dice.append(PartyDiceFace.FIGHTER.value)
                    
                    # Remove potion from dungeon dice and add to graveyard
                    game_state.dungeon_dice.remove(DungeonDiceFace.POTION.value)
                    game_state.graveyard.append(DungeonDiceFace.POTION.value)
                    available_potions -= 1
                
                return available_potions
            else:
                print("Invalid choice.")
                return available_potions
        except ValueError:
            print("Invalid input.")
            return available_potions 