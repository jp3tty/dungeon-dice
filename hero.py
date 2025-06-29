from enum import Enum
import random
from dice import DungeonDiceFace

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
        print(f"🔮 Passive Specialty: {self.specialty}")
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

class AlchemistThaumaturgeHero(HeroCard):
    def __init__(self):
        super().__init__(
            novice_name="Alchemist",
            master_name="Thaumaturge",
            novice_specialty="All Chests become Potions.",
            master_specialty="All Chests become Potions.",
            novice_ultimate="Healing Salve: Roll 1 Party die from the Graveyard and add it to your Party.",
            master_ultimate="Transformation Potion: Roll 2 dice from the Graveyard and add them to your Party.",
            xp_to_master=5
        )
    
    def use_ultimate(self, game_state):
        """Roll dice from the Graveyard based on current rank"""
        if super().use_ultimate(game_state):
            dice_to_roll = 2 if self.current_rank == HeroRank.MASTER else 1
            if not game_state.graveyard:
                print("The Graveyard is empty!")
                self.is_exhausted = False
                return False
                
            dice_rolled = []
            for _ in range(min(dice_to_roll, len(game_state.graveyard))):
                if game_state.graveyard:
                    die = random.choice(game_state.graveyard)
                    game_state.graveyard.remove(die)
                    game_state.party_dice.append(die)
                    dice_rolled.append(die)
            
            if dice_rolled:
                print(f"The {self.name} revives {len(dice_rolled)} die/dice: {', '.join(dice_rolled)}")
                return True
            return False
        return False 