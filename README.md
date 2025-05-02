# Dungeon Dice

A text-based dungeon crawling dice game where you lead a party of adventurers through dangerous dungeons, fighting monsters, collecting treasure, and gaining experience. The game features unique hero abilities, special dice mechanics, and strategic decision-making.

## Game Overview

In Dungeon Dice, you have three delves to prove your worth and gather as much treasure as possible. Each delve presents increasingly difficult challenges as you progress through dungeon levels. You'll need to manage your party of adventurers wisely, using their unique abilities to overcome monsters, collect treasure, and survive encounters with fearsome dragons.

## Game Rules

### Basic Mechanics
- You have 3 delves to gather treasure and experience
- Each delve starts with 7 Party Dice and encounters based on the dungeon level
- Party members can defeat specific monsters:
  - Fighters can defeat any number of Goblins
  - Clerics can defeat any number of Skeletons
  - Mages can defeat any number of Oozes
  - Thieves can defeat any single monster
  - Champions can defeat any single monster
  - Scrolls allow re-rolling of dice

### Heroes
- Start as a Novice hero with a unique specialty
- Can be upgraded to Master rank by gaining experience
- Have powerful ultimate abilities that can turn the tide of battle
- Current Hero: Minstrel/Bard
  - Specialty: Thieves may be used as Mages and Mages may be used as Thieves
  - Ultimate: Discard all dice from the Dragon's Lair

### Phases
1. **Setup Phase**: Roll Party Dice and Dungeon Dice
2. **Monster Phase**: Defeat monsters using party members
3. **Loot Phase**: Open chests and use potions
4. **Dragon Phase**: Deal with any dragons in the Dragon's Lair
5. **Regroup Phase**: Choose to continue delving or retire to safety

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
├── phases.py              # Implementation of game phases
├── game_state.py         # Game state management
├── hero.py               # Hero classes and abilities
├── dice.py               # Dice mechanics and faces
└── treasure.py           # Treasure system implementation
```

### File Descriptions
- `main.py`: Entry point for the game, handles game initialization and main loop
- `dungeon_dice_game.py`: Core game mechanics and overall game flow
- `phases.py`: Implements the different game phases (Monster, Loot, Dragon, etc.)
- `game_state.py`: Manages the game state, including party dice, dungeon dice, and resources
- `hero.py`: Defines hero classes, their abilities, and progression system
- `dice.py`: Implements dice mechanics, including different die faces and rolling logic
- `treasure.py`: Handles treasure system, including different types of treasure and their effects

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