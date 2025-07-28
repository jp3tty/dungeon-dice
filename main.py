import random
from dice import PartyDiceFace, DungeonDiceFace, DiceManager
from game_state import GameState
from phases import MonsterPhase, LootPhase, DragonPhase, RegroupPhase
from treasure import TreasureActions, TreasureType
from hero import HeroRank, MinstrelBardHero, AlchemistThaumaturgeHero, ArchaeologistTombRaiderHero
from dungeon_dice_game import clear_screen

def pause_for_continue(phase_name=""):
    """Pause and wait for player to continue to the next phase."""
    if phase_name:
        print(f"\n{'='*50}")
        print(f"🎯 {phase_name.upper()} PHASE COMPLETE 🎯".center(50))
        print(f"{'='*50}")
    else:
        print(f"\n{'='*50}")
        print(f"⏸️  PAUSE ⏸️".center(50))
        print(f"{'='*50}")
    
    print("Review the current game state above.")
    input("Press Enter when ready to continue...")
    clear_screen()

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
            print(f"   Expert Ability: {hero.master_ultimate}")
        
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
                self.state.experience_tokens >= self.state.selected_hero_card.xp_to_expert):
                self.state.selected_hero_card.check_level_up(self.state.experience_tokens)
            
            # Show progress after each delve
            print(f"\n📊 End of Delve {self.state.delve_count} Summary:")
            print(f"🌟 Experience: {self.state.experience_tokens} tokens")
            print(f"💎 Treasure: {self.state.treasure_tokens} tokens")
            self.state.display_treasure_info()
            
            # Pause between delves (except after the last one)
            if self.state.delve_count < self.MAX_DELVES:
                pause_for_continue("Delve")
        
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
        
        # Pause after Setup Phase
        pause_for_continue("Setup")
        
        # Continue until the delve is over (player chooses to end or fails)
        delve_active = True
        while delve_active:
            # Monster Phase
            monster_result = MonsterPhase.execute(self.state, self.state.selected_hero_card)
            if not monster_result:
                print("The monsters were too powerful! Delve ends.")
                break
            
            # Pause after Monster Phase
            pause_for_continue("Monster")
                
            # Loot Phase
            LootPhase.execute(self.state)
            
            # Pause after Loot Phase
            pause_for_continue("Loot")
            
            # Dragon Phase if dragons are present
            if self.state.dragons_lair:
                dragon_result = DragonPhase.execute(self.state, self.state.selected_hero_card)
                if not dragon_result:
                    # Dragon phase might end the delve based on the result
                    break
                
                # Pause after Dragon Phase (only if it occurred)
                pause_for_continue("Dragon")
            
            # Regroup Phase - player decides whether to continue or end delve
            regroup_result = RegroupPhase.execute(self.state, self.state.selected_hero_card)
            if not regroup_result:
                print("You've chosen to end this delve.")
                delve_active = False
    
    def setup_delve(self):
        """Set up for a new delve (one game round) with proper setup."""
        print("\n--- SETUP PHASE ---")
        print(f"🗡️  DELVE {self.state.delve_count} OF {self.MAX_DELVES}  🗡️")
        
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
    
    def roll_dungeon_dice(self, num_dice=1):
        """Roll the black dungeon dice, handling dragons specially."""
        result = []
        
        for _ in range(num_dice):
            die = self.dice_manager.roll_dungeon_dice(1)[0]
            if die == DungeonDiceFace.DRAGON.value:
                self.state.dragons_lair.append(die)
                print("A Dragon appears! The die moves to the Dragon's Lair.")
            else:
                result.append(die)
        
        return result
    
    def print_party_dice(self):
        """Print the current party dice."""
        print("\nYour Party Dice:")
        for i, die in enumerate(self.state.party_dice, 1):
            print(f"{i}. {die}")
    
    def print_dungeon_dice(self):
        """Print the current dungeon dice."""
        print("\nDungeon Dice:")
        for i, die in enumerate(self.state.dungeon_dice, 1):
            print(f"{i}. {die}")
        
        if self.state.dragons_lair:
            print(f"\nDragon's Lair: {len(self.state.dragons_lair)} dragon dice")

if __name__ == "__main__":
    game = DungeonDiceGame()
    game.start_game() 