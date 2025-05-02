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

class DiceManager:
    @staticmethod
    def roll_party_dice(num_dice=7):
        """Roll the white party dice."""
        party_faces = [face.value for face in PartyDiceFace]
        return [random.choice(party_faces) for _ in range(num_dice)]
    
    @staticmethod
    def roll_dungeon_dice(num_dice=1):
        """Roll the black dungeon dice."""
        dungeon_faces = [face.value for face in DungeonDiceFace]
        return [random.choice(dungeon_faces) for _ in range(num_dice)] 