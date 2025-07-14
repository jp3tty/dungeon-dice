# Dungeon Dice Changelog

## [Unreleased] - 2024-12-19

### Added
- **New Hero: Archaeologist/Tomb Raider** (2024-12-19 19:00)
  - Added ArchaeologistTombRaiderHero class with formation and end-game specialties
  - **Formation Specialty**: Draw 2 Treasure Tokens when forming the party
  - **End-Game Specialty**: Discard 6 Treasure Tokens at game end
  - **Novice Ultimate**: Treasure Seeker - Draw 2 Treasure Tokens, then discard 2
  - **Master Ultimate**: Treasure Seeker - Draw 2 Treasure Tokens, then discard 1
  - Integrated with existing treasure pool system for seamless gameplay
- Flexible hero specialty system for future heroes (2024-12-19 19:00)
  - Added `apply_formation_specialty()` and `apply_end_game_specialty()` methods to base HeroCard class
  - System supports heroes with party formation and end-game mechanics
  - Easy to extend for future heroes with similar specialty requirements
- Dragon die count display in Regroup Phase (2024-12-19 14:30)
  - Added "🐉 Dragon Dice in Lair: X" message to show number of dragon dice present during regroup decisions
- **Enhanced Regroup Phase display** (2024-12-19 21:30)
  - Added dragon dice count display in Regroup Phase for better threat assessment
  - Added collected treasure items list with descriptions for strategic planning
  - Improved organization with grouped resource sections
  - Enhanced readability with consistent formatting and bullet points
- **Modular Dragon Phase** (2024-12-19 20:00)
  - Separated Dragon Phase mechanics into dedicated `dragon_phase.py` module
  - Improved code organization and maintainability
  - Eliminated duplicate Dragon Phase implementations

### Changed
- Removed redundant hero display after selection (2024-12-19 15:15)
  - Eliminated the "Your Chosen Hero" section that appeared after hero selection in both `main.py` and `dungeon_dice_game.py`
  - Hero information is still available during gameplay through game state displays
- Updated combat terminology for clarity (2024-12-19 16:45)
  - Changed "Any number of" to "All of the" for companion abilities in monster combat
  - Affects Champions, Fighters, Clerics, and Mages descriptions and combat messages
  - Updated both `phases.py` and `README.md` to reflect new terminology
- Fixed Dragon Phase trigger condition (2024-12-19 17:30)
  - Changed Dragon Phase trigger from requiring 3+ dragons to requiring 1+ dragon
  - Fixed inconsistent behavior where Dragon Phase would skip when dragons were present
  - Updated message from "Not enough dragons to attract attention" to "No dragons in the lair"
- **Updated Dragon Phase trigger condition** (2024-12-19 20:30)
  - Changed Dragon Phase trigger back to requiring 3+ dragons for more strategic gameplay
  - Updated message to "Not enough dragons in the lair to attract attention"
  - Creates more tension and strategic decision-making before Dragon Phase begins
- **Fixed Dragon Phase mechanics** (2024-12-19 20:00)
  - Consolidated to single Dragon Phase implementation with proper mechanics
  - **Requires exactly 3 different companion types** to battle the dragon
  - **Manual companion selection** including treasure companions
  - **Deterministic success** when 3 different types are selected
  - **Proper treasure integration** - treasure tokens can be used as companions
  - **Consistent reward structure** (1 treasure + 1 experience + 1 drawn treasure)
  - Removed random chance-based system in favor of strategic companion selection
- **Fixed Scroll mechanics in Dragon Phase** (2024-12-19 21:00)
  - **Scrolls are no longer considered companions** for dragon battles
  - **Added Scroll usage during dragon battle** - can re-roll dice before combat
  - **Strategic depth** - players can improve party composition before dragon battle
  - **Clear messaging** - players understand Scrolls are utility items, not combat companions
- **Fixed treasure token display** (2024-12-19 20:00)
  - Treasure tokens now properly displayed in "Active Party Dice" section during Monster Phase
  - Treasure companions integrated into party dice counts
  - Eliminated separate "Treasure Companions" section for cleaner display
- Fixed Alchemist/Thaumaturge ultimate ability (2024-12-19 18:00)
  - Changed from random selection to player choice for revived companions
  - Now allows player to select which companions to revive from graveyard
  - Added proper interaction for both Novice (1 die) and Master (2 dice) abilities

### Technical Details
- Modified `hero.py`: Added ArchaeologistTombRaiderHero class with specialty methods (2024-12-19 19:00)
- Modified `main.py`: Added hero to available heroes list and integrated specialty system (2024-12-19 19:00)
- Modified `dungeon_dice_game.py`: Added hero to available heroes list and integrated specialty system (2024-12-19 19:00)
- Modified `hero.py`: Added flexible specialty system methods to base HeroCard class (2024-12-19 19:00)
- Modified `dungeon_dice_game.py`: Added dragon count display in regroup_phase() (2024-12-19 14:30)
- Modified `main.py`: Removed hero display after selection (2024-12-19 15:15)
- Modified `dungeon_dice_game.py`: Removed hero display after selection (2024-12-19 15:15)
- Modified `phases.py`: Updated all combat descriptions and messages (2024-12-19 16:45)
- Modified `README.md`: Updated game rules documentation (2024-12-19 16:45)
- Modified `main.py`: Fixed Dragon Phase trigger condition in DragonPhase.execute() (2024-12-19 17:30)
- Modified `hero.py`: Fixed AlchemistThaumaturgeHero.use_ultimate() to allow player choice (2024-12-19 18:00)

### Files Changed
- `hero.py`
- `main.py`
- `dungeon_dice_game.py`
- `phases.py`
- `README.md`
- `dd_changelog.md` (new file - 2024-12-19 17:00) 