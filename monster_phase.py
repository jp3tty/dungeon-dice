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
                # Go directly to companion selection with descriptions
                if MonsterPhase.use_companions(game_state, monsters, hero_card, True):
                    # Update monster list as dice may have changed
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
        
        # Add treasure companions to the display
        treasure_companions = game_state.get_usable_companions()
        for idx, token in treasure_companions:
            companion_type = token.get_companion_type()
            dice_counts[companion_type] = dice_counts.get(companion_type, 0) + 1
            total_companions += 1
        
        for die_face, count in dice_counts.items():
            print(f"  ▫️ {die_face}: {count} dice")
        print(f"  Total Companions: {total_companions}")
        print(f"  Total Scrolls: {dice_counts.get(PartyDiceFace.SCROLL.value, 0)}")
        
        print("\n💎 Carried Treasure:")
        treasures = game_state.get_available_treasures()
        if treasures:
            for treasure in treasures:
                print(f"  ▫️ {treasure.name} - {treasure.get_description()}")
        else:
            print("  ▫️ None")
        
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
        
        print("\n🐉 Dragon's Lair:")
        if game_state.dragons_lair:
            print(f"  ▫️ Dragon: {len(game_state.dragons_lair)} dice")
        else:
            print("  ▫️ Empty")
    
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
        
        if not reroll_options:
            print("No dice available to re-roll!")
            return False
        
        print(f"{len(reroll_options)+1}. Cancel")
        
        choice = input("Choose dice to re-roll (number): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(reroll_options):
                print("Re-roll cancelled.")
                return False
            if 0 <= choice_idx < len(reroll_options):
                source, idx, old_die = reroll_options[choice_idx]
                
                # Re-roll the selected die
                dice_manager = DiceManager()
                if source == "dungeon":
                    new_die = dice_manager.roll_dungeon_dice(1)[0]
                    game_state.dungeon_dice[idx] = new_die
                    print(f"Dungeon die re-rolled: {old_die} → {new_die}")
                else:  # party
                    new_die = dice_manager.roll_party_dice(1)[0]
                    game_state.party_dice[idx] = new_die
                    print(f"Party die re-rolled: {old_die} → {new_die}")
                
                return True
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False
    
    @staticmethod
    def use_champion(game_state, monsters, hero_card, specialty_active):
        """Use a Champion to defeat monsters."""
        champion_indices = [i for i, die in enumerate(game_state.party_dice) if die == PartyDiceFace.CHAMPION.value]
        
        if not champion_indices:
            print("No Champions available!")
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
        
        # Champions can defeat all monsters of a given type
        # Group monsters by type
        monster_types = {}
        for monster in monsters:
            if monster not in monster_types:
                monster_types[monster] = []
            monster_types[monster].append(monster)
        
        # Check if Expert Bard specialty is active
        bard_master_active = specialty_active and hero_card.current_rank == HeroRank.MASTER
        
        if bard_master_active:
            print(f"\n✨ Expert Bard's specialty active: Champion can defeat monsters of TWO different types! ✨")
            print(f"Champion can defeat all monsters of a given type:")
        else:
            print(f"\nChampion can defeat all monsters of a given type:")
        
        for i, (monster_type, monster_list) in enumerate(monster_types.items()):
            print(f"{i+1}. All {monster_type}s ({len(monster_list)} monster(s))")
        
        # Let player choose first monster type to defeat
        choice = input("Choose first monster type to defeat (number): ").strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(monster_types):
                selected_type = list(monster_types.keys())[choice_idx]
                selected_monsters = monster_types[selected_type]
                
                print(f"Champion defeats {len(selected_monsters)} {selected_type}(s).")
                
                # Remove defeated monsters from dungeon dice and monsters list
                for monster in selected_monsters:
                    game_state.dungeon_dice.remove(monster)
                    monsters.remove(monster)
                
                # If Expert Bard is active, allow selecting a second monster type
                if bard_master_active and len(monster_types) > 1:
                    # Update monster types after first defeat
                    remaining_monster_types = {}
                    for monster in monsters:
                        if monster not in remaining_monster_types:
                            remaining_monster_types[monster] = []
                        remaining_monster_types[monster].append(monster)
                    
                    if remaining_monster_types:
                        print(f"\n✨ Expert Bard's specialty allows defeating a second monster type! ✨")
                        print(f"Remaining monster types:")
                        for i, (monster_type, monster_list) in enumerate(remaining_monster_types.items()):
                            print(f"{i+1}. All {monster_type}s ({len(monster_list)} monster(s))")
                        
                        second_choice = input("Choose second monster type to defeat (number, or 0 to skip): ").strip()
                        try:
                            second_choice_idx = int(second_choice) - 1
                            if second_choice_idx == -1:  # Skip second choice
                                print("Skipping second monster type.")
                            elif 0 <= second_choice_idx < len(remaining_monster_types):
                                second_selected_type = list(remaining_monster_types.keys())[second_choice_idx]
                                second_selected_monsters = remaining_monster_types[second_selected_type]
                                
                                print(f"✨ Champion also defeats {len(second_selected_monsters)} {second_selected_type}(s)! ✨")
                                
                                # Remove second set of defeated monsters
                                for monster in second_selected_monsters:
                                    game_state.dungeon_dice.remove(monster)
                                    monsters.remove(monster)
                                
                                # Move champion to graveyard
                                game_state.use_party_die(champion_idx)
                                total_defeated = len(selected_monsters) + len(second_selected_monsters)
                                print(f"Champion moved to Graveyard after defeating {total_defeated} monsters ({len(selected_monsters)} {selected_type}s + {len(second_selected_monsters)} {second_selected_type}s).")
                                
                                return True
                            else:
                                print("Invalid choice for second monster type.")
                                # Move champion to graveyard for first defeat only
                                game_state.use_party_die(champion_idx)
                                print(f"Champion moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                                
                                return True
                        except ValueError:
                            print("Invalid input for second monster type.")
                            # Move champion to graveyard for first defeat only
                            game_state.use_party_die(champion_idx)
                            print(f"Champion moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                            
                            return True
                    else:
                        # No remaining monsters after first defeat
                        game_state.use_party_die(champion_idx)
                        print(f"Champion moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                        
                        return True
                else:
                    # Normal Champion behavior (no Expert Bard or no second monster type available)
                    game_state.use_party_die(champion_idx)
                    print(f"Champion moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                    
                    return True
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False
    
    @staticmethod
    def use_companions(game_state, monsters, hero_card, specialty_active):
        """Use companions to defeat monsters."""
        if not monsters:
            print("No monsters to defeat!")
            return False
        
        if not game_state.party_dice and not game_state.get_usable_companions():
            print("No companions available!")
            return False
        
        print("\n📋 Monster Defeat Guide:")
        print("• Fighter: defeats one Skeleton, one Ooze, or any number of Goblins")
        print("• Cleric: defeats one Goblin, one Ooze, or any number of Skeletons")
        print("• Mage: defeats one Goblin, one Skeleton, or any number of Oozes")
        print("• Thief: defeats one Goblin, one Skeleton, or one Ooze")
        print("• Champion: defeats any number of Goblins, Skeletons, or Oozes")
        
        if specialty_active:
            print(f"\n✨ {hero_card.name}'s specialty active:")
            if hero_card.current_rank == HeroRank.NOVICE:
                print("• Thieves may be used as Mages and Mages may be used as Thieves")
            else:  # Master
                print("• Thieves may be used as Mages and Mages may be used as Thieves")
                print("• Champions can defeat monsters of TWO different types")
        
        # Show available companions
        print("\n🤝 Available Companions:")
        companions = []
        
        # Add party dice companions
        for i, die in enumerate(game_state.party_dice):
            if die != PartyDiceFace.SCROLL.value:  # Scrolls are not companions
                companions.append(("party", i, die))
                print(f"{len(companions)}. Party: {die}")
        
        # Add treasure companions
        treasure_companions = game_state.get_usable_companions()
        for idx, token in treasure_companions:
            companions.append(("treasure", idx, token))
            print(f"{len(companions)}. Treasure: {token.name} (acts as {token.get_companion_type()})")
        
        if not companions:
            print("No companions available!")
            return False
        
        print(f"{len(companions)+1}. Cancel")
        
        choice = input("\nChoose companion to use (number): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == len(companions):
                return False
            if 0 <= choice_idx < len(companions):
                source, idx, companion = companions[choice_idx]
                
                # Determine companion type
                if source == "treasure":
                    companion_type = companion.get_companion_type()
                else:
                    companion_type = companion
                
                # Store original companion type for specialty choice
                original_companion_type = companion_type
                
                # Apply specialty transformations if Minstrel/Bard specialty is active
                if specialty_active and companion_type in [PartyDiceFace.THIEF.value, PartyDiceFace.MAGE.value]:
                    print(f"\n✨ Minstrel/Bard specialty allows {companion_type} to be used as either {companion_type} or the other type!")
                    print(f"1. Use as {companion_type} (original abilities)")
                    if companion_type == PartyDiceFace.THIEF.value:
                        print(f"2. Use as {PartyDiceFace.MAGE.value} (defeat all Oozes, open all chests)")
                    else:  # MAGE
                        print(f"2. Use as {PartyDiceFace.THIEF.value} (defeat all Oozes, open all chests)")
                    
                    choice = input("Choose how to use this companion (1 or 2): ").strip()
                    try:
                        choice_idx = int(choice)
                        if choice_idx == 1:
                            # Use original abilities
                            companion_type = original_companion_type
                        elif choice_idx == 2:
                            # Use other type's abilities
                            if companion_type == PartyDiceFace.THIEF.value:
                                companion_type = PartyDiceFace.MAGE.value
                                print(f"✨ {original_companion_type} acts as {companion_type}")
                            else:  # MAGE
                                companion_type = PartyDiceFace.THIEF.value
                                print(f"✨ {original_companion_type} acts as {companion_type}")
                        else:
                            print("Invalid choice. Using original abilities.")
                            companion_type = original_companion_type
                    except ValueError:
                        print("Invalid input. Using original abilities.")
                        companion_type = original_companion_type
                
                # Special handling for Champions
                if companion_type == PartyDiceFace.CHAMPION.value:
                    # Champions can defeat all monsters of a given type
                    # Group monsters by type
                    monster_types = {}
                    for monster in monsters:
                        if monster not in monster_types:
                            monster_types[monster] = []
                        monster_types[monster].append(monster)
                    
                    # Check if Master Bard specialty is active
                    bard_master_active = specialty_active and hero_card.current_rank == HeroRank.MASTER
                    
                    if bard_master_active:
                        print(f"\n✨ Master Bard's specialty active: Champion can defeat monsters of TWO different types! ✨")
                        print(f"Champion can defeat all monsters of a given type:")
                    else:
                        print(f"\nChampion can defeat all monsters of a given type:")
                    
                    for i, (monster_type, monster_list) in enumerate(monster_types.items()):
                        print(f"{i+1}. All {monster_type}s ({len(monster_list)} monster(s))")
                    
                    # Let player choose first monster type to defeat
                    choice = input("Choose first monster type to defeat (number): ").strip()
                    try:
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(monster_types):
                            selected_type = list(monster_types.keys())[choice_idx]
                            selected_monsters = monster_types[selected_type]
                            
                            print(f"Champion defeats {len(selected_monsters)} {selected_type}(s).")
                            
                            # Remove defeated monsters from dungeon dice and monsters list
                            for monster in selected_monsters:
                                game_state.dungeon_dice.remove(monster)
                                monsters.remove(monster)
                            
                            # If Expert Bard is active, allow selecting a second monster type
                            if bard_master_active and len(monster_types) > 1:
                                # Update monster types after first defeat
                                remaining_monster_types = {}
                                for monster in monsters:
                                    if monster not in remaining_monster_types:
                                        remaining_monster_types[monster] = []
                                    remaining_monster_types[monster].append(monster)
                                
                                if remaining_monster_types:
                                    print(f"\n✨ Expert Bard's specialty allows defeating a second monster type! ✨")
                                    print(f"Remaining monster types:")
                                    for i, (monster_type, monster_list) in enumerate(remaining_monster_types.items()):
                                        print(f"{i+1}. All {monster_type}s ({len(monster_list)} monster(s))")
                                    
                                    second_choice = input("Choose second monster type to defeat (number, or 0 to skip): ").strip()
                                    try:
                                        second_choice_idx = int(second_choice) - 1
                                        if second_choice_idx == -1:  # Skip second choice
                                            print("Skipping second monster type.")
                                        elif 0 <= second_choice_idx < len(remaining_monster_types):
                                            second_selected_type = list(remaining_monster_types.keys())[second_choice_idx]
                                            second_selected_monsters = remaining_monster_types[second_selected_type]
                                            
                                            print(f"✨ Champion also defeats {len(second_selected_monsters)} {second_selected_type}(s)! ✨")
                                            
                                            # Remove second set of defeated monsters
                                            for monster in second_selected_monsters:
                                                game_state.dungeon_dice.remove(monster)
                                                monsters.remove(monster)
                                            
                                            # Use companion
                                            if source == "party":
                                                game_state.use_party_die(idx)
                                                total_defeated = len(selected_monsters) + len(second_selected_monsters)
                                                print(f"{companion} moved to Graveyard after defeating {total_defeated} monsters ({len(selected_monsters)} {selected_type}s + {len(second_selected_monsters)} {second_selected_type}s).")
                                            else:  # treasure
                                                game_state.use_treasure(idx)
                                                total_defeated = len(selected_monsters) + len(second_selected_monsters)
                                                print(f"{companion.name} used and returned to treasure pool after defeating {total_defeated} monsters ({len(selected_monsters)} {selected_type}s + {len(second_selected_monsters)} {second_selected_type}s).")
                                            
                                            return True
                                        else:
                                            print("Invalid choice for second monster type.")
                                            # Use companion for first defeat only
                                            if source == "party":
                                                game_state.use_party_die(idx)
                                                print(f"{companion} moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                                            else:  # treasure
                                                game_state.use_treasure(idx)
                                                print(f"{companion.name} used and returned to treasure pool after defeating {len(selected_monsters)} {selected_type}(s).")
                                            
                                            return True
                                    except ValueError:
                                        print("Invalid input for second monster type.")
                                        # Use companion for first defeat only
                                        if source == "party":
                                            game_state.use_party_die(idx)
                                            print(f"{companion} moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                                        else:  # treasure
                                            game_state.use_treasure(idx)
                                            print(f"{companion.name} used and returned to treasure pool after defeating {len(selected_monsters)} {selected_type}(s).")
                                        
                                        return True
                                else:
                                    # No remaining monsters after first defeat
                                    if source == "party":
                                        game_state.use_party_die(idx)
                                        print(f"{companion} moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                                    else:  # treasure
                                        game_state.use_treasure(idx)
                                        print(f"{companion.name} used and returned to treasure pool after defeating {len(selected_monsters)} {selected_type}(s).")
                                    
                                    return True
                            else:
                                # Normal Champion behavior (no Expert Bard or no second monster type available)
                                if source == "party":
                                    game_state.use_party_die(idx)
                                    print(f"{companion} moved to Graveyard after defeating {len(selected_monsters)} {selected_type}(s).")
                                else:  # treasure
                                    game_state.use_treasure(idx)
                                    print(f"{companion.name} used and returned to treasure pool after defeating {len(selected_monsters)} {selected_type}(s).")
                                
                                return True
                        else:
                            print("Invalid choice.")
                            return False
                    except ValueError:
                        print("Invalid input.")
                        return False
                
                # Find monsters this companion can defeat
                defeatable_monsters = []
                for monster in monsters:
                    if MonsterPhase.can_defeat_monster(companion_type, monster):
                        defeatable_monsters.append(monster)
                
                if not defeatable_monsters:
                    print(f"{companion_type} cannot defeat any of the remaining monsters!")
                    return False
                
                # Handle different companion types according to the rules
                if companion_type == PartyDiceFace.FIGHTER.value:
                    # Fighter defeats one Skeleton, one Ooze, or any number of Goblins
                    goblins = [m for m in defeatable_monsters if m == DungeonDiceFace.GOBLIN.value]
                    skeletons = [m for m in defeatable_monsters if m == DungeonDiceFace.SKELETON.value]
                    oozes = [m for m in defeatable_monsters if m == DungeonDiceFace.OOZE.value]
                    
                    print(f"\nFighter can:")
                    options = []
                    if goblins:
                        options.append(f"1. Defeat ALL Goblins ({len(goblins)} monster(s))")
                    if skeletons:
                        options.append(f"2. Defeat 1 Skeleton")
                    if oozes:
                        options.append(f"3. Defeat 1 Ooze")
                    
                    for option in options:
                        print(f"  {option}")
                    
                    choice = input("Choose option (number): ").strip()
                    try:
                        choice_idx = int(choice)
                        if choice_idx == 1 and goblins:
                            # Defeat all Goblins
                            for monster in goblins:
                                game_state.dungeon_dice.remove(monster)
                                monsters.remove(monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard after defeating {len(goblins)} Goblin(s).")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool after defeating {len(goblins)} Goblin(s).")
                            
                            print(f"Defeated {len(goblins)} Goblin(s)!")
                            return True
                        elif choice_idx == 2 and skeletons:
                            # Defeat 1 Skeleton
                            defeated_monster = skeletons[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        elif choice_idx == 3 and oozes:
                            # Defeat 1 Ooze
                            defeated_monster = oozes[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        else:
                            print("Invalid choice.")
                            return False
                    except ValueError:
                        print("Invalid input.")
                        return False
                        
                elif companion_type == PartyDiceFace.CLERIC.value:
                    # Cleric defeats one Goblin, one Ooze, or any number of Skeletons
                    goblins = [m for m in defeatable_monsters if m == DungeonDiceFace.GOBLIN.value]
                    skeletons = [m for m in defeatable_monsters if m == DungeonDiceFace.SKELETON.value]
                    oozes = [m for m in defeatable_monsters if m == DungeonDiceFace.OOZE.value]
                    
                    print(f"\nCleric can:")
                    options = []
                    if skeletons:
                        options.append(f"1. Defeat ALL Skeletons ({len(skeletons)} monster(s))")
                    if goblins:
                        options.append(f"2. Defeat 1 Goblin")
                    if oozes:
                        options.append(f"3. Defeat 1 Ooze")
                    
                    for option in options:
                        print(f"  {option}")
                    
                    choice = input("Choose option (number): ").strip()
                    try:
                        choice_idx = int(choice)
                        if choice_idx == 1 and skeletons:
                            # Defeat all Skeletons
                            for monster in skeletons:
                                game_state.dungeon_dice.remove(monster)
                                monsters.remove(monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard after defeating {len(skeletons)} Skeleton(s).")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool after defeating {len(skeletons)} Skeleton(s).")
                            
                            print(f"Defeated {len(skeletons)} Skeleton(s)!")
                            return True
                        elif choice_idx == 2 and goblins:
                            # Defeat 1 Goblin
                            defeated_monster = goblins[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        elif choice_idx == 3 and oozes:
                            # Defeat 1 Ooze
                            defeated_monster = oozes[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        else:
                            print("Invalid choice.")
                            return False
                    except ValueError:
                        print("Invalid input.")
                        return False
                        
                elif companion_type == PartyDiceFace.MAGE.value:
                    # Mage defeats one Goblin, one Skeleton, or any number of Oozes
                    goblins = [m for m in defeatable_monsters if m == DungeonDiceFace.GOBLIN.value]
                    skeletons = [m for m in defeatable_monsters if m == DungeonDiceFace.SKELETON.value]
                    oozes = [m for m in defeatable_monsters if m == DungeonDiceFace.OOZE.value]
                    
                    print(f"\nMage can:")
                    options = []
                    if oozes:
                        options.append(f"1. Defeat ALL Oozes ({len(oozes)} monster(s))")
                    if goblins:
                        options.append(f"2. Defeat 1 Goblin")
                    if skeletons:
                        options.append(f"3. Defeat 1 Skeleton")
                    
                    for option in options:
                        print(f"  {option}")
                    
                    choice = input("Choose option (number): ").strip()
                    try:
                        choice_idx = int(choice)
                        if choice_idx == 1 and oozes:
                            # Defeat all Oozes
                            for monster in oozes:
                                game_state.dungeon_dice.remove(monster)
                                monsters.remove(monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard after defeating {len(oozes)} Ooze(s).")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool after defeating {len(oozes)} Ooze(s).")
                            
                            print(f"Defeated {len(oozes)} Ooze(s)!")
                            return True
                        elif choice_idx == 2 and goblins:
                            # Defeat 1 Goblin
                            defeated_monster = goblins[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        elif choice_idx == 3 and skeletons:
                            # Defeat 1 Skeleton
                            defeated_monster = skeletons[0]
                            game_state.dungeon_dice.remove(defeated_monster)
                            monsters.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        else:
                            print("Invalid choice.")
                            return False
                    except ValueError:
                        print("Invalid input.")
                        return False
                        
                else:
                    # For Thieves and other companions, they can only defeat one monster
                    print(f"\n{companion_type} can defeat:")
                    for i, monster in enumerate(defeatable_monsters):
                        print(f"{i+1}. {monster}")
                    
                    monster_choice = input("Choose monster to defeat (number): ").strip()
                    try:
                        monster_idx = int(monster_choice) - 1
                        if 0 <= monster_idx < len(defeatable_monsters):
                            defeated_monster = defeatable_monsters[monster_idx]
                            
                            # Remove monster from dungeon dice
                            game_state.dungeon_dice.remove(defeated_monster)
                            
                            # Use companion
                            if source == "party":
                                game_state.use_party_die(idx)
                                print(f"{companion} moved to Graveyard.")
                            else:  # treasure
                                game_state.use_treasure(idx)
                                print(f"{companion.name} used and returned to treasure pool.")
                            
                            print(f"Defeated {defeated_monster}!")
                            return True
                        else:
                            print("Invalid choice.")
                            return False
                    except ValueError:
                        print("Invalid input.")
                        return False
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False
    
    @staticmethod
    def can_defeat_monster(companion_type, monster_type):
        """Check if a companion can defeat a specific monster type."""
        if companion_type == PartyDiceFace.CHAMPION.value:
            return True  # Champions can defeat any monster
        
        if monster_type == DungeonDiceFace.GOBLIN.value:
            return companion_type in [PartyDiceFace.FIGHTER.value, PartyDiceFace.CLERIC.value, PartyDiceFace.MAGE.value, PartyDiceFace.THIEF.value]
        elif monster_type == DungeonDiceFace.SKELETON.value:
            return companion_type in [PartyDiceFace.FIGHTER.value, PartyDiceFace.CLERIC.value, PartyDiceFace.MAGE.value, PartyDiceFace.THIEF.value]
        elif monster_type == DungeonDiceFace.OOZE.value:
            return companion_type in [PartyDiceFace.FIGHTER.value, PartyDiceFace.CLERIC.value, PartyDiceFace.MAGE.value, PartyDiceFace.THIEF.value]
        
        return False
    
    @staticmethod
    def can_defeat_monsters(game_state, monsters, hero_card, specialty_active):
        """Check if all monsters can be defeated with available companions."""
        if not monsters:
            return True
        
        # Create a copy of available companions
        available_companions = []
        
        # Add party dice companions
        for i, die in enumerate(game_state.party_dice):
            if die != PartyDiceFace.SCROLL.value:  # Scrolls are not companions
                available_companions.append(("party", i, die))
        
        # Add treasure companions
        treasure_companions = game_state.get_usable_companions()
        for idx, token in treasure_companions:
            available_companions.append(("treasure", idx, token))
        
        if not available_companions:
            return False
        
        # Create a copy of monsters to simulate defeat
        remaining_monsters = monsters.copy()
        
        # Try to defeat monsters using available companions
        for source, idx, companion in available_companions:
            if not remaining_monsters:
                break
            
            # Determine companion type
            if source == "treasure":
                companion_type = companion.get_companion_type()
            else:
                companion_type = companion
            
            # Apply specialty transformations
            if specialty_active:
                if companion_type == PartyDiceFace.THIEF.value:
                    companion_type = PartyDiceFace.MAGE.value
                elif companion_type == PartyDiceFace.MAGE.value:
                    companion_type = PartyDiceFace.THIEF.value
            
            # Find monsters this companion can defeat
            defeatable_monsters = [m for m in remaining_monsters if MonsterPhase.can_defeat_monster(companion_type, m)]
            
            if defeatable_monsters:
                if companion_type == PartyDiceFace.CHAMPION.value:
                    # Champions can defeat any number of monsters of a given type
                    # For simulation, just remove one monster (the actual implementation will handle multiple)
                    remaining_monsters.remove(defeatable_monsters[0])
                elif companion_type == PartyDiceFace.FIGHTER.value:
                    # Fighter defeats one Skeleton, one Ooze, or any number of Goblins
                    goblins = [m for m in defeatable_monsters if m == DungeonDiceFace.GOBLIN.value]
                    if goblins:
                        # Remove all Goblins
                        for monster in goblins:
                            remaining_monsters.remove(monster)
                    else:
                        # Defeat one monster of any type they can handle
                        remaining_monsters.remove(defeatable_monsters[0])
                elif companion_type == PartyDiceFace.CLERIC.value:
                    # Cleric defeats one Goblin, one Ooze, or any number of Skeletons
                    skeletons = [m for m in defeatable_monsters if m == DungeonDiceFace.SKELETON.value]
                    if skeletons:
                        # Remove all Skeletons
                        for monster in skeletons:
                            remaining_monsters.remove(monster)
                    else:
                        # Defeat one monster of any type they can handle
                        remaining_monsters.remove(defeatable_monsters[0])
                elif companion_type == PartyDiceFace.MAGE.value:
                    # Mage defeats one Goblin, one Skeleton, or any number of Oozes
                    oozes = [m for m in defeatable_monsters if m == DungeonDiceFace.OOZE.value]
                    if oozes:
                        # Remove all Oozes
                        for monster in oozes:
                            remaining_monsters.remove(monster)
                    else:
                        # Defeat one monster of any type they can handle
                        remaining_monsters.remove(defeatable_monsters[0])
                else:
                    # Other companions (like Thieves) can only defeat one monster
                    remaining_monsters.remove(defeatable_monsters[0])
        
        return len(remaining_monsters) == 0
    
    @staticmethod
    def use_companions_for_remaining_monsters(game_state, monsters, hero_card, specialty_active):
        """Automatically use companions to defeat remaining monsters."""
        if not monsters:
            return True
        
        print("\n🤖 Automatically defeating remaining monsters...")
        
        # Create a copy of available companions
        available_companions = []
        
        # Add party dice companions
        for i, die in enumerate(game_state.party_dice):
            if die != PartyDiceFace.SCROLL.value:  # Scrolls are not companions
                available_companions.append(("party", i, die))
        
        # Add treasure companions
        treasure_companions = game_state.get_usable_companions()
        for idx, token in treasure_companions:
            available_companions.append(("treasure", idx, token))
        
        if not available_companions:
            return False
        
        # Try to defeat monsters using available companions
        for source, idx, companion in available_companions:
            if not monsters:
                break
            
            # Determine companion type
            if source == "treasure":
                companion_type = companion.get_companion_type()
            else:
                companion_type = companion
            
            # Apply specialty transformations
            if specialty_active:
                if companion_type == PartyDiceFace.THIEF.value:
                    companion_type = PartyDiceFace.MAGE.value
                elif companion_type == PartyDiceFace.MAGE.value:
                    companion_type = PartyDiceFace.THIEF.value
            
            # Find monsters this companion can defeat
            defeatable_monsters = [m for m in monsters if MonsterPhase.can_defeat_monster(companion_type, m)]
            
            if defeatable_monsters:
                if companion_type == PartyDiceFace.CHAMPION.value:
                    # Champions can defeat any number of monsters of a given type
                    # For automatic defeat, just defeat one monster (the actual implementation will handle multiple)
                    defeated_monster = defeatable_monsters[0]
                    game_state.dungeon_dice.remove(defeated_monster)
                    monsters.remove(defeated_monster)
                    
                    # Use companion
                    if source == "party":
                        game_state.use_party_die(idx)
                        print(f"{companion} moved to Graveyard after defeating {defeated_monster}.")
                    else:  # treasure
                        game_state.use_treasure(idx)
                        print(f"{companion.name} used and returned to treasure pool after defeating {defeated_monster}.")
                    
                elif companion_type == PartyDiceFace.FIGHTER.value:
                    # Fighter defeats one Skeleton, one Ooze, or any number of Goblins
                    goblins = [m for m in defeatable_monsters if m == DungeonDiceFace.GOBLIN.value]
                    if goblins:
                        # Defeat all Goblins
                        for monster in goblins:
                            game_state.dungeon_dice.remove(monster)
                            monsters.remove(monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {len(goblins)} Goblin(s).")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {len(goblins)} Goblin(s).")
                    else:
                        # Defeat one monster of any type they can handle
                        defeated_monster = defeatable_monsters[0]
                        game_state.dungeon_dice.remove(defeated_monster)
                        monsters.remove(defeated_monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {defeated_monster}.")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {defeated_monster}.")
                    
                elif companion_type == PartyDiceFace.CLERIC.value:
                    # Cleric defeats one Goblin, one Ooze, or any number of Skeletons
                    skeletons = [m for m in defeatable_monsters if m == DungeonDiceFace.SKELETON.value]
                    if skeletons:
                        # Defeat all Skeletons
                        for monster in skeletons:
                            game_state.dungeon_dice.remove(monster)
                            monsters.remove(monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {len(skeletons)} Skeleton(s).")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {len(skeletons)} Skeleton(s).")
                    else:
                        # Defeat one monster of any type they can handle
                        defeated_monster = defeatable_monsters[0]
                        game_state.dungeon_dice.remove(defeated_monster)
                        monsters.remove(defeated_monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {defeated_monster}.")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {defeated_monster}.")
                    
                elif companion_type == PartyDiceFace.MAGE.value:
                    # Mage defeats one Goblin, one Skeleton, or any number of Oozes
                    oozes = [m for m in defeatable_monsters if m == DungeonDiceFace.OOZE.value]
                    if oozes:
                        # Defeat all Oozes
                        for monster in oozes:
                            game_state.dungeon_dice.remove(monster)
                            monsters.remove(monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {len(oozes)} Ooze(s).")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {len(oozes)} Ooze(s).")
                    else:
                        # Defeat one monster of any type they can handle
                        defeated_monster = defeatable_monsters[0]
                        game_state.dungeon_dice.remove(defeated_monster)
                        monsters.remove(defeated_monster)
                        
                        # Use companion
                        if source == "party":
                            game_state.use_party_die(idx)
                            print(f"{companion} moved to Graveyard after defeating {defeated_monster}.")
                        else:  # treasure
                            game_state.use_treasure(idx)
                            print(f"{companion.name} used and returned to treasure pool after defeating {defeated_monster}.")
                    
                else:
                    # Other companions (like Thieves) can only defeat one monster
                    defeated_monster = defeatable_monsters[0]
                    game_state.dungeon_dice.remove(defeated_monster)
                    monsters.remove(defeated_monster)
                    
                    # Use companion
                    if source == "party":
                        game_state.use_party_die(idx)
                        print(f"{companion} moved to Graveyard after defeating {defeated_monster}.")
                    else:  # treasure
                        game_state.use_treasure(idx)
                        print(f"{companion.name} used and returned to treasure pool after defeating {defeated_monster}.")
        
        return len(monsters) == 0 