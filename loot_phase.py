from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from hero import HeroRank
from treasure import TreasureType
import random

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
        print("- Thieves and Champions can open all of the Chests")
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
                
                # Automatically open all available chests
                num_chests = max_chests
                
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
                        game_state.player_treasure.add_treasure(treasure)
                        game_state.treasure_tokens += 1  # Update display counter
                        print(f"\n💎 TREASURE FOUND: {treasure.name} 💎")
                        print(f"📜 Effect: {treasure.get_description()}")
                        
                        # If it's a companion-type treasure, show it in the party section
                        if treasure.can_use_as_companion():
                            print(f"🎯 This treasure can be used as a {treasure.get_companion_type()} in your party!")
                    else:
                        # If no treasure tokens remain, gain experience instead
                        game_state.experience_tokens += 1
                        print(f"\n💫 NO TREASURE REMAINS! 💫")
                        print("You gain an Experience token instead.")
                
                print(f"\nTotal Experience tokens: {game_state.experience_tokens}")
                print(f"Total Treasure tokens: {game_state.treasure_tokens}")
                
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
        
        # Check if Thaumaturge ultimate is available and can recover more dice
        if (game_state.selected_hero_card.__class__.__name__ == "AlchemistThaumaturgeHero" and 
            game_state.selected_hero_card.current_rank.value == "Master" and 
            not game_state.selected_hero_card.is_exhausted):
            print("Each Potion allows you to recover one die from the Graveyard.")
            print("💫 Thaumaturge Ultimate Available: Can recover 2 dice with Transformation Potion!")
        else:
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
                # Automatically quaff all available potions
                max_potions = min(available_potions, len(game_state.graveyard))
                print(f"\nYou can recover up to {max_potions} dice from the Graveyard.")
                num_potions = max_potions
                
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
                            print(f"Recovered a {chosen_face}!")
                            
                            # Remove potion from dungeon dice
                            game_state.dungeon_dice.remove(DungeonDiceFace.POTION.value)
                            available_potions -= 1
                        else:
                            print("Invalid choice.")
                            return available_potions
                    except ValueError:
                        print("Invalid input.")
                        return available_potions
                
                print(f"\nTotal Experience tokens: {game_state.experience_tokens}")
                print(f"Total Treasure tokens: {game_state.treasure_tokens}")
                
                return available_potions
            else:
                print("Invalid choice.")
                return available_potions
        except ValueError:
            print("Invalid input.")
            return available_potions 