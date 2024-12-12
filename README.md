# Mimic-Fighter
🎮 Python 2D game where you fight your way through a dungeon of enemies. 🎮
The game is available here [Mimic Fighter](https://www.github.com/AndreiP256/Mimic-Fighter)

## What We Implemented
- **Player Movement:** Full player movement with animations, including sprinting, rolling, and various attack types. 🏃‍♂️
- **Enemy AI:** Basic attack patterns and movement for both ranged and melee enemies. 🤖
- **Collision Detection:** Accurate collision detection (both with environment and for entities) and damage system. 💥
- **Level Design:** Customizable levels with tilesets using Tiled. 🗺️
- **Final Boss:** A challenging final boss encounter with a lot of animations and special attacks. 🏆
- **UI and HUD:** User interface and heads-up display for game information. 📊
- **Audio:** Sound effects and background music. 🎵
- **Special Ability:** Unique vortex ability for the player. 🌀

## FINAL project Structure 
As you can see, this s verry different betwen the initial plan and the final project structure. This is because we had to adapt to the needs of the project and we ended up having A LOT of classes
```bash
./game
├── assets
│   ├── A LOT OF ASSETS....
├── enemies
│   ├── enemy.py
│   ├── enemy_builder.py
│   ├── enemy_factory.py
│   ├── healthdrop.py
│   ├── momo_mama.py
│   ├── monster_pack_enemy.py
│   ├── skeleton_enemy.py
│   └── slime_enemy.py
├── environment.py
├── groups
│   └── all_sprites_group.py
├── healthbars
│   ├── ability_bar.py
│   ├── boss_bar.py
│   ├── enemy_healthbar.py
│   ├── healthbar.py
│   └── player_healthbar.py
├── main.py
├── npc.py
├── player
│   ├── Camera.py
│   ├── InputHandler.py
│   ├── Vortex_attack.py
│   └── player.py
├── screens
│   ├── button.py
│   ├── death_screen.py
│   ├── fades.py
│   ├── menu_screen.py
│   └── pause_screen.py
├── sounds
│   ├── sfx_loader.py
│   └── sound_manager.py
└── sprites
    ├── animated_sprite.py
    ├── colision_handler.py
    ├── merge_sheet.py
    ├── projectiles
    │   ├── enemy_projectile.py
    │   └── projectile.py
    ├── shift_spritesheet.py
    ├── sprite.py
    ├── tile_sprite.py
    └── tiles.py

```
## Controls

- **W/A/S/D or Arrow Keys** - Move ⬅️⬆️⬇️➡️
- **Space** - Roll 🔄
- **Left Click / K** - Slash Attack ⚔️
- **Right Click / L** - Chop Attack 🪓
- **Shift** - Sprint 🏃‍♂️
- **E** - Use Vortex Ability 🌀

## How to Run

1. Install Python 3.8.5 or later 🐍
2. Install PygameCE 1.2.0 or later 🎮
3. Run `python main.py` (from `./game` directory) ▶️
4. Enjoy! 🎉

## Technologies Used
- Python 🐍
- PygameCE 🎮
- Pillow 🖼️ (there was an AI attempt, it failed)

## Overview of Classes
- **./player:** 
  - contains the player class with all movement, animation, and attack logic.
  - contains input handler class that handles all player input.
  - contains Camera class that follows the player.
  - contains Vortex_attack class that handles the player's special ability.
- **./screens**:
  - contains all the menu screens and transitions.
  - contains button class that handles all button logic.
  - contains fades class that handles screen transitions.
  - contains death_screen class that handles the death screen.
  - contains pause_screen class that handles the pause screen.
- **./enemies**:
  - contains the enemy class that handles all enemy logic.
  - contains the enemy_builder class that builds the enemy.
  - contains the enemy_factory class that creates the enemy.
  - contains the healthdrop class that handles the health drop.
  - contains the momo_mama class that handles the final boss.
- **./sprites**:
  - contains the animated_sprite class that handles all sprite animations.
  - contains the colision_handler class that handles all collisions.
  - contains the merge_sheet class that merges sprite sheets. ( was used to make some sprites work )
  - contains projectiles folder that contains all projectile classes.
  - contains the shift_spritesheet class that shifts sprite sheets. ( was used to make some sprites work )
  - contains the tile_sprite class that handles all tile sprites.
- **./healthbars**:
  - contains the ability_bar class that handles the player's ability bar.
  - contains the boss_bar class that handles the boss's health bar.
  - contains the enemy_healthbar class that handles the enemy's health bar.
  - contains the healthbar class that handles the player's health bar.
  - contains the player_healthbar class that handles the player's health bar.
- **./sounds**:
  - contains the sfx_loader class that loads all sound effects.
  - contains the sound_manager class that manages all sound effects.

## Team Members and Contributions
- **Andrei-Ionut Prusacov**:
  - Implemented sound effects 🔊
  - Developed enemy logic and generic enemy class 🤖
  - Created slime enemies 🟢
  - Handled collisions and attack collisions 💥
  - Structured the project 🗂️
  - Documented the project 📄
  - Developed the initial sprite-animation class 🎨
  - Designed levels 🗺️
  - Designed the final boss 🏆
  - Implemented player special ability 🌀
  - Set up and designed levels 🗺️

- **Albert-Calin Luchian**:
  - Animated and implemented player movement 🏃‍♂️
  - Developed all projectile enemies 🎯
  - Handled environment collisions 💥
  - Created all menu screens 📋
  - Designed buttons 🔘
  - Implemented game camera 📷
  - Handled input ⌨️
  - Refactored code and fixed bugs 🐛
  - Designed the final boss 🏆

## WHY AI failed ##
- **Performance Issues:** The AI system was too complex and slowed down the game significantly. 🐢
- **Complexity:** The AI system was too complex for the scope of the project. 🤯
- **Time Constraints:** The AI system required more time than we had available. ( both to develop, and to train, so it couldnt work real-time) ⏳

In the future I would like to revisit the idea of implementing an AI system, but for now, it is not feasible.

## Difficulties Faced
- **AI Integration:** Initial attempts to integrate machine learning for NPC behavior were unsuccessful due to performance issues and complexity. 🤖
- **Collision Detection:** Ensuring accurate collision detection between player, enemies, and environment required multiple iterations and testing. 💥
- **Animation:** Implementing smooth animations for player and enemies was challenging due to the number of frames and sprites. 🎨
- **Different Sprites:** Creating and integrating different sprites for player, enemies, and environment was time-consuming. ( especially because none of them were standardized ) 🖼️

## Future Improvements
- **AI:** Implement a more advanced AI system with machine learning. 🤖
- **Levels:** Add more levels and more bosses. 🗺️
- **Items:** Add more items and power-ups. 🎁
- **Bug Fixes:** Fix any bugs or issues that arise. 🐛
- **Performance:** Optimize the game for better performance. 🚀

### Copyright © 2024 Prusacov Andrei-Ionut & Luchian Albert-Calin ###