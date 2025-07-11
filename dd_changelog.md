# Dungeon Dice Changelog

## [Unreleased] - 2024-12-19

### Added
- Dragon die count display in Regroup Phase (2024-12-19 14:30)
  - Added "🐉 Dragon Dice in Lair: X" message to show number of dragon dice present during regroup decisions

### Changed
- Removed redundant hero display after selection (2024-12-19 15:15)
  - Eliminated the "Your Chosen Hero" section that appeared after hero selection in both `main.py` and `dungeon_dice_game.py`
  - Hero information is still available during gameplay through game state displays
- Updated combat terminology for clarity (2024-12-19 16:45)
  - Changed "Any number of" to "All of the" for companion abilities in monster combat
  - Affects Champions, Fighters, Clerics, and Mages descriptions and combat messages
  - Updated both `phases.py` and `README.md` to reflect new terminology

### Technical Details
- Modified `dungeon_dice_game.py`: Added dragon count display in regroup_phase() (2024-12-19 14:30)
- Modified `main.py`: Removed hero display after selection (2024-12-19 15:15)
- Modified `dungeon_dice_game.py`: Removed hero display after selection (2024-12-19 15:15)
- Modified `phases.py`: Updated all combat descriptions and messages (2024-12-19 16:45)
- Modified `README.md`: Updated game rules documentation (2024-12-19 16:45)

### Files Changed
- `dungeon_dice_game.py`
- `main.py`
- `phases.py`
- `README.md`
- `dd_changelog.md` (new file - 2024-12-19 17:00) 