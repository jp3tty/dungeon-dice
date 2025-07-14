import random
import os
import time
from enum import Enum
from hero import HeroRank, MinstrelBardHero, AlchemistThaumaturgeHero, ArchaeologistTombRaiderHero
from dice import PartyDiceFace, DungeonDiceFace, DiceManager

def clear_screen():
    """Clear the terminal screen using ANSI escape codes and newlines."""
    print("\n" * 3)  # Print just a few newlines for better spacing
    print("\033[2J\033[H", end="")  # ANSI escape sequence to clear screen and move cursor to top
    print("\n")  # Just one newline for padding

class PartyDiceFace(Enum):
    FIGHTER = "Fighter"
    MAGE = "Mage"
    CLERIC = "Cleric"
    THIEF = "Thief"
    CHAMPION = "Champion"
    SCROLL = "Scroll"

class HeroCard:
    def __init__(self, novice_name, master_name, novice_specialty, master_specialty, 
                 novice_ultimate, master_ultimate, xp_to_master=5):
        self.novice_name = novice_name
        self.master_name = master_name
        self.novice_specialty = novice_specialty
        self.master_specialty = master_specialty
        self.novice_ultimate = novice_ultimate
        self.master_ultimate = master_ultimate
        self.xp_to_master = xp_to_master
        
        # Current state
        self.current_rank = HeroRank.NOVICE
        self.is_exhausted = False
    
    @property
    def name(self):
        return self.master_name if self.current_rank == HeroRank.MASTER else self.novice_name
    
    @property
    def specialty(self):
        return self.master_specialty if self.current_rank == HeroRank.MASTER else self.novice_specialty
    
    @property
    def ultimate(self):
        return self.master_ultimate if self.current_rank == HeroRank.MASTER else self.novice_ultimate
    
    def check_level_up(self, xp):
        """Check if hero can level up based on XP"""
        if self.current_rank == HeroRank.NOVICE and xp >= self.xp_to_master:
            self.current_rank = HeroRank.MASTER
            print(f"Your hero has ascended from {self.novice_name} to {self.master_name}!")
            print(f"New Specialty: {self.master_specialty}")
            return True
        return False
    
    def use_specialty(self, game_state):
        """Use the hero's specialty ability based on current rank"""
        print(f"Using {self.name}'s specialty: {self.specialty}")
        # Implementation specific to each hero will be in subclasses
        return False
    
    def use_ultimate(self, game_state):
        """Use the hero's ultimate ability based on current rank"""
        if not self.is_exhausted:
            print(f"Using {self.name}'s ultimate ability: {self.ultimate}")
            self.is_exhausted = True
            # Implementation specific to each hero will be in subclasses
            return True
        else:
            print(f"{self.name}'s ultimate ability is exhausted!")
            return False
    
    def refresh(self):
        """Refresh the hero card"""
        if self.is_exhausted:
            self.is_exhausted = False
            print(f"{self.name}'s ultimate ability is now refreshed!")
            return True
        return False
    
    def display_card_info(self):
        """Display detailed hero card information"""
        rank_text = "✨ MASTER ✨" if self.current_rank == HeroRank.MASTER else "NOVICE"
        print(f"\n{'='*50}")
        print(f"📜 {self.name} ({rank_text}) 📜".center(50))
        print(f"{'='*50}")
        print(f"🔮 Specialty: {self.specialty}")
        print(f"⚡ Ultimate: {self.ultimate}")
        status = "❌ EXHAUSTED" if self.is_exhausted else "✅ READY"
        print(f"📋 Status: {status}")
        if self.current_rank == HeroRank.NOVICE:
            print(f"📈 XP needed to master: {self.xp_to_master}")
        print("-"*50)


class MinstrelBardHero(HeroCard):
    def __init__(self):
        super().__init__(
            novice_name="Minstrel",
            master_name="Bard",
            novice_specialty="Thieves may be used as Mages and Mages may be used as Thieves.",
            master_specialty="Thieves may be used as Mages and Mages may be used as Thieves. Champions defeat 1 extra monster.",
            novice_ultimate="Discard all dice from the Dragon's Lair.",
            master_ultimate="Discard all dice from the Dragon's Lair.",
            xp_to_master=5
        )
    
    def use_ultimate(self, game_state):
        """Discard all dice from the Dragon's Lair"""
        if super().use_ultimate(game_state):
            dragon_count = len(game_state.dragons_lair)
            if dragon_count > 0:
                print(f"The {self.name} plays a powerful melody, banishing {dragon_count} dragons!")
                game_state.dragons_lair = []
                return True
            else:
                print("There are no dragons in the Dragon's Lair.")
                # Don't exhaust the hero if there were no dragons
                self.is_exhausted = False
                return False
        return False

class GameState:
    def __init__(self):
        self.delve_count = 0
        self.level = 1
        self.party_dice = []
        self.dungeon_dice = []
        self.dragons_lair = []  # Stores dragon dice separately
        self.treasure_tokens = 0
        self.experience_tokens = 0
        self.selected_hero_card = None
        self.current_phase = None
        self.graveyard = []

class DungeonDiceGame:
    def __init__(self):
        self.state = GameState()
        self.dice_manager = DiceManager()  # Initialize the dice manager
        self.MAX_DELVES = 3
        self.MAX_PARTY_DICE = 7
        self.MAX_DUNGEON_DICE = 7
        self.MAX_LEVEL = 10
        self.available_hero_cards = self.initialize_hero_cards()
        
    def initialize_hero_cards(self):
        """Initialize available hero cards"""
        return [MinstrelBardHero(), AlchemistThaumaturgeHero(), ArchaeologistTombRaiderHero()]
        
    def start_game(self):
        """Start a new game with 3 delves."""
        clear_screen()
        print("\n" + "="*50)
        print("🎲 WELCOME TO DUNGEON DICE 🎲".center(50))
        print("="*50)
        print("\nPrepare yourself for an epic adventure!")
        print("You have 3 delves to prove your worth, gather treasure,")
        print("and become a legendary hero!\n")
        
        # Choose a hero card
        print("Available Heroes:")
        for i, hero in enumerate(self.available_hero_cards, 1):
            print(f"\n{i}) {hero.novice_name}/{hero.master_name}")
            print(f"   Specialty: {hero.novice_specialty}")
            print(f"   Novice Ability: {hero.novice_ultimate}")
            print(f"   Master Ability: {hero.master_ultimate}")
        
        while True:
            try:
                choice = int(input("\nChoose your hero (number): ").strip())
                if 1 <= choice <= len(self.available_hero_cards):
                    self.state.selected_hero_card = self.available_hero_cards[choice - 1]
                    clear_screen()  # Clear screen after selection
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.available_hero_cards)}")
            except ValueError:
                print("Please enter a valid number")
        
        self.state.delve_count = 0
        self.state.treasure_tokens = 0
        self.state.experience_tokens = 0
        
        # Main game loop - 3 delves
        while self.state.delve_count < self.MAX_DELVES:
            print(f"\n{'='*50}")
            print(f"🗡️  DELVE {self.state.delve_count + 1} OF {self.MAX_DELVES}  🗡️".center(50))
            print(f"{'='*50}")
            
            self.start_delve()
            
            # Check for hero level up between delves
            if (self.state.selected_hero_card.current_rank == HeroRank.NOVICE and 
                self.state.experience_tokens >= self.state.selected_hero_card.xp_to_master):
                self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
            
            # Show progress after each delve
            print(f"\n📊 End of Delve {self.state.delve_count} Summary:")
            print(f"🌟 Experience: {self.state.experience_tokens} tokens")
            print(f"💎 Treasure: {self.state.treasure_tokens} tokens")
        
        self.end_game()
    
    def start_delve(self):
        """Start a new delve (one game round) with proper setup."""
        clear_screen()
        self.state.delve_count += 1
        
        # Setup phase
        self.setup_delve()
        self.display_game_state()
        print(f"\n=== Starting Delve {self.state.delve_count} ===")
        
        # Continue until the delve is over (player chooses to end or fails)
        delve_active = True
        while delve_active:
            # Monster Phase
            monster_result = self.monster_phase()
            if not monster_result:
                print("The monsters were too powerful! Delve ends.")
                break
                
            # Loot Phase
            self.loot_phase()
            
            # Dragon Phase if dragons are present
            if self.state.dragons_lair:
                dragon_result = self.dragon_phase()
                if not dragon_result:
                    # Dragon phase might end the delve based on the result
                    break
            
            # Regroup Phase - player decides whether to continue or end delve
            regroup_result = self.regroup_phase()
            if not regroup_result:
                print("You've chosen to end this delve.")
                delve_active = False
    
    def setup_delve(self):
        """Set up for a new delve following the 4 steps described."""
        print("\n--- SETUP PHASE ---")
        
        # Step 1: Roll all 7 Party Dice
        print("Rolling 7 Party Dice to form your starting party...")
        self.state.party_dice = self.roll_party_dice(self.MAX_PARTY_DICE)
        # Reset graveyard
        self.state.graveyard = []
        
        # Step 2: Apply hero's formation specialty
        if self.state.selected_hero_card:
            self.state.selected_hero_card.apply_formation_specialty(self.state)
        
        # Step 3: Refresh Hero Card if exhausted
        if self.state.selected_hero_card and self.state.selected_hero_card.is_exhausted:
            self.state.selected_hero_card.refresh()
        
        # Step 3: Set Level Die to 1
        self.state.level = 1
        
        # Step 4: Roll 1 Dungeon Die to populate the dungeon
        print("\nRolling 1 Dungeon Die to populate the dungeon...")
        initial_roll = self.dice_manager.roll_dungeon_dice(1)  # This returns a list
        if not initial_roll:  # Safety check
            print("Error: No dice were rolled!")
            return
            
        die_result = initial_roll[0]  # Get the first (and only) die result
        print(f"Rolled a {die_result}!")
        
        # Handle the roll appropriately
        if die_result == DungeonDiceFace.DRAGON.value:
            self.state.dragons_lair.append(die_result)
            print("The Dragon moves to the Dragon's Lair!")
            self.state.dungeon_dice = []  # No dice in dungeon area
        else:
            self.state.dungeon_dice = [die_result]  # Place die in dungeon area
        
        # Display the result
        if self.state.dungeon_dice:
            print(f"Dungeon Area: {', '.join(self.state.dungeon_dice)}")
        if self.state.dragons_lair:
            print(f"Dragon's Lair: {len(self.state.dragons_lair)} Dragon(s)")
            
        # Reset dragon's lair if empty (for clarity)
        if not self.state.dragons_lair:
            self.state.dragons_lair = []
    
    def roll_party_dice(self, num_dice=7):
        """Roll the white party dice."""
        return self.dice_manager.roll_party_dice(num_dice)
    
    def roll_dungeon_dice(self, num_dice=1):
        """Roll the black dungeon dice, handling dragons specially."""
        result = []
        
        # Roll the dice using the dice manager
        new_dice = self.dice_manager.roll_dungeon_dice(num_dice)
        
        # Process each die
        for die in new_dice:
            if die == DungeonDiceFace.DRAGON.value:
                # Dragon dice go to the Dragon's Lair
                self.state.dragons_lair.append(die)
                print("A Dragon appears! The die is moved to the Dragon's Lair.")
            else:
                result.append(die)
                print(f"Rolled a {die}!")
        
        return result
    
    def print_party_dice(self):
        """Display the party dice."""
        print("\nYour Party:")
        
        # Count dice by type for cleaner display
        dice_counts = {}
        for die in self.state.party_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
        
        for die_face, count in dice_counts.items():
            print(f"- {die_face}: {count} dice")
    
    def print_dungeon_dice(self):
        """Display the dungeon dice and dragon's lair."""
        print("\nDungeon Encounter:")
        
        if not self.state.dungeon_dice:
            print("- No dungeon dice present")
        else:
            # Count dice by type for cleaner display
            dice_counts = {}
            for die in self.state.dungeon_dice:
                dice_counts[die] = dice_counts.get(die, 0) + 1
            
            for die_face, count in dice_counts.items():
                print(f"- {die_face}: {count} dice")
        
        if self.state.dragons_lair:
            print("\nDragon's Lair:")
            print(f"- Dragon: {len(self.state.dragons_lair)} dice")
        elif self.state.current_phase == "Dragon Phase":
            print("\nDragon's Lair: Empty")
    
    def display_game_state(self):
        """Display the current state of the game."""
        print(f"\n{'='*50}")
        print(f"🎲 DUNGEON DICE - DELVE {self.state.delve_count} OF {self.MAX_DELVES} 🎲".center(50))
        print(f"{'='*50}")
        print(f"\n📊 Current Status:")
        print(f"🌟 Experience: {self.state.experience_tokens} tokens")
        print(f"💎 Treasure: {self.state.treasure_tokens} tokens")
        print(f"📈 Dungeon Level: {self.state.level}")
        
        # Display hero info
        self.state.selected_hero_card.display_card_info()
        
        # Display dice info
        self.print_party_dice()
        self.print_dungeon_dice()
        print(f"\n{'-'*50}\n")

    def monster_phase(self):
        """Monster Phase: Adventurers fight monsters."""
        clear_screen()
        self.state.current_phase = "Monster Phase"
        self.display_game_state()
        print("\n--- MONSTER PHASE ---")
        
        # Process monster encounters
        monsters = [die for die in self.state.dungeon_dice if die in 
                   [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
        
        if monsters:
            print(f"\nEncountered {len(monsters)} monsters!")
            
            # Specialty is now always active
            if self.can_defeat_monsters(monsters, True):  # Always pass True for using_specialty
                print("Your party successfully defeats all monsters!")
                # Remove monsters from dungeon dice
                for monster in monsters:
                    self.state.dungeon_dice.remove(monster)
                
                # Gain experience for defeating monsters
                exp_gained = len(monsters)
                self.state.experience_tokens += exp_gained
                print(f"Gained {exp_gained} experience tokens! Total: {self.state.experience_tokens}")
                
                # Check for hero level-up
                if (self.state.selected_hero_card.current_rank == HeroRank.NOVICE and 
                    self.state.experience_tokens >= self.state.selected_hero_card.xp_to_master):
                    self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
                
                return True
            else:
                print("Your party cannot defeat all monsters!")
                
                # Give player option to use hero ultimate ability
                if not self.state.selected_hero_card.is_exhausted:
                    use_ultimate = input(f"Use {self.state.selected_hero_card.name}'s ultimate ability? (y/n): ").lower().strip()
                    if use_ultimate == 'y':
                        # For Minstrel/Bard, the ultimate clears dragons, not helps with monsters
                        self.state.selected_hero_card.use_ultimate(self.state)
                        
                        # Recheck monster combat with specialty always active
                        if self.can_defeat_monsters(monsters, True):  # Always pass True for using_specialty
                            print("Your party now defeats the monsters!")
                            # Remove monsters from dungeon dice
                            for monster in monsters:
                                self.state.dungeon_dice.remove(monster)
                            
                            # Gain experience for defeating monsters
                            exp_gained = len(monsters)
                            self.state.experience_tokens += exp_gained
                            print(f"Gained {exp_gained} experience tokens! Total: {self.state.experience_tokens}")
                            return True
                
                # Use a potion as a last resort
                potions = self.state.dungeon_dice.count(DungeonDiceFace.POTION.value)
                if potions > 0:
                    use_potion = input("Use a potion to help defeat monsters? (y/n): ").lower().strip()
                    if use_potion == 'y':
                        self.quaff_potion()
                        self.state.dungeon_dice.remove(DungeonDiceFace.POTION.value)
                        
                        # Final check if monsters can be defeated
                        if self.can_defeat_monsters(monsters, True):  # Always pass True for using_specialty
                            print("With the potion's help, your party defeats the monsters!")
                            # Remove monsters from dungeon dice
                            for monster in monsters:
                                self.state.dungeon_dice.remove(monster)
                            
                            # Gain experience for defeating monsters
                            exp_gained = len(monsters)
                            self.state.experience_tokens += exp_gained
                            print(f"Gained {exp_gained} experience tokens! Total: {self.state.experience_tokens}")
                            return True
                
                return False
        else:
            print("No monsters encountered in this phase.")
            return True
    
    def can_defeat_monsters(self, monsters, using_specialty=False):
        """Check if the party can defeat the monsters encountered."""
        # Count heroes by type
        fighters = self.state.party_dice.count(PartyDiceFace.FIGHTER.value)
        clerics = self.state.party_dice.count(PartyDiceFace.CLERIC.value)
        mages = self.state.party_dice.count(PartyDiceFace.MAGE.value)
        thieves = self.state.party_dice.count(PartyDiceFace.THIEF.value)
        champions = self.state.party_dice.count(PartyDiceFace.CHAMPION.value)
        
        # Apply Minstrel/Bard specialty if active
        if using_specialty:
            # Thieves may be used as Mages and Mages may be used as Thieves
            # For simplicity, we'll just combine their counts for effectiveness
            combined_mages_thieves = mages + thieves
            mages = combined_mages_thieves
            thieves = combined_mages_thieves
            
            # If Bard (Master), Champions defeat 1 extra monster
            if self.state.selected_hero_card.current_rank == HeroRank.MASTER:
                # Each champion counts as two for monster defeat
                champions *= 2
        
        # Count monsters by type
        goblins = monsters.count(DungeonDiceFace.GOBLIN.value)
        skeletons = monsters.count(DungeonDiceFace.SKELETON.value)
        oozes = monsters.count(DungeonDiceFace.OOZE.value)
        
        # Champions can defeat any monster
        monsters_champions_can_defeat = min(champions, goblins + skeletons + oozes)
        remaining_goblins = max(0, goblins - monsters_champions_can_defeat)
        remaining_skeletons = max(0, skeletons - monsters_champions_can_defeat)
        remaining_oozes = max(0, oozes - monsters_champions_can_defeat)
        
        # Fighters are good against goblins
        goblins_defeated_by_fighters = min(fighters, remaining_goblins)
        remaining_goblins -= goblins_defeated_by_fighters
        
        # Clerics are good against skeletons
        skeletons_defeated_by_clerics = min(clerics, remaining_skeletons)
        remaining_skeletons -= skeletons_defeated_by_clerics
        
        # Mages are good against oozes
        oozes_defeated_by_mages = min(mages, remaining_oozes)
        remaining_oozes -= oozes_defeated_by_mages
        
        # Thieves can defeat one of any monster
        monsters_thieves_can_defeat = min(thieves, remaining_goblins + remaining_skeletons + remaining_oozes)
        
        # Total monsters remaining
        total_remaining = remaining_goblins + remaining_skeletons + remaining_oozes - monsters_thieves_can_defeat
        
        return total_remaining <= 0
    
    def loot_phase(self):
        """Loot Phase: Open Chests or Quaff Potions (up to two actions)."""
        clear_screen()
        self.state.current_phase = "Loot Phase"
        self.display_game_state()
        print("\n--- LOOT PHASE ---")
        
        # If Alchemist/Thaumaturge is active, convert all chests to potions
        if isinstance(self.state.selected_hero_card, AlchemistThaumaturgeHero):
            chest_indices = [i for i, die in enumerate(self.state.dungeon_dice) 
                           if die == DungeonDiceFace.CHEST.value]
            if chest_indices:
                for idx in chest_indices:
                    self.state.dungeon_dice[idx] = DungeonDiceFace.POTION.value
                print(f"The {self.state.selected_hero_card.name}'s alchemy transforms {len(chest_indices)} chest(s) into potions!")
        
        # Count available chests and potions
        chests = self.state.dungeon_dice.count(DungeonDiceFace.CHEST.value)
        potions = self.state.dungeon_dice.count(DungeonDiceFace.POTION.value)
        
        print(f"Available: {chests} chests, {potions} potions")
        
        # Allow up to two actions
        actions_taken = 0
        while actions_taken < 2:
            if chests <= 0 and potions <= 0:
                print("No more items available.")
                break
                
            print(f"\nAction {actions_taken + 1}/2:")
            actions = []
            if chests > 0:
                actions.append("Open Chest")
            if potions > 0:
                actions.append("Quaff Potion")
            actions.append("End Loot Phase")  # Always provide option to end early
            
            for i, act in enumerate(actions):
                print(f"{i+1}. {act}")
                
            choice = input("Choose action (number): ").strip()
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(actions):
                    selected_action = actions[choice_idx]
                    
                    if selected_action == "Open Chest":
                        self.open_chest()
                        chests -= 1
                        # Remove a chest die from dungeon dice
                        self.state.dungeon_dice.remove(DungeonDiceFace.CHEST.value)
                        actions_taken += 1
                    elif selected_action == "Quaff Potion":
                        if self.quaff_potion():  # Only count action if potion was successfully used
                            potions -= 1
                            # Remove a potion die from dungeon dice
                            self.state.dungeon_dice.remove(DungeonDiceFace.POTION.value)
                            actions_taken += 1
                    else:  # End Loot Phase
                        return  # Exit the phase immediately
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def open_chest(self):
        """Open a chest to gain treasure."""
        print("Opening chest...")
        treasure_found = random.randint(1, 3)
        self.state.treasure_tokens += treasure_found
        print(f"You found {treasure_found} treasure! Total treasure: {self.state.treasure_tokens}")
    
    def quaff_potion(self):
        """Use a potion to recover a die from the graveyard."""
        print("Quaffing potion...")
        
        if not self.state.graveyard:
            print("No dice in Graveyard to recover!")
            return False
            
        print("Choose a die face for the recovered Party die:")
        for i, face in enumerate(PartyDiceFace):
            print(f"{i+1}. {face.value}")
        
        face_choice = input("Choose face (number): ").strip()
        try:
            face_idx = int(face_choice) - 1
            if 0 <= face_idx < len(PartyDiceFace):
                # Remove a die from graveyard
                self.state.graveyard.pop()
                # Add new die with chosen face
                chosen_face = list(PartyDiceFace)[face_idx].value
                self.state.party_dice.append(chosen_face)
                print(f"Added a {chosen_face} to your active party!")
                
                # Move potion to graveyard
                self.state.graveyard.append(DungeonDiceFace.POTION.value)
                return True
            else:
                print("Invalid face choice. Using Fighter.")
                self.state.graveyard.pop()
                self.state.party_dice.append(PartyDiceFace.FIGHTER.value)
                
                # Move potion to graveyard
                self.state.graveyard.append(DungeonDiceFace.POTION.value)
                return True
        except ValueError:
            print("Invalid input. Using Fighter.")
            self.state.graveyard.pop()
            self.state.party_dice.append(PartyDiceFace.FIGHTER.value)
            
            # Move potion to graveyard
            self.state.graveyard.append(DungeonDiceFace.POTION.value)
            return True
    
    def dragon_phase(self):
        """Dragon Phase: Occurs if Dragon is attracted to the dungeon."""
        # This method is now a placeholder - Dragon Phase is handled in main.py
        # The actual Dragon Phase mechanics are implemented in main.py DragonPhase class
        if not self.state.dragons_lair:
            return True
            
        # Import and use the DragonPhase from dragon_phase.py
        from dragon_phase import DragonPhase
        return DragonPhase.execute(self.state, self.state.selected_hero_card)
    
    def regroup_phase(self):
        """Regroup Phase: Make decisions after the delve."""
        clear_screen()
        self.state.current_phase = "Regroup Phase"
        self.display_game_state()
        print("\n--- REGROUP PHASE ---")
        # Show number of dragon dice in the lair
        print(f"🐉 Dragon Dice in Lair: {len(self.state.dragons_lair)}")
        
        # Check if level 10 was cleared
        if self.state.level == 10:
            print("\n🏆 STUFF OF LEGEND! 🏆")
            print("You've cleared the dungeon at Level 10!")
            print("This is a legendary achievement!")
            
            # Award experience tokens
            self.state.experience_tokens += 10
            print(f"You gain 10 Experience tokens for this legendary feat!")
            print(f"Total Experience tokens: {self.state.experience_tokens}")
            
            # Return dragons to available pool if any
            if self.state.dragons_lair:
                print(f"\nReturning {len(self.state.dragons_lair)} Dragon dice to the available pool.")
                self.state.dragons_lair = []
            
            return False  # End the delve
        
        print("Choose your regroup action:")
        print("1. Retire to the Tavern (End delve and bank treasure)")
        print("2. Seek Glory (Continue delving to the next level)")
        
        choice = input("Choose action (number): ").strip()
        
        if choice == "1":
            return self.retire_to_tavern()
        else:
            return self.seek_glory()
    
    def seek_glory(self):
        """Continue with the same party to the next level."""
        print("Your party continues their quest for glory!")
        
        # Increase dungeon level
        self.state.level = min(self.state.level + 1, self.MAX_LEVEL)
        print(f"\nProceeding to dungeon level {self.state.level}...")
        
        # Calculate available dice
        total_dungeon_dice = self.MAX_DUNGEON_DICE
        available_dice = total_dungeon_dice - len(self.state.dragons_lair)
        dice_to_roll = min(self.state.level, available_dice)
        
        print(f"\nWARNING! The Dungeon Lord will roll {dice_to_roll} Dungeon dice.")
        print("Once rolled, you must defeat all monsters and possibly the Dragon,")
        print("or you must Flee, gaining NO Experience for this delve!")
        print("There is no turning back once the Dungeon dice are cast!")
        
        proceed = input("\nDo you wish to proceed? (y/n): ").lower().strip()
        if proceed != 'y':
            print("Wise choice. You retire to the tavern.")
            return self.retire_to_tavern()
        
        # Roll dungeon dice
        new_dice = self.roll_dungeon_dice(dice_to_roll)
        self.state.dungeon_dice.extend(new_dice)
        
        return True

    def retire_to_tavern(self):
        """End the delve and bank treasure."""
        print("You retire to the tavern, ending this delve.")
        
        # Award experience based on current level
        exp_gained = self.state.level
        self.state.experience_tokens += exp_gained
        print(f"You gain {exp_gained} Experience tokens for reaching level {self.state.level}!")
        print(f"Total Experience tokens: {self.state.experience_tokens}")
        
        # Bank treasure - in this implementation we just keep it
        banked = self.state.treasure_tokens
        print(f"You've collected {banked} treasure tokens so far.")
        
        # Return dragons to available pool if any
        if self.state.dragons_lair:
            print(f"\nReturning {len(self.state.dragons_lair)} Dragon dice to the available pool.")
            self.state.dragons_lair = []
        
        # End this delve
        return False

    def end_game(self):
        """Handle end game scoring and final display."""
        clear_screen()
        print("\n" + "="*40)
        print("GAME OVER - FINAL SCORING")
        print("="*40)
        
        # Apply hero's end-game specialty
        if self.state.selected_hero_card:
            self.state.selected_hero_card.apply_end_game_specialty(self.state)
        
        # Display hero final state
        print("\n" + "="*50)
        print("📜 Final Hero State 📜".center(50))
        print("="*50)
        print(f"Name: {self.state.selected_hero_card.name}")
        self.state.selected_hero_card.display_card_info()
        print(f"🌟 Experience: {self.state.experience_tokens} tokens")
        print(f"💎 Treasure: {self.state.treasure_tokens} tokens")
        print("-"*50)

if __name__ == "__main__":
    game = DungeonDiceGame()
    game.start_game() 
    