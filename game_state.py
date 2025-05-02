from treasure import TreasureManager, PlayerTreasure, TreasureType

class GameState:
    def __init__(self):
        self.delve_count = 0
        self.level = 1
        self.party_dice = []  # Active party dice
        self.graveyard = []   # Used party dice go here
        self.dungeon_dice = []
        self.dragons_lair = []  # Stores dragon dice separately
        self.treasure_tokens = 0  # This is now just a counter for display
        self.experience_tokens = 0
        self.selected_hero_card = None
        self.current_phase = None
        
        # Initialize treasure system
        self.treasure_manager = TreasureManager()
        self.player_treasure = PlayerTreasure(self.treasure_manager)
        
    def use_party_die(self, die_index):
        """Move a party die to the graveyard and return its value."""
        if die_index < 0 or die_index >= len(self.party_dice):
            return None
        
        die = self.party_dice.pop(die_index)
        self.graveyard.append(die)
        return die
    
    def reset_graveyard(self):
        """Return all dice from graveyard to active party."""
        self.party_dice.extend(self.graveyard)
        self.graveyard = []
    
    def draw_treasure(self):
        """Draw a treasure token from the pool."""
        token = self.treasure_manager.draw_treasure()
        if token:
            self.player_treasure.add_treasure(token)
            self.treasure_tokens += 1  # Increment display counter
            return token
        else:
            # If no treasure tokens remain, gain experience instead
            self.experience_tokens += 1
            print("No Treasure tokens remain! You gain an Experience token instead.")
            return None
    
    def use_treasure(self, index):
        """Use a treasure token from the player's collection."""
        token = self.player_treasure.use_treasure(index)
        if token:
            self.treasure_tokens -= 1  # Decrement display counter
        return token
    
    def get_available_treasures(self):
        """Get all treasures in the player's collection."""
        return self.player_treasure.get_available_treasures()
    
    def get_usable_companions(self):
        """Get all treasures that can be used as companions."""
        return self.player_treasure.get_usable_companions()
    
    def calculate_final_score(self):
        """Calculate final score including treasure bonuses."""
        base_exp = self.experience_tokens
        treasure_exp = self.player_treasure.calculate_end_game_experience()
        return base_exp + treasure_exp
    
    def display_treasure_info(self):
        """Display detailed information about available treasures."""
        treasures = self.get_available_treasures()
        if not treasures:
            print("No treasures in your collection.")
            return
        
        print("\nYour Treasures:")
        for i, token in enumerate(treasures):
            print(f"{i+1}. {token.name}")
            print(f"   Effect: {token.get_description()}")
        
        # Show special counts
        dragon_scales = self.player_treasure.count_treasure_type(TreasureType.DRAGON_SCALE)
        if dragon_scales > 0:
            pairs = dragon_scales // 2
            print(f"\nDragon Scale pairs: {pairs} (Worth {pairs * 2} exp at game end)")
        
        town_portals = self.player_treasure.count_treasure_type(TreasureType.TOWN_PORTAL)
        if town_portals > 0:
            print(f"Unused Town Portals: {town_portals} (Worth {town_portals * 2} exp if unused at game end)") 