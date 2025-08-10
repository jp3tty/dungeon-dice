import random
from enum import Enum
from typing import List, Dict
from dice import PartyDiceFace, DungeonDiceFace

class TreasureType(Enum):
    VORPAL_SWORD = "Vorpal Sword"
    TALISMAN = "Talisman"
    SCEPTER_OF_POWER = "Scepter of Power"
    THIEVES_TOOLS = "Thieves' Tools"
    SCROLL = "Scroll"
    RING_OF_INVISIBILITY = "Ring of Invisibility"
    DRAGON_SCALE = "Dragon Scale"
    ELIXIR = "Elixir"
    DRAGON_BAIT = "Dragon Bait"
    TOWN_PORTAL = "Town Portal"

class TreasureToken:
    def __init__(self, treasure_type: TreasureType):
        self.type = treasure_type
        
    @property
    def name(self) -> str:
        return self.type.value
        
    def get_description(self) -> str:
        descriptions = {
            TreasureType.VORPAL_SWORD: "Use as one Fighter",
            TreasureType.TALISMAN: "Use as one Cleric",
            TreasureType.SCEPTER_OF_POWER: "Use as one Mage",
            TreasureType.THIEVES_TOOLS: "Use as one Thief",
            TreasureType.SCROLL: "Use as one Scroll die",
            TreasureType.RING_OF_INVISIBILITY: "Return all Dungeon dice from the Dragons Lair to the active supply of Dungeon dice. This does not count as Defeating the dragon - do not collect an Experience token or draw a Treasure",
            TreasureType.DRAGON_SCALE: "At the end of the game, collect 2 additional Experience tokens for each pair of Dragon Scales you possess",
            TreasureType.ELIXIR: "Revive 1 Party die (return it from the Graveyard to your active party) and choose its face",
            TreasureType.DRAGON_BAIT: "Transform all monsters into Dragon faces. Move those dice into the Dragon's Lair",
            TreasureType.TOWN_PORTAL: "Collect Experience tokens equal to the Level Die. The delve is over. If unused, Town Portal is worth 2 experience at the end of the game instead of the usual 1"
        }
        return descriptions[self.type]
    
    def can_use_as_companion(self) -> bool:
        """Check if this treasure can be used as a companion."""
        return self.type in [
            TreasureType.VORPAL_SWORD,
            TreasureType.TALISMAN,
            TreasureType.SCEPTER_OF_POWER,
            TreasureType.THIEVES_TOOLS
        ]
    
    def get_companion_type(self) -> str:
        """Get the companion type this treasure can act as."""
        companion_map = {
            TreasureType.VORPAL_SWORD: PartyDiceFace.FIGHTER.value,
            TreasureType.TALISMAN: PartyDiceFace.CLERIC.value,
            TreasureType.SCEPTER_OF_POWER: PartyDiceFace.MAGE.value,
            TreasureType.THIEVES_TOOLS: PartyDiceFace.THIEF.value,
            TreasureType.SCROLL: PartyDiceFace.SCROLL.value
        }
        return companion_map.get(self.type)

class TreasureManager:
    def __init__(self):
        # Initialize the treasure pool with correct counts
        self.treasure_pool: List[TreasureToken] = []
        self.initialize_treasure_pool()
        
    def initialize_treasure_pool(self):
        """Initialize the treasure pool with the correct number of each type."""
        counts = {
            TreasureType.VORPAL_SWORD: 3,
            TreasureType.TALISMAN: 3,
            TreasureType.SCEPTER_OF_POWER: 3,
            TreasureType.THIEVES_TOOLS: 3,
            TreasureType.SCROLL: 3,
            TreasureType.RING_OF_INVISIBILITY: 4,
            TreasureType.DRAGON_SCALE: 6,
            TreasureType.ELIXIR: 3,
            TreasureType.DRAGON_BAIT: 4,
            TreasureType.TOWN_PORTAL: 4
        }
        
        for treasure_type, count in counts.items():
            for _ in range(count):
                self.treasure_pool.append(TreasureToken(treasure_type))
    
    def draw_treasure(self) -> TreasureToken:
        """Draw a random treasure token from the pool."""
        if not self.treasure_pool:
            return None
        return self.treasure_pool.pop(random.randint(0, len(self.treasure_pool) - 1))
    
    def return_treasure(self, token: TreasureToken):
        """Return a used treasure token to the pool."""
        self.treasure_pool.append(token)
    
    def get_pool_size(self) -> int:
        """Get the number of treasure tokens remaining in the pool."""
        return len(self.treasure_pool)
    
    def get_pool_contents(self) -> Dict[str, int]:
        """Get a count of each type of treasure in the pool."""
        contents = {}
        for token in self.treasure_pool:
            contents[token.name] = contents.get(token.name, 0) + 1
        return contents

class PlayerTreasure:
    def __init__(self, treasure_manager: TreasureManager):
        self.treasure_manager = treasure_manager
        self.collected_treasures: List[TreasureToken] = []
    
    def add_treasure(self, token: TreasureToken):
        """Add a treasure token to the player's collection."""
        self.collected_treasures.append(token)
    
    def use_treasure(self, index: int) -> TreasureToken:
        """Use a treasure token from the player's collection."""
        if 0 <= index < len(self.collected_treasures):
            token = self.collected_treasures.pop(index)
            self.treasure_manager.return_treasure(token)
            return token
        return None
    
    def get_available_treasures(self) -> List[TreasureToken]:
        """Get all treasures in the player's collection."""
        return self.collected_treasures
    
    def calculate_end_game_experience(self) -> int:
        """Calculate additional experience from treasures at game end."""
        exp = 0
        
        # Count Dragon Scales (2 exp per pair)
        dragon_scales = sum(1 for t in self.collected_treasures 
                          if t.type == TreasureType.DRAGON_SCALE)
        exp += (dragon_scales // 2) * 2
        
        # Count Town Portals (2 exp each if unused)
        town_portals = sum(1 for t in self.collected_treasures 
                          if t.type == TreasureType.TOWN_PORTAL)
        exp += town_portals * 2
        
        # All other treasures worth 1 exp
        other_treasures = len(self.collected_treasures) - dragon_scales - town_portals
        exp += other_treasures
        
        return exp
    
    def get_usable_companions(self) -> List[tuple[int, TreasureToken]]:
        """Get all treasures that can be used as companions."""
        return [(i, t) for i, t in enumerate(self.collected_treasures) 
                if t.can_use_as_companion()]
    
    def has_treasure_type(self, treasure_type: TreasureType) -> bool:
        """Check if player has a specific type of treasure."""
        return any(t.type == treasure_type for t in self.collected_treasures)
    
    def count_treasure_type(self, treasure_type: TreasureType) -> int:
        """Count how many of a specific treasure type the player has."""
        return sum(1 for t in self.collected_treasures if t.type == treasure_type)

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
                    
                elif token.type == TreasureType.SCROLL:
                    # Use Scroll treasure to re-roll dice
                    print("Scroll treasure used! Select dice to re-roll (results will be random).")
                    game_state.use_treasure(choice_idx)
                    
                    # Create a list of all available dice to re-roll
                    print("\nAvailable Dice to Re-roll:")
                    print("=== Dungeon Dice (excluding Dragon dice) ===")
                    reroll_options = []
                    # Add dungeon dice (excluding dragon dice)
                    for i, die in enumerate(game_state.dungeon_dice):
                        reroll_options.append(("dungeon", i, die))
                        print(f"{len(reroll_options)}. Dungeon Die: {die}")
                    
                    print("\n=== Party Dice ===")
                    # Add party dice
                    for i, die in enumerate(game_state.party_dice):
                        reroll_options.append(("party", i, die))
                        print(f"{len(reroll_options)}. Party Die: {die}")
                    
                    if not reroll_options:
                        print("No dice available to re-roll!")
                        return False
                    
                    print(f"{len(reroll_options)+1}. Cancel")
                    
                    reroll_choice = input("Choose dice to re-roll (number): ").strip()
                    try:
                        reroll_choice_idx = int(reroll_choice) - 1
                        if reroll_choice_idx == len(reroll_options):
                            print("Re-roll cancelled.")
                            return False
                        if 0 <= reroll_choice_idx < len(reroll_options):
                            source, idx, old_die = reroll_options[reroll_choice_idx]
                            
                            # Re-roll the selected die
                            from dice import DiceManager
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
                    
                else:  # Companion-like treasures are handled in their respective phases
                    print("This treasure must be used during combat or specific phases.")
                    return False
            else:
                print("Invalid choice.")
                return False
        except ValueError:
            print("Invalid input.")
            return False 