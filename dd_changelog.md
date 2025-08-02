# Dungeon Dice Changelog

## [Unreleased] - 2025-08-02

### Fixed
- **Fixed Scroll re-roll IndexError in Regroup Phase** (2025-08-02)
  - **Fixed list index out of range error** - Scroll usage during regroup phase no longer causes IndexError when re-rolling dice
  - **Resolved index shifting issue** - Fixed bug where removing scroll from party dice shifted subsequent indices incorrectly
  - **Added proper index adjustment** - Re-roll logic now accounts for scroll removal by adjusting target die index when needed
  - **Enhanced user experience** - Players can now successfully use scrolls to re-roll any party die without crashes
  - **Preserved game mechanics** - All scroll functionality remains intact, only the index calculation was corrected

## [Unreleased] - 2025-07-31

### Fixed
- **Fixed Thaumaturge hero companion revival issue** (2025-07-31)
  - **Fixed invalid choice handling** - Thaumaturge hero's ultimate ability no longer skips companion revival when invalid choices are made
  - **Added dynamic companion display** - Shows available companions in graveyard for each selection, not just initially
  - **Implemented retry mechanism** - Players can retry invalid selections instead of losing revival opportunities
  - **Enhanced user experience** - Clear error messages guide players to make valid selections
  - **Preserved game mechanics** - All companion revivals are completed as intended, no revivals are skipped

## [Unreleased] - 2025-07-29

### Fixed
- **Fixed Dragon dice handling in Loot Phase** (2025-07-29)
  - **Fixed missing Dragon lair movement** - Dragon dice rolled during loot phase re-rolls now properly move to Dragon's Lair
  - **Added Dragon detection logic** - Loot phase now checks if re-rolled dungeon dice become Dragons
  - **Consistent Dragon handling** - Matches the same Dragon lair movement logic used in Dragon Phase
  - **Enhanced user feedback** - Shows "Rolled a Dragon! It goes to the Dragon's Lair." message when Dragon appears
  - **Proper dice management** - Removes old die from dungeon dice and adds new Dragon die to lair
  - **Preserved game mechanics** - All other re-roll functionality remains unchanged

- **Fixed missing party dice in Loot Phase scroll re-rolls** (2025-07-29)
  - **Fixed incorrect scroll exclusion logic** - Party dice were being incorrectly excluded from re-roll options after scroll usage
  - **Resolved index shifting issue** - Scroll removal was changing party dice indices, causing wrong dice to be excluded
  - **Simplified logic** - Removed unnecessary exclusion check since scroll is already removed from party dice
  - **Enhanced user experience** - All party dice now properly appear as re-roll options after using a scroll

### Changed
- **Improved Dragon Phase scroll timing** (2025-07-29)
  - **Moved scroll option before companion selection** - Players can now use scrolls to re-roll dice before choosing dragon battle companions
  - **Enhanced strategic planning** - Allows players to potentially improve party composition before committing to battle companions
  - **Better user experience** - More logical flow where scroll usage precedes companion selection
  - **Updated messaging** - Changed prompt from "before the battle" to "before selecting companions" for clarity

- **Separated treasure companions from Active Party Dice display** (2025-07-29)
  - **Removed treasure counting from Active Party Dice** - Treasure tokens that act as companions are no longer counted in the "Active Party Dice" section
  - **Preserved treasure availability** - Treasure companions still appear in "Available Companions" list during monster combat
  - **Enhanced clarity** - "Active Party Dice" now only shows actual party dice, while "Carried Treasure" shows treasure items separately
  - **Improved user experience** - Clearer distinction between actual party dice and treasure items that can act as companions

- **Fixed dragon lair persistence between delves** (2025-07-29)
  - **Added dragon lair clearing on flee** - Dragon's lair is now cleared when players flee from dragons or monsters
  - **Enhanced game balance** - Dragons no longer persist between delves when fleeing, preventing unfair dragon encounters
  - **Improved user feedback** - Clear messaging shows when dragon dice are returned to the available pool
  - **Consistent behavior** - Dragon lair is cleared whether fleeing from monsters or dragons, maintaining game balance

## [Unreleased] - 2025-07-28

### Added
- **"Stuff of Legend" Level 10 Victory Condition** (2025-07-28)
  - **Added automatic retirement at level 10** - Players must retire when they successfully clear level 10
  - **Implemented legendary achievement** - Special "Stuff of Legend" messaging celebrates the milestone
  - **Fixed experience reward** - Awards exactly 10 experience tokens (not level-based amount)
  - **Required dragon defeat** - Players must defeat any dragons in the lair before achieving "Stuff of Legend"
  - **Complete victory requirement** - Only defeating both monsters and dragons (if present) qualifies for legendary status
  - **Proper game flow** - Dragon phase occurs before regroup phase, ensuring dragons are dealt with first
  - **Automatic cleanup** - Returns dragon dice to available pool and ends delve cleanly

## [Unreleased] - 2025-07-24

### Fixed
- **Fixed hero specialty application bug** (2025-07-24)
  - **Fixed incorrect specialty activation** - Minstrel/Bard specialty was being applied to all heroes instead of only when Minstrel/Bard was selected
  - **Added proper hero type checking** - Monster phase now correctly checks if the current hero is Minstrel/Bard before applying specialty
  - **Isolated hero specialties** - Each hero's specialty now only activates when that specific hero is selected
  - **Enhanced gameplay integrity** - Players no longer receive specialty options from heroes they haven't selected
  - **Preserved intended mechanics** - Minstrel/Bard specialty still works correctly when Minstrel/Bard is the selected hero

## [Unreleased] - 2025-07-23

### Changed
- **Improved hero level-up messages** (2025-07-23)
  - **Added new ultimate ability display** - Hero level-up now always shows the new ultimate ability when ascending to Expert rank
  - **Smart specialty display** - Only shows specialty changes when they actually change (most heroes keep same specialty)
  - **Enhanced user experience** - Players now see the most important upgrade (ultimate ability) prominently displayed
  - **Accurate information** - Eliminates confusion about specialty changes that don't actually occur

- **Fixed dragon phase companion tracking** (2025-07-23)
  - **Fixed missing companions in graveyard** - Companions used in dragon battles now properly appear in graveyard during regroup phase
  - **Improved indexing reliability** - Dragon phase now finds actual dice in party list instead of relying on potentially invalid stored indices
  - **Enhanced scroll compatibility** - Fixed issue where scroll re-rolls during dragon battle could cause wrong companions to be moved to graveyard
  - **Added safety checks** - Warning message if selected companion is not found in party dice list
  - **Preserved treasure handling** - Treasure companions continue to work correctly and return to treasure pool

- **Renamed hero levels from "Master" to "Expert"** (2025-07-23)
  - **Updated all hero level references** - Changed "Master" rank to "Expert" rank throughout the codebase
  - **Updated hero names and abilities** - All hero progression now uses "Expert" terminology
  - **Updated documentation** - README and changelog now reflect "Expert" level terminology
  - **Updated user interface** - All displays now show "Expert" instead of "Master" for advanced heroes
  - **No functional impact** - This is purely a terminology change, all game mechanics remain the same

- **Removed color references from dice documentation** (2025-07-22)
  - **Cleaned up dice.py docstrings** - Removed "white party dice" and "black dungeon dice" color references
  - **Improved code clarity** - Dice documentation now focuses on functionality rather than physical appearance
  - **Consistent terminology** - All dice references now use generic "party dice" and "dungeon dice" terminology
  - **No functional impact** - Color removal is purely cosmetic and doesn't affect game mechanics

## [Unreleased] - 2025-07-20

### Added
- **Scroll Usage in All Phases** (2025-07-20 15:30)
  - **Added scroll usage to Loot Phase** - Players can now use scrolls to re-roll dice during loot collection
  - **Added scroll usage to Regroup Phase** - Players can now use scrolls to re-roll party dice before deciding to continue or retire
  - **Enhanced strategic flexibility** - Scrolls are now available in all four phases (Monster, Loot, Dragon, Regroup)
  - **Consistent interface** - Both new phases use the same scroll selection and re-roll mechanics as existing phases
  - **Smart availability** - Scroll options only appear when scrolls are actually available in the player's party
  - **Dynamic state updates** - Loot Phase updates chest and potion counts after scroll re-rolls
  - **Recursive phase restart** - Regroup Phase restarts after scroll usage to show updated game state

- **Dragon's Lair Display in Monster Phase** (2025-07-20 15:00)
  - **Added permanent Dragon's Lair section** - Always shows dragon count in Monster Phase display
  - **Enhanced visibility** - Dragon count is now prominently displayed whether dragons are present or not
  - **Clear status indication** - Shows "Empty" when no dragons are in the lair, shows count when dragons are present
  - **Improved strategic planning** - Players can always see dragon threat level during monster encounters

- **Bard Master Ability Implementation** (2025-07-20 14:30)
  - **Implemented "Champions defeat 1 extra monster"** - Bard's master ability now has meaningful gameplay impact
  - **Enhanced Champion power** - Champions can now defeat monsters of TWO different types when Bard is Master rank
  - **Two-stage selection process** - Players choose first monster type, then optionally choose a second type
  - **Flexible usage** - Players can choose to defeat only one type or both types with a single Champion
  - **Clear visual feedback** - Shows remaining monster types after first defeat with option to skip second choice
  - **Comprehensive implementation** - Updated both `use_champion()` and `use_companions()` methods
  - **Updated descriptions** - Monster defeat guide now shows "Champions can defeat monsters of TWO different types"

### Fixed
- **Minstrel/Bard Hero Specialty Logic** (2025-07-20 23:58)

### Added
- **Phase Pause System** (2025-07-18 23:50)
  - **Added pauses between all major phases** to improve game pacing and player experience
  - **Setup Phase pause** - Players can review starting party and dungeon state before first monster phase
  - **Monster Phase pause** - Players can review combat results and remaining monsters before loot phase
  - **Loot Phase pause** - Players can review treasure gained and remaining items before next phase
  - **Dragon Phase pause** - Players can review dragon battle results before regroup phase (only when dragons present)
  - **Between Delve pause** - Players can review delve summary and prepare for next delve (except after final delve)
  - **Enhanced user control** - Players control when to proceed to next phase with "Press Enter to continue"
  - **Clear phase boundaries** - Visual indicators show when each phase completes
  - **Screen clearing** - Automatic screen clear between phases for cleaner presentation
  - **Strategic review time** - Players can analyze current game state and plan next moves

### Fixed
- **Minstrel/Bard Hero Specialty Logic** (2025-07-20 23:58)
  - **Fixed automatic transformation bug** - Thieves and Mages are no longer automatically transformed to the other type
  - **Added player choice** - When using Thieves or Mages with Minstrel/Bard specialty, players can choose to use original abilities or the other type's abilities
  - **Enhanced user experience** - Clear messaging shows both options: "Use as [original type] (original abilities)" or "Use as [other type] (defeat all Oozes, open all chests)"
  - **Preserved specialty benefits** - Thieves can still defeat all Oozes and open all chests, Mages can still defeat all Oozes and open all chests
  - **Updated loot phase** - Chest opening now properly handles Minstrel/Bard specialty without automatic transformation
  - **Fixed simulation methods** - Automatic monster defeat now intelligently chooses the best option for Thieves/Mages with specialty

- **Treasure Companions in Loot Phase** (2025-07-20 23:59)
  - **Added treasure companions to chest opening** - Treasure items that act as companions (like Thieves' Tools) are now available options for opening chests
  - **Enhanced companion selection** - Both party dice and treasure companions are shown with clear labels ("Party:" vs "Treasure:")
  - **Proper treasure handling** - Treasure companions are used and returned to the treasure pool, while party dice are moved to the graveyard
  - **Consistent behavior** - Treasure companions follow the same rules as their corresponding companion types for chest opening abilities

- **Monster Defeat Rules** (2025-07-18 23:55)

- **Chest Opening and Potion Rules** (2025-07-18 23:55)
  - **Corrected chest opening rules** - One Thief or Champion may be used to open any number of Chests in the level. Any other Companion may be used to open one Chest
  - **Corrected potion rules** - Any Party die (including Scrolls) can be used to Quaff any number of Potions. For each Potion quaffed the Adventurer takes 1 Party die from the Graveyard and adds it to the active party, choosing its face
  - **Updated loot phase messaging** - Clear descriptions of chest opening and potion quaffing abilities
  - **Preserved treasure token mechanics** - For each Chest opened the Adventurer draws one Treasure Token. In the rare case that no Treasure tokens remain in the pool, the Adventure receives one Experience token instead

- **Monster Defeat Mechanics** (2025-07-18 23:45)

- **Monster Defeat Mechanics** (2025-07-18 23:30)
  - **Fixed Champion mechanics** - Champions now properly defeat all monsters of a chosen type instead of just one
  - **Fixed Fighter mechanics** - Fighters now automatically defeat ALL Goblins instead of just one
  - **Fixed Cleric mechanics** - Clerics now automatically defeat ALL Skeletons instead of just one  
  - **Fixed Mage mechanics** - Mages now automatically defeat ALL Oozes instead of just one
  - **Thief mechanics unchanged** - Thieves correctly defeat any single monster (was already working)
  - **Updated all simulation methods** - `can_defeat_monsters` and `use_companions_for_remaining_monsters` now properly simulate the correct monster defeat behavior
  - **Enhanced user experience** - Clear messaging when companions defeat multiple monsters
  - **Preserved specialty mechanics** - Minstrel/Bard specialty and Master Bard Champion bonus still work correctly

- **Minstrel/Bard Hero Specialty** (2025-07-18 23:15)
  - **Fixed chest opening mechanics** - Mages can now open any number of chests (like Thieves) when playing Minstrel/Bard
  - **Monster phase already working** - Thieves and Mages are properly interchangeable for monster defeat
  - **Passive specialty** - No manual activation required, specialty is always active when Minstrel/Bard is selected
  - **Clear visual indicators** - Shows when specialty is active with ✨ symbols and descriptive text

### Added
- **Modular Phase Architecture** (2025-07-18 23:00)
  - **Separated phases into individual modules** for improved code organization
  - **monster_phase.py**: Contains MonsterPhase class with all monster combat mechanics
  - **loot_phase.py**: Contains LootPhase class with treasure and potion mechanics
  - **regroup_phase.py**: Contains RegroupPhase class with delve continuation logic
  - **dragon_phase.py**: Already existed as separate module (unchanged)
  - **phases.py**: Now serves as central import hub for all phase modules
  - **Enhanced maintainability** - each phase is now in its own dedicated file
  - **Improved code organization** - easier to locate and modify specific phase logic
  - **Preserved gameplay** - all game mechanics and player experience remain identical
- **New Hero: Archaeologist/Tomb Raider** (2024-12-19 19:00)
  - Added ArchaeologistTombRaiderHero class with formation and end-game specialties
  - **Formation Specialty**: Draw 2 Treasure Tokens when forming the party
  - **End-Game Specialty**: Discard 6 Treasure Tokens at game end
  - **Novice Ultimate**: Treasure Seeker - Draw 2 Treasure Tokens, then discard 2
  - **Expert Ultimate**: Treasure Seeker - Draw 2 Treasure Tokens, then discard 1
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
- **Fixed Tomb Raider treasure discard crashes** (2024-12-19 22:30)
  - Fixed IndexError when Tomb Raider discards treasures during both ultimate ability and end-game scoring
  - Issue occurred when trying to access treasure name after treasure was removed from list
  - Solution: Store treasure name before using treasure to avoid index out of range error
  - Game now properly handles treasure discarding for both ultimate ability and final scoring phase
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
- **Added Carried Treasure display to Monster Phase** (2024-12-19 22:00)
  - Added "💎 Carried Treasure" section between Active Party Dice and Graveyard
  - Shows all collected treasure items with descriptions during Monster Phase
  - Improves strategic decision-making by making treasure availability visible
  - Particularly helpful for heroes like Archaeologist who start with treasure tokens
- Fixed Alchemist/Thaumaturge ultimate ability (2024-12-19 18:00)
  - Changed from random selection to player choice for revived companions
  - Now allows player to select which companions to revive from graveyard
  - Added proper interaction for both Novice (1 die) and Master (2 dice) abilities

### Technical Details
- **Modified `monster_phase.py`**: Added permanent Dragon's Lair display section and implemented Bard master ability for Champions (2025-07-20 15:00)
- **Modified `loot_phase.py`**: Added scroll usage functionality with `use_scroll()` method and updated action menu (2025-07-20 15:30)
- **Modified `regroup_phase.py`**: Added scroll usage functionality with `use_scroll()` method and updated action menu (2025-07-20 15:30)
- **Modified `phases.py`**: Converted to import hub, removed all phase class implementations (2025-07-18 23:00)
- **Created `monster_phase.py`**: Extracted MonsterPhase class with all monster combat logic (2025-07-18 23:00)
- **Created `loot_phase.py`**: Extracted LootPhase class with treasure and potion mechanics (2025-07-18 23:00)
- **Created `regroup_phase.py`**: Extracted RegroupPhase class with delve continuation logic (2025-07-18 23:00)
- **Modified `main.py`**: Updated imports to use new modular phase structure (2025-07-18 23:00)
- Modified `hero.py`: Fixed Tomb Raider ultimate ability and end-game specialty to prevent IndexError (2024-12-19 22:30)
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
- `phases.py` (converted to import hub)
- `monster_phase.py` (new file)
- `loot_phase.py` (new file)
- `regroup_phase.py` (new file)
- `main.py` (updated imports)
- `hero.py`
- `dungeon_dice_game.py`
- `README.md`
- `dd_changelog.md` (new file - 2024-12-19 17:00) 