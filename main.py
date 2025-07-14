import random
from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from game_state import GameState
from phases import MonsterPhase, LootPhase
from treasure import TreasureActions, TreasureType
from hero import HeroRank, MinstrelBardHero, AlchemistThaumaturgeHero, ArchaeologistTombRaiderHero
from dungeon_dice_game import clear_screen
from dragon_phase import DragonPhase

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
        
        print(f"\nTreasure Tokens: {game_state.treasure_tokens}")
        print(f"Experience Tokens: {game_state.experience_tokens}")
        
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
        available_heroes = [MinstrelBardHero(), AlchemistThaumaturgeHero(), ArchaeologistTombRaiderHero()]
        print("Available Heroes:")
        for i, hero in enumerate(available_heroes, 1):
            print(f"\n{i}) {hero.novice_name}/{hero.master_name}")
            print(f"   Specialty: {hero.novice_specialty}")
            print(f"   Novice Ability: {hero.novice_ultimate}")
            print(f"   Master Ability: {hero.master_ultimate}")
        
        while True:
            try:
                choice = int(input("\nChoose your hero (number): ").strip())
                if 1 <= choice <= len(available_heroes):
                    self.state.selected_hero_card = available_heroes[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(available_heroes)}")
            except ValueError:
                print("Please enter a valid number")
        
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
        
        # Apply hero's end-game specialty
        if self.state.selected_hero_card:
            self.state.selected_hero_card.apply_end_game_specialty(self.state)
        
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
            regroup_result = RegroupPhase.execute(self.state, self.state.selected_hero_card)
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
        
        # Step 2: Apply hero's formation specialty
        if self.state.selected_hero_card:
            self.state.selected_hero_card.apply_formation_specialty(self.state)
        
        # Step 3: Refresh Hero Card if exhausted
        if self.state.selected_hero_card and self.state.selected_hero_card.is_exhausted:
            self.state.selected_hero_card.refresh()
        
        # Step 4: Set Level Die to 1
        self.state.level = 1
        print("Dungeon Level set to 1")
        
        # Step 5: Roll 1 Dungeon Die to populate the dungeon
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