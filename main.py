import random
from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from game_state import GameState
from phases import MonsterPhase, LootPhase
from treasure import TreasureActions, TreasureType
from hero import HeroRank, MinstrelBardHero, AlchemistThaumaturgeHero

class DragonPhase:
    @staticmethod
    def execute(game_state, hero_card):
        """Execute the Dragon Phase."""
        if len(game_state.dragons_lair) < 3:
            print("\n--- DRAGON PHASE ---")
            print("Not enough dragons to attract attention. Proceeding to Regroup Phase...")
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

class RegroupPhase:
    @staticmethod
    def execute(game_state):
        """Execute the Regroup Phase."""
        print("\n--- REGROUP PHASE ---")
        
        # Display current state
        print(f"Current Level: {game_state.level}")
        if game_state.dragons_lair:
            print(f"Dragons in Lair: {len(game_state.dragons_lair)}")
        
        # Check for Stuff of Legend (Level 10 victory)
        if game_state.level == 10:
            print("\n🏆 STUFF OF LEGEND! 🏆")
            print("You've cleared the dungeon at Level 10!")
            print("This is a legendary achievement!")
            
            # Award experience tokens
            game_state.experience_tokens += 10
            print(f"You gain 10 Experience tokens for this legendary feat!")
            print(f"Total Experience tokens: {game_state.experience_tokens}")
            
            # Return dragons to available pool if any
            if game_state.dragons_lair:
                print(f"\nReturning {len(game_state.dragons_lair)} Dragon dice to the available pool.")
                game_state.dragons_lair = []
            
            return False  # End the delve
        
        # Regular regroup choices
        while True:  # Keep prompting until a valid choice is made
            print("\nChoose your Regroup action:")
            print("1) Retire to the Tavern (End delve and gain Experience)")
            print("2) Seek Glory (Challenge the next dungeon level)")
            
            choice = input("Choose action (number): ").strip()
            
            if choice == "1":
                return RegroupPhase.retire_to_tavern(game_state, forced_retirement=False)
            elif choice == "2":
                return RegroupPhase.seek_glory(game_state)
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
    
    @staticmethod
    def retire_to_tavern(game_state, forced_retirement):
        """End the delve and collect experience."""
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
        print(f"\nRolling {dice_to_roll} Dungeon dice...")
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
        
        # Display results
        print("\nDungeon dice results:")
        dice_counts = {}
        for die in game_state.dungeon_dice:
            dice_counts[die] = dice_counts.get(die, 0) + 1
        for die_face, count in dice_counts.items():
            print(f"- {die_face}: {count}")
        
        if game_state.dragons_lair:
            print(f"\nDragon's Lair now contains {len(game_state.dragons_lair)} dice!")
        
        # Continue delving
        return True

class DungeonDiceGame:
    def __init__(self):
        self.state = GameState()
        self.dice_manager = DiceManager()
        self.MAX_DELVES = 3
        self.MAX_PARTY_DICE = 7
        self.MAX_DUNGEON_DICE = 7
        self.MAX_LEVEL = 10
        self.available_hero_cards = self.initialize_hero_cards()
        
    def initialize_hero_cards(self):
        """Initialize available hero cards"""
        return [MinstrelBardHero(), AlchemistThaumaturgeHero()]
        
    def start_game(self):
        """Start a new game."""
        print("\n" + "="*50)
        print("🎲 WELCOME TO DUNGEON DICE 🎲".center(50))
        print("="*50)
        print("\nPrepare yourself for an epic adventure!")
        print("You have 3 delves to prove your worth, gather treasure,")
        print("and become a legendary hero!\n")
        
        # Choose a hero card
        print("Available Heroes:")
        for i, hero in enumerate([MinstrelBardHero(), AlchemistThaumaturgeHero()], 1):
            print(f"\n{i}) {hero.novice_name}/{hero.master_name}")
            print(f"   Specialty: {hero.novice_specialty}")
            print(f"   Novice Ability: {hero.novice_ultimate}")
            print(f"   Master Ability: {hero.master_ultimate}")
        
        while True:
            try:
                choice = int(input("\nChoose your hero (number): ").strip())
                if choice == 1:
                    self.state.selected_hero_card = MinstrelBardHero()
                    break
                elif choice == 2:
                    self.state.selected_hero_card = AlchemistThaumaturgeHero()
                    break
                else:
                    print("Please enter either 1 or 2")
            except ValueError:
                print("Please enter a valid number")
        
        print("\n🦸 Your Chosen Hero 🦸".center(50))
        print("-"*50)
        print(f"Name: {self.state.selected_hero_card.name}")
        self.state.selected_hero_card.display_card_info()
        
        # Initialize game state
        self.state.delve_count = 0
        self.state.level = 1
        self.state.party_dice = []
        self.state.dungeon_dice = []
        self.state.dragons_lair = []
        self.state.treasure_tokens = 0
        self.state.experience_tokens = 0
        self.state.graveyard = []
        
        # Start first delve
        print(f"\n{'='*50}")
        print(f"🗡️  DELVE {self.state.delve_count + 1} OF {self.MAX_DELVES}  🗡️".center(50))
        print(f"{'='*50}")
        
        # Main game loop - 3 delves
        while self.state.delve_count < self.MAX_DELVES:
            self.start_delve()
            
            # Check for hero level up between delves
            if (self.state.selected_hero_card.current_rank == HeroRank.NOVICE and 
                self.state.experience_tokens >= self.state.selected_hero_card.xp_to_master):
                self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
            
            # Show progress after each delve
            print(f"\n📊 End of Delve {self.state.delve_count} Summary:")
            print(f"🌟 Experience: {self.state.experience_tokens} tokens")
            print(f"💎 Treasure: {self.state.treasure_tokens} tokens")
            self.state.display_treasure_info()
        
        self.end_game()
    
    def end_game(self):
        """Handle end game scoring and final display."""
        print("\n" + "="*40)
        print("GAME OVER - FINAL SCORING")
        print("="*40)
        
        # Display hero final state
        print(f"\nFinal Hero State:")
        print(f"Hero: {self.state.selected_hero_card.name}")
        print(f"Rank: {self.state.selected_hero_card.current_rank.value}")
        
        # Display base experience
        print(f"\nBase Experience: {self.state.experience_tokens} tokens")
        
        # Display treasure scoring details
        print("\nTreasure Scoring:")
        treasures = self.state.get_available_treasures()
        
        # Count Dragon Scales
        dragon_scales = self.state.player_treasure.count_treasure_type(TreasureType.DRAGON_SCALE)
        if dragon_scales > 0:
            pairs = dragon_scales // 2
            print(f"Dragon Scale pairs: {pairs} (Worth {pairs * 2} Experience)")
        
        # Count Town Portals
        town_portals = self.state.player_treasure.count_treasure_type(TreasureType.TOWN_PORTAL)
        if town_portals > 0:
            print(f"Unused Town Portals: {town_portals} (Worth {town_portals * 2} Experience)")
        
        # Count other treasures
        other_treasures = len(treasures) - dragon_scales - town_portals
        if other_treasures > 0:
            print(f"Other unused treasures: {other_treasures} (Worth {other_treasures} Experience)")
        
        # Calculate and display final score
        treasure_exp = self.state.player_treasure.calculate_end_game_experience()
        final_score = self.state.calculate_final_score()
        
        print("\nFinal Score Breakdown:")
        print(f"Base Experience:     {self.state.experience_tokens}")
        print(f"Treasure Bonuses:    {treasure_exp}")
        print(f"{'='*20}")
        print(f"FINAL SCORE:        {final_score}")
        
        # Display achievement message based on score
        if final_score >= 30:
            print("\nLEGENDARY! You are truly a master of the dungeon!")
        elif final_score >= 20:
            print("\nIMPRESSIVE! You've proven yourself a worthy adventurer!")
        elif final_score >= 10:
            print("\nGOOD EFFORT! You're learning the ways of the dungeon.")
        else:
            print("\nYou've survived to tell the tale. Better luck next time!")
    
    def start_delve(self):
        """Start a new delve (one game round) with proper setup."""
        self.state.delve_count += 1
        
        # Setup phase
        self.setup_delve()
        
        # Continue until the delve is over (player chooses to end or fails)
        delve_active = True
        while delve_active:
            # Monster Phase
            monster_result = MonsterPhase.execute(self.state, self.state.selected_hero_card)
            if not monster_result:
                print("The monsters were too powerful! Delve ends.")
                break
                
            # Loot Phase
            LootPhase.execute(self.state)
            
            # Dragon Phase if dragons are present
            if self.state.dragons_lair:
                dragon_result = DragonPhase.execute(self.state, self.state.selected_hero_card)
                if not dragon_result:
                    # Dragon phase might end the delve based on the result
                    break
            
            # Regroup Phase - player decides whether to continue or end delve
            regroup_result = RegroupPhase.execute(self.state)
            if not regroup_result:
                print("You've chosen to end this delve.")
                delve_active = False
    
    def setup_delve(self):
        """Set up for a new delve (one game round) with proper setup."""
        print("\n--- SETUP PHASE ---")
        
        # Step 1: Roll all 7 Party Dice
        print("Rolling 7 Party Dice to form your starting party...")
        self.state.party_dice = self.dice_manager.roll_party_dice(self.MAX_PARTY_DICE)
        # Reset graveyard
        self.state.graveyard = []
        
        # Step 2: Refresh Hero Card if exhausted
        if self.state.selected_hero_card and self.state.selected_hero_card.is_exhausted:
            self.state.selected_hero_card.refresh()
        
        # Step 3: Set Level Die to 1
        self.state.level = 1
        print("Dungeon Level set to 1")
        
        # Step 4: Roll 1 Dungeon Die to populate the dungeon
        print("Rolling 1 Dungeon Die to populate the dungeon...")
        self.state.dungeon_dice = self.roll_dungeon_dice(1)
        
        # Reset dragon's lair
        self.state.dragons_lair = []
    
    def roll_dungeon_dice(self, num_dice=1):
        """Roll the black dungeon dice, handling dragons specially."""
        result = []
        
        for _ in range(num_dice):
            dice_roll = self.dice_manager.roll_dungeon_dice(1)[0]
            if dice_roll == DungeonDiceFace.DRAGON.value:
                # Dragon dice go to the Dragon's Lair
                self.state.dragons_lair.append(dice_roll)
                print("A Dragon appears! The die is moved to the Dragon's Lair.")
            else:
                result.append(dice_roll)
        
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

if __name__ == "__main__":
    game = DungeonDiceGame()
    game.start_game() 