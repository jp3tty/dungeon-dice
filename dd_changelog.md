# Dungeon Dice Changelog

## [Unreleased] - 2024-12-19

### Added
- Dragon die count display in Regroup Phase
  - Added "🐉 Dragon Dice in Lair: X" message to show number of dragon dice present during regroup decisions

### Changed
- Removed redundant hero display after selection
  - Eliminated the "Your Chosen Hero" section that appeared after hero selection in both `main.py` and `dungeon_dice_game.py`
  - Hero information is still available during gameplay through game state displays
- Updated combat terminology for clarity
  - Changed "Any number of" to "All of the" for companion abilities in monster combat
  - Affects Champions, Fighters, Clerics, and Mages descriptions and combat messages
  - Updated both `phases.py` and `README.md` to reflect new terminology

### Technical Details
- Modified `dungeon_dice_game.py`: Added dragon count display in regroup_phase()
- Modified `main.py`: Removed hero display after selection
- Modified `dungeon_dice_game.py`: Removed hero display after selection  
- Modified `phases.py`: Updated all combat descriptions and messages
- Modified `README.md`: Updated game rules documentation

### Files Changed
- `dungeon_dice_game.py`
- `main.py`
- `phases.py`
- `README.md`
- `dd_changelog.md` (new file) 