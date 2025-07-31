from enum import Enum
import random
from dice import DungeonDiceFace, DiceManager

class HeroRank(Enum):
    NOVICE = "Novice"
    MASTER = "Expert"

class HeroCard:
    def __init__(self, novice_name, master_name, novice_specialty, master_specialty, 
                 novice_ultimate, master_ultimate, xp_to_expert=5):
        self.novice_name = novice_name
        self.master_name = master_name
        self.novice_specialty = novice_specialty
        self.master_specialty = master_specialty
        self.novice_ultimate = novice_ultimate
        self.master_ultimate = master_ultimate
        self.xp_to_expert = xp_to_expert
        
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
        if self.current_rank == HeroRank.NOVICE and xp >= self.xp_to_expert:
            self.current_rank = HeroRank.MASTER
            print(f"Your hero has ascended from {self.novice_name} to {self.master_name}!")
            print(f"New Ultimate: {self.master_ultimate}")
            # Only show specialty change if it actually changed
            if self.master_specialty != self.novice_specialty:
                print(f"New Specialty: {self.master_specialty}")
            return True
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
    
    def apply_formation_specialty(self, game_state):
        """Apply hero's specialty during party formation. Override in subclasses."""
        return False
    
    def apply_end_game_specialty(self, game_state):
        """Apply hero's specialty at game end. Override in subclasses."""
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
        rank_text = "✨ EXPERT ✨" if self.current_rank == HeroRank.MASTER else "NOVICE"
        print(f"\n{'='*50}")
        print(f"📜 {self.name} ({rank_text}) 📜".center(50))
        print(f"{'='*50}")
        print(f"🔮 Passive Specialty: {self.specialty}")
        print(f"⚡ Ultimate: {self.ultimate}")
        status = "❌ EXHAUSTED" if self.is_exhausted else "✅ READY"
        print(f"📋 Status: {status}")
        if self.current_rank == HeroRank.NOVICE:
            print(f"📈 XP needed to expert: {self.xp_to_expert}")
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
            xp_to_expert=5
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

class AlchemistThaumaturgeHero(HeroCard):
    def __init__(self):
        super().__init__(
            novice_name="Alchemist",
            master_name="Thaumaturge",
            novice_specialty="All Chests become Potions.",
            master_specialty="All Chests become Potions.",
            novice_ultimate="Healing Salve: Roll 1 Party die from the Graveyard and add it to your Party.",
            master_ultimate="Transformation Potion: Roll 2 dice from the Graveyard and add them to your Party.",
            xp_to_expert=5
        )
    
    def use_ultimate(self, game_state):
        """Roll dice from the Graveyard based on current rank"""
        if super().use_ultimate(game_state):
            dice_to_roll = 2 if self.current_rank == HeroRank.MASTER else 1
            if not game_state.graveyard:
                print("The Graveyard is empty!")
                self.is_exhausted = False
                return False
            
            print(f"\nThe {self.name} can revive {dice_to_roll} companion(s) from the Graveyard.")
            print("Available companions in the Graveyard:")
            
            # Count dice by type in graveyard
            graveyard_counts = {}
            for die in game_state.graveyard:
                graveyard_counts[die] = graveyard_counts.get(die, 0) + 1
            
            # Display available companions
            available_companions = []
            for die_type, count in graveyard_counts.items():
                for i in range(count):
                    available_companions.append(die_type)
                    print(f"{len(available_companions)}. {die_type}")
            
            dice_rolled = []
            for i in range(min(dice_to_roll, len(available_companions))):
                while True:
                    print(f"\nSelect companion {i+1}/{min(dice_to_roll, len(available_companions))} to revive:")
                    print("Available companions in the Graveyard:")
                    
                    # Display current available companions
                    for idx, companion in enumerate(available_companions, 1):
                        print(f"{idx}. {companion}")
                    
                    try:
                        choice = int(input("Choose companion (number): ").strip())
                        if 1 <= choice <= len(available_companions):
                            selected_die = available_companions[choice - 1]
                            # Remove the selected die from graveyard
                            game_state.graveyard.remove(selected_die)
                            # Roll the die to get a random new face
                            dice_manager = DiceManager()
                            new_die = dice_manager.roll_party_dice(1)[0]
                            # Add the rolled die to party
                            game_state.party_dice.append(new_die)
                            dice_rolled.append(new_die)
                            print(f"Revived and rolled {selected_die} → {new_die}!")
                            # Update available companions list
                            available_companions.pop(choice - 1)
                            break
                        else:
                            print("Invalid choice. Please select a valid number from the list above.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            
            if dice_rolled:
                print(f"\nThe {self.name} successfully revived {len(dice_rolled)} companion(s): {', '.join(dice_rolled)}")
                return True
            else:
                print("No companions were revived.")
                self.is_exhausted = False
                return False
        return False 

class ArchaeologistTombRaiderHero(HeroCard):
    def __init__(self):
        super().__init__(
            novice_name="Archaeologist",
            master_name="Tomb Raider",
            novice_specialty="When Forming the Party, draw 2 Treasure Tokens. Discard 6 Treasure Tokens at game end.",
            master_specialty="When Forming the Party, draw 2 Treasure Tokens. Discard 6 Treasure Tokens at game end.",
            novice_ultimate="Treasure Seeker: Draw 2 Treasure Tokens from the Treasure Pool and then discard 2 Treasure Tokens.",
            master_ultimate="Treasure Seeker: Draw 2 Treasure Tokens from the Treasure Pool and then discard 1 Treasure Token.",
            xp_to_expert=5
        )
    
    def use_ultimate(self, game_state):
        """Draw treasure tokens and then discard some based on rank"""
        if super().use_ultimate(game_state):
            tokens_to_discard = 2 if self.current_rank == HeroRank.NOVICE else 1
            
            print(f"\nThe {self.name} uses Treasure Seeker ability!")
            print(f"Drawing 2 Treasure Tokens from the Treasure Pool...")
            
            # Draw 2 treasure tokens from the pool
            drawn_tokens = []
            for i in range(2):
                token = game_state.treasure_manager.draw_treasure()
                if token:
                    game_state.player_treasure.add_treasure(token)
                    game_state.treasure_tokens += 1
                    drawn_tokens.append(token)
                    print(f"Drew: {token.name}")
                else:
                    print("No more treasure tokens in the pool!")
                    break
            
            if drawn_tokens:
                print(f"\nNow discarding {tokens_to_discard} Treasure Token(s)...")
                
                # Let player choose which tokens to discard
                available_treasures = game_state.get_available_treasures()
                if len(available_treasures) >= tokens_to_discard:
                    print("\nChoose which treasures to discard:")
                    for i, treasure in enumerate(available_treasures):
                        print(f"{i+1}. {treasure.name}")
                    
                    discarded_count = 0
                    while discarded_count < tokens_to_discard:
                        try:
                            choice = int(input(f"Choose treasure {discarded_count + 1} to discard (number): ").strip())
                            if 1 <= choice <= len(available_treasures):
                                # Store the treasure name before using it
                                treasure_name = available_treasures[choice - 1].name
                                # Use the treasure (which returns it to the pool)
                                game_state.use_treasure(choice - 1)
                                discarded_count += 1
                                print(f"Discarded: {treasure_name}")
                            else:
                                print("Invalid choice. Please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    
                    print(f"\nSuccessfully drew {len(drawn_tokens)} treasure(s) and discarded {tokens_to_discard} treasure(s)!")
                    return True
                else:
                    print(f"Not enough treasures to discard {tokens_to_discard} tokens!")
                    self.is_exhausted = False  # Don't exhaust if we can't complete the action
                    return False
            else:
                print("No treasures were drawn!")
                self.is_exhausted = False  # Don't exhaust if no treasures were drawn
                return False
        return False
    
    def apply_formation_specialty(self, game_state):
        """Apply Archaeologist/Tomb Raider specialty: Draw 2 Treasure Tokens during party formation."""
        print(f"\n✨ {self.name}'s Specialty: Drawing 2 Treasure Tokens during party formation! ✨")
        
        drawn_tokens = []
        for i in range(2):
            token = game_state.treasure_manager.draw_treasure()
            if token:
                game_state.player_treasure.add_treasure(token)
                game_state.treasure_tokens += 1
                drawn_tokens.append(token)
                print(f"Drew: {token.name}")
            else:
                print("No more treasure tokens in the pool!")
                break
        
        if drawn_tokens:
            print(f"Successfully drew {len(drawn_tokens)} treasure token(s) during party formation!")
            return True
        else:
            print("No treasures were drawn during party formation.")
            return False
    
    def apply_end_game_specialty(self, game_state):
        """Apply Archaeologist/Tomb Raider specialty: Discard 6 Treasure Tokens at game end."""
        print(f"\n✨ {self.name}'s End-Game Specialty: Discarding 6 Treasure Tokens! ✨")
        
        available_treasures = game_state.get_available_treasures()
        if len(available_treasures) < 6:
            print(f"Not enough treasures to discard! You have {len(available_treasures)} treasures but need to discard 6.")
            print("All remaining treasures will be discarded.")
            tokens_to_discard = len(available_treasures)
        else:
            tokens_to_discard = 6
        
        if tokens_to_discard > 0:
            print(f"\nChoose which {tokens_to_discard} treasure(s) to discard:")
            for i, treasure in enumerate(available_treasures):
                print(f"{i+1}. {treasure.name}")
            
            discarded_count = 0
            while discarded_count < tokens_to_discard and available_treasures:
                try:
                    choice = int(input(f"Choose treasure {discarded_count + 1} to discard (number): ").strip())
                    if 1 <= choice <= len(available_treasures):
                        # Store the treasure name before using it
                        treasure_name = available_treasures[choice - 1].name
                        # Use the treasure (which returns it to the pool)
                        game_state.use_treasure(choice - 1)
                        discarded_count += 1
                        print(f"Discarded: {treasure_name}")
                        # Update available treasures list
                        available_treasures = game_state.get_available_treasures()
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            print(f"\nSuccessfully discarded {discarded_count} treasure token(s) at game end!")
            return True
        else:
            print("No treasures to discard.")
            return False 