import random
from enum import Enum

class PartyDiceFace(Enum):
    FIGHTER = "Fighter"
    MAGE = "Mage"
    CLERIC = "Cleric"
    THIEF = "Thief"
    CHAMPION = "Champion"
    SCROLL = "Scroll"

class DungeonDiceFace(Enum):
    GOBLIN = "Goblin"
    SKELETON = "Skeleton"
    OOZE = "Ooze"
    DRAGON = "Dragon"
    CHEST = "Chest"
    POTION = "Potion"

class HeroRank(Enum):
    NOVICE = "Novice"
    MASTER = "Master"

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
        self.MAX_DELVES = 3
        self.MAX_PARTY_DICE = 7
        self.MAX_DUNGEON_DICE = 7
        self.MAX_LEVEL = 10
        self.available_hero_cards = self.initialize_hero_cards()
        
    def initialize_hero_cards(self):
        """Initialize available hero cards"""
        return [MinstrelBardHero()]
        
    def start_game(self):
        """Start a new game with 3 delves."""
        print("=== DUNGEON DICE GAME ===")
        print("Setting up the game...")
        
        # Choose a hero card - for now we only have one
        self.state.selected_hero_card = self.available_hero_cards[0]
        print(f"Your hero: {self.state.selected_hero_card.name}")
        self.state.selected_hero_card.display_card_info()
        
        self.state.delve_count = 0
        self.state.treasure_tokens = 0
        self.state.experience_tokens = 0
        
        while self.state.delve_count < self.MAX_DELVES:
            self.start_delve()
            
            # Check for hero level up between delves
            if (self.state.selected_hero_card.current_rank == HeroRank.NOVICE and 
                self.state.experience_tokens >= self.state.selected_hero_card.xp_to_master):
                self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
            
        print(f"\nGame Over! Final Score: {self.state.treasure_tokens} treasure tokens and {self.state.experience_tokens} experience tokens")
    
    def start_delve(self):
        """Start a new delve (one game round) with proper setup."""
        self.state.delve_count += 1
        print(f"\n=== DELVE {self.state.delve_count} ===")
        
        # Setup phase
        self.setup_delve()
        
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
            else:
                # Increase dungeon level for the next round if continuing
                self.state.level = min(self.state.level + 1, self.MAX_LEVEL)
                print(f"Proceeding to dungeon level {self.state.level}...")
                
                # Roll additional dungeon dice based on level
                new_dice = self.roll_dungeon_dice(1)  # Roll 1 die per level
                self.state.dungeon_dice.extend(new_dice)
    
    def setup_delve(self):
        """Set up for a new delve following the 4 steps described."""
        print("\n--- SETUP PHASE ---")
        
        # Step 1: Roll all 7 Party Dice
        self.state.party_dice = self.roll_party_dice(self.MAX_PARTY_DICE)
        # Reset graveyard
        self.state.graveyard = []
        
        # Step 2: Refresh Hero Card if exhausted
        if self.state.selected_hero_card and self.state.selected_hero_card.is_exhausted:
            self.state.selected_hero_card.refresh()
        
        # Step 3: Set Level Die to 1
        self.state.level = 1
        
        # Step 4: Roll 1 Dungeon Die to populate the dungeon
        self.state.dungeon_dice = self.roll_dungeon_dice(1)
        
        # Reset dragon's lair
        self.state.dragons_lair = []
    
    def roll_party_dice(self, num_dice=7):
        """Roll the white party dice."""
        party_faces = [face.value for face in PartyDiceFace]
        return [random.choice(party_faces) for _ in range(num_dice)]
    
    def roll_dungeon_dice(self, num_dice=1):
        """Roll the black dungeon dice, handling dragons specially."""
        dungeon_faces = [face.value for face in DungeonDiceFace]
        result = []
        
        for _ in range(num_dice):
            face = random.choice(dungeon_faces)
            if face == DungeonDiceFace.DRAGON.value:
                # Dragon dice go to the Dragon's Lair
                self.state.dragons_lair.append(face)
                print("A Dragon appears! The die is moved to the Dragon's Lair.")
            else:
                result.append(face)
        
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
        
        # Count dice by type for cleaner display
        dice_counts = {}
        for die in self.state.dungeon_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
        
        for die_face, count in dice_counts.items():
            print(f"- {die_face}: {count} dice")
        
        if self.state.dragons_lair:
            print("\nDragon's Lair:")
            print(f"- Dragon: {len(self.state.dragons_lair)} dice")
    
    def monster_phase(self):
        """Monster Phase: Adventurers fight monsters."""
        self.state.current_phase = "Monster Phase"
        print("\n--- MONSTER PHASE ---")
        
        # Print current dungeon state
        self.print_party_dice()
        self.print_dungeon_dice()
        
        # Display hero card info
        self.state.selected_hero_card.display_card_info()
        
        # Process monster encounters
        monsters = [die for die in self.state.dungeon_dice if die in 
                   [DungeonDiceFace.GOBLIN.value, DungeonDiceFace.SKELETON.value, DungeonDiceFace.OOZE.value]]
        
        if monsters:
            print(f"\nEncountered {len(monsters)} monsters!")
            
            # Give player option to use hero specialty before combat
            use_specialty = input(f"Use {self.state.selected_hero_card.name}'s specialty? (y/n): ").lower().strip()
            if use_specialty == 'y':
                # For Minstrel/Bard, we'll implement the specialty in the can_defeat_monsters method
                # Just acknowledge the specialty activation here
                print(f"Activating {self.state.selected_hero_card.name}'s specialty: {self.state.selected_hero_card.specialty}")
            
            if self.can_defeat_monsters(monsters, use_specialty == 'y'):
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
                        
                        # Recheck monster combat with specialty if active
                        if self.can_defeat_monsters(monsters, use_specialty == 'y'):
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
                        if self.can_defeat_monsters(monsters, use_specialty == 'y'):
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
        """Loot Phase: Open Chests or Quaff Potions (two actions)."""
        self.state.current_phase = "Loot Phase"
        print("\n--- LOOT PHASE ---")
        
        # Count available chests and potions
        chests = self.state.dungeon_dice.count(DungeonDiceFace.CHEST.value)
        potions = self.state.dungeon_dice.count(DungeonDiceFace.POTION.value)
        
        print(f"Available: {chests} chests, {potions} potions")
        
        # Allow two actions
        actions_taken = 0
        while actions_taken < 2:
            print(f"\nAction {actions_taken + 1}/2:")
            
            if chests <= 0 and potions <= 0:
                print("No chests or potions available.")
                break
                
            actions = []
            if chests > 0:
                actions.append("Open Chest")
            if potions > 0:
                actions.append("Quaff Potion")
                
            actions.append("Skip")
            
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
                        self.quaff_potion()
                        potions -= 1
                        # Remove a potion die from dungeon dice
                        self.state.dungeon_dice.remove(DungeonDiceFace.POTION.value)
                        actions_taken += 1
                    else:  # Skip
                        print("Action skipped.")
                        actions_taken += 1
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
        """Use a potion for its effect."""
        print("Quaffing potion...")
        
        # Simple potion effects
        effects = [
            "Gain a temporary Fighter die for this delve",
            "Gain a temporary Cleric die for this delve",
            "Gain a temporary Mage die for this delve",
            "Gain a temporary Thief die for this delve",
            "Refresh your hero card ability"
        ]
        
        effect = random.choice(effects)
        print(f"Potion effect: {effect}")
        
        if "temporary" in effect:
            hero_type = effect.split("temporary ")[1].split(" die")[0]
            self.state.party_dice.append(hero_type)
            print(f"A {hero_type} joins your party temporarily!")
        elif "Refresh" in effect and self.state.selected_hero_card:
            self.state.selected_hero_card.refresh()
            print(f"{self.state.selected_hero_card.name}'s ability is now refreshed!")
    
    def dragon_phase(self):
        """Dragon Phase: Occurs if Dragon is attracted to the dungeon."""
        if not self.state.dragons_lair:
            return True
            
        self.state.current_phase = "Dragon Phase"
        print("\n--- DRAGON PHASE ---")
        
        dragon_count = len(self.state.dragons_lair)
        print(f"There {'is' if dragon_count == 1 else 'are'} {dragon_count} dragon{'s' if dragon_count > 1 else ''} in the Dragon's Lair!")
        
        # Option to use Minstrel/Bard ultimate ability
        if not self.state.selected_hero_card.is_exhausted:
            use_ultimate = input(f"Use {self.state.selected_hero_card.name}'s ultimate ability to clear dragons? (y/n): ").lower().strip()
            if use_ultimate == 'y':
                self.state.selected_hero_card.use_ultimate(self.state)
                # If dragons are cleared, no need to continue with this phase
                if not self.state.dragons_lair:
                    return True
        
        # Need at least 3 different hero types to challenge a dragon
        unique_heroes = set(self.state.party_dice)
        unique_hero_count = len(unique_heroes)
        
        print(f"Your party has {unique_hero_count} different hero types.")
        
        if unique_hero_count >= 3:
            print("Your diverse party can challenge the dragon!")
            
            fight_dragon = input("Do you wish to fight the dragon? (y/n): ").lower().strip()
            if fight_dragon == 'y':
                # Success chance depends on party composition
                success_chance = min(0.8, 0.5 + (unique_hero_count - 3) * 0.1)
                
                if random.random() < success_chance:
                    print("Victory! Your party defeats the dragon!")
                    
                    # Rewards based on dragon count
                    treasure_reward = dragon_count * 3
                    exp_reward = dragon_count * 2
                    
                    self.state.treasure_tokens += treasure_reward
                    self.state.experience_tokens += exp_reward
                    
                    print(f"You gain {treasure_reward} treasure tokens and {exp_reward} experience tokens!")
                    
                    # Check for hero level-up
                    if (self.state.selected_hero_card.current_rank == HeroRank.NOVICE and 
                        self.state.experience_tokens >= self.state.selected_hero_card.xp_to_master):
                        self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
                    
                    # Clear dragon's lair
                    self.state.dragons_lair = []
                    
                    return True
                else:
                    print("The dragon is too powerful! Your party fails.")
                    # Option to end delve or continue without beating dragon
                    continue_delve = input("Continue delving without defeating the dragon? (y/n): ").lower().strip()
                    return continue_delve == 'y'
            else:
                print("You choose not to face the dragon for now.")
                return True
        else:
            print("Your party lacks the diversity needed to challenge the dragon.")
            print("You need at least 3 different hero types.")
            return True
    
    def regroup_phase(self):
        """Regroup Phase: Make decisions after the delve."""
        self.state.current_phase = "Regroup Phase"
        print("\n--- REGROUP PHASE ---")
        
        print("Choose your regroup action:")
        print("1. Retire to the Tavern (End delve and bank treasure)")
        print("2. Stuff of Legend (Attempt to gain extra party dice)")
        print("3. Seek Glory (Continue delving to the next level)")
        
        choice = input("Choose action (number): ").strip()
        
        if choice == "1":
            return self.retire_to_tavern()
        elif choice == "2":
            return self.stuff_of_legend()
        else:
            return self.seek_glory()
    
    def retire_to_tavern(self):
        """End the delve and bank treasure."""
        print("You retire to the tavern, ending this delve.")
        
        # Bank treasure - in this implementation we just keep it
        banked = self.state.treasure_tokens
        print(f"You've collected {banked} treasure tokens so far.")
        
        # End this delve
        return False
    
    def stuff_of_legend(self):
        """Attempt to gain extra party dice."""
        print("Attempting to recruit more heroes...")
        
        # Roll a die to determine success
        if random.random() < 0.6:  # 60% chance
            new_hero = random.choice([face.value for face in PartyDiceFace])
            self.state.party_dice.append(new_hero)
            print(f"Success! A {new_hero} joins your party!")
        else:
            print("No new heroes were willing to join your quest.")
        
        # Ask if player wants to continue delving
        continue_delve = input("Continue delving to the next level? (y/n): ").lower().strip()
        return continue_delve == 'y'
    
    def seek_glory(self):
        """Continue with the same party to the next level."""
        print("Your party continues their quest for glory!")
        # Continue delving
        return True

if __name__ == "__main__":
    game = DungeonDiceGame()
    game.start_game() 
    