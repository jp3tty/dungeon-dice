# Dungeon Dice

A text-based dungeon crawling dice game where you lead a party of adventurers through dangerous dungeons, fighting monsters, collecting treasure, and gaining experience. The game features unique hero abilities, special dice mechanics, and strategic decision-making.

## Game Overview

In Dungeon Dice, you have three delves to prove your worth and gather as much treasure as possible. Each delve presents increasingly difficult challenges as you progress through dungeon levels. You'll need to manage your party of adventurers wisely, using their unique abilities to overcome monsters, collect treasure, and survive encounters with fearsome dragons.

The game features a **pause system** between phases that allows you to review the current game state and plan your next moves at your own pace. You control when to proceed to the next phase, giving you time to analyze the situation and make strategic decisions.

## Game Rules

### Basic Mechanics
- You have 3 delves to gather treasure and experience
- Each delve starts with 7 Party Dice and encounters based on the dungeon level
- Party members can defeat specific monsters:
  - **Fighter** defeats one Skeleton, one Ooze, or any number of Goblins
  - **Cleric** defeats one Goblin, one Ooze, or any number of Skeletons
  - **Mage** defeats one Goblin, one Skeleton, or any number of Oozes
  - **Thief** defeats one Goblin, one Skeleton, or one Ooze
  - **Champion** may be used to defeat any number of Goblins, any number of Skeletons, or any number of Oozes
  - **Scrolls** allow re-rolling of dice in any phase

### Heroes
- Start as a Novice hero with a unique specialty
- Can be upgraded to Master rank by gaining experience
- Have powerful ultimate abilities that can turn the tide of battle
- Available Heroes:
  - **Minstrel/Bard**
    - Specialty: Thieves may be used as Mages and Mages may be used as Thieves (Mages can open any number of chests like Thieves)
    - Novice Ultimate: Discard all dice from the Dragon's Lair
    - Master Ultimate: Discard all dice from the Dragon's Lair + Champions can defeat monsters of TWO different types
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
   - Always shows Dragon's Lair count for threat assessment
3. **Loot Phase**: Open chests and use potions
   - **Opening Chests**: One Thief or Champion may be used to open any number of Chests in the level. Any other Companion may be used to open one Chest. For each Chest opened the Adventurer draws one Treasure Token. In the rare case that no Treasure tokens remain in the pool, the Adventure receives one Experience token instead.
   - **Quaffing Potions**: Any Party die (including Scrolls) can be used to Quaff any number of Potions. For each Potion quaffed the Adventurer takes 1 Party die from the Graveyard and adds it to the active party, choosing its face.
   - **Scroll Usage**: Can use Scrolls to re-roll dice for better loot results
4. **Dragon Phase**: Deal with any dragons in the Dragon's Lair
5. **Regroup Phase**: Choose to continue delving or retire to safety
   - Displays dragon dice count for threat assessment
   - Shows collected treasure items with descriptions
   - Provides complete resource overview for strategic decisions
   - Can use Scrolls to re-roll party dice before deciding to continue or retire

### Dragon Phase Mechanics
- **Triggers when 3+ dragon dice** are in the Dragon's Lair
- **Requires exactly 3 different companion types** to battle the dragon
- **Manual companion selection** - choose which companions to use (Scrolls and Champions are not companions)
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

### Game Flow and Pauses
The game includes strategic pauses between phases to enhance your experience:

- **Setup Phase Pause**: Review your starting party and dungeon state before the first monster encounter
- **Monster Phase Pause**: Analyze combat results and remaining monsters before collecting loot
- **Loot Phase Pause**: Review treasure gained and remaining items before the next phase
- **Dragon Phase Pause**: Assess dragon battle results before regrouping (only when dragons are present)
- **Between Delve Pause**: Review your progress and prepare for the next delve (except after the final delve)

Each pause shows a clear phase completion message and allows you to review the current game state. Simply press **Enter** when you're ready to continue to the next phase. The screen automatically clears between phases for a clean presentation.

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

## Recent Updates

### Code Documentation Cleanup (Latest)
- **Removed color references from dice documentation** - Cleaned up docstrings in `dice.py` to remove "white party dice" and "black dungeon dice" references
- **Improved code clarity** - Documentation now focuses on functionality rather than physical appearance
- **Consistent terminology** - All dice references use generic "party dice" and "dungeon dice" terminology
- **No functional impact** - Changes are purely cosmetic and don't affect game mechanics

### Monster Defeat Mechanics (Latest)
- **Fixed all companion monster defeat abilities** to match game rules exactly
- **Fighters, Clerics, and Mages** can now choose between defeating ALL of their primary monster type OR individual monsters of other types they can handle
- **Enhanced player choice** - When companions have monsters of their primary type, players can choose their preferred strategy
- **Champions** can defeat all monsters of a chosen type (player selects which type)
- **Thieves** correctly defeat any single monster (unchanged)
- **Enhanced user experience** with clear messaging for multiple monster defeats

### Hero Specialties (Latest)
- **Minstrel/Bard specialty** now works correctly in both monster combat and chest opening
- **Mages can open any number of chests** when playing Minstrel/Bard (like Thieves)
- **Thieves and Mages are interchangeable** for monster defeat when playing Minstrel/Bard
- **Passive specialty activation** - no manual activation required

### User Experience Enhancements (Latest)
- **Added strategic pause system** between all major game phases
- **Player-controlled pacing** - you decide when to proceed to the next phase
- **Enhanced strategic review** - time to analyze current game state and plan next moves
- **Clear phase boundaries** with visual completion indicators
- **Automatic screen clearing** between phases for cleaner presentation

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