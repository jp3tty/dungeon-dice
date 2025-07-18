# Dungeon Dice

A text-based dungeon crawling dice game where you lead a party of adventurers through dangerous dungeons, fighting monsters, collecting treasure, and gaining experience. The game features unique hero abilities, special dice mechanics, and strategic decision-making.

## Game Overview

In Dungeon Dice, you have three delves to prove your worth and gather as much treasure as possible. Each delve presents increasingly difficult challenges as you progress through dungeon levels. You'll need to manage your party of adventurers wisely, using their unique abilities to overcome monsters, collect treasure, and survive encounters with fearsome dragons.

## Game Rules

### Basic Mechanics
- You have 3 delves to gather treasure and experience
- Each delve starts with 7 Party Dice and encounters based on the dungeon level
- Party members can defeat specific monsters:
  - Fighters can defeat all of the Goblins
  - Clerics can defeat all of the Skeletons
  - Mages can defeat all of the Oozes
  - Thieves can defeat any single monster
  - Champions can defeat all of the monsters of a given type
  - Scrolls allow re-rolling of dice

### Heroes
- Start as a Novice hero with a unique specialty
- Can be upgraded to Master rank by gaining experience
- Have powerful ultimate abilities that can turn the tide of battle
- Available Heroes:
  - **Minstrel/Bard**
    - Specialty: Thieves may be used as Mages and Mages may be used as Thieves
    - Novice Ultimate: Discard all dice from the Dragon's Lair
    - Master Ultimate: Discard all dice from the Dragon's Lair
  - **Alchemist/Thaumaturge**
    - Specialty: All Chests become Potions
    - Novice Ultimate: Healing Salve - Roll 1 Party die from the Graveyard and add it to your Party
    - Master Ultimate: Transformation Potion - Roll 2 dice from the Graveyard and add them to your Party
  - **Archaeologist/Tomb Raider**
    - Specialty: When Forming the Party, draw 2 Treasure Tokens. Discard 6 Treasure Tokens at game end.
    - Novice Ultimate: Treasure Seeker - Draw 2 Treasure Tokens, then discard 2
    - Master Ultimate: Treasure Seeker - Draw 2 Treasure Tokens, then discard 1

### Phases
1. **Setup Phase**: Roll Party Dice and Dungeon Dice
2. **Monster Phase**: Defeat monsters using party members
   - Shows carried treasure items with descriptions for strategic planning
   - Displays active party dice including treasure companions
3. **Loot Phase**: Open chests and use potions
4. **Dragon Phase**: Deal with any dragons in the Dragon's Lair
5. **Regroup Phase**: Choose to continue delving or retire to safety
   - Displays dragon dice count for threat assessment
   - Shows collected treasure items with descriptions
   - Provides complete resource overview for strategic decisions

### Dragon Phase Mechanics
- **Triggers when 3+ dragon dice** are in the Dragon's Lair
- **Requires exactly 3 different companion types** to battle the dragon
- **Manual companion selection** - choose which companions to use (Scrolls are not companions)
- **Treasure integration** - treasure tokens can be used as companions
- **Scroll usage** - can use Scrolls to re-roll dice before dragon battle
- **Deterministic success** when 3 different types are selected
- **Strategic gameplay** - must carefully choose companion combination
- **Rewards**: 1 treasure token + 1 experience token + 1 drawn treasure

### Progression
- Gain experience by defeating monsters
- Collect treasure from chests
- Higher dungeon levels offer more rewards but greater danger
- Dragons offer the greatest rewards but pose significant risk

## Project Structure

```
dungeon-dice/
├── main.py                 # Main game entry point
├── dungeon_dice_game.py    # Core game logic and flow
├── phases.py              # Central import hub for all phase modules
├── monster_phase.py       # Monster Phase mechanics and combat
├── loot_phase.py          # Loot Phase mechanics (treasure and potions)
├── dragon_phase.py        # Dragon Phase mechanics
├── regroup_phase.py       # Regroup Phase mechanics (continue or retire)
├── game_state.py         # Game state management
├── hero.py               # Hero classes and abilities
├── dice.py               # Dice mechanics and faces
└── treasure.py           # Treasure system implementation
```

### File Descriptions
- `main.py`: Entry point for the game, handles game initialization and main loop
- `dungeon_dice_game.py`: Core game mechanics and overall game flow
- `phases.py`: Central import hub that provides access to all phase modules
- `monster_phase.py`: Monster Phase implementation with combat mechanics and companion selection
- `loot_phase.py`: Loot Phase implementation for opening chests and using potions
- `dragon_phase.py`: Dragon Phase mechanics and companion selection for dragon battles
- `regroup_phase.py`: Regroup Phase implementation for deciding to continue or end delves
- `game_state.py`: Game state management and data structures
- `hero.py`: Hero classes and abilities
- `dice.py`: Dice mechanics and faces
- `treasure.py`: Treasure system implementation

### Modular Architecture
The game uses a modular phase architecture where each game phase is implemented in its own dedicated file:
- **Improved maintainability**: Each phase can be modified independently
- **Better code organization**: Easy to locate specific phase logic
- **Enhanced readability**: Clear separation of concerns
- **Preserved gameplay**: All game mechanics remain identical to the player

## Installation

### Requirements
- Python 3.6 or higher
- No external dependencies required! The game uses only Python standard library modules:
  - `random`: For dice rolling and random events
  - `enum`: For game enumerations
  - `typing`: For type hints
  - `collections`: For utility functions

### Setup
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/dungeon-dice.git
cd dungeon-dice
```

2. No additional installation steps needed! The game uses only Python standard library modules.

## Running the Game

To play Dungeon Dice:

```bash
python main.py
```

Follow the on-screen prompts to make decisions and progress through your delves. Good luck, adventurer! 