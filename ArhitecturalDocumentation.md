# Arhitectural Documentation - Mimic Fighter #

## Project Description ##
This project is a Python-based 2D game in which an AI algorithm learns the player’s unique playstyle in real time. Using collected data on player actions and strategies, the machine learning model develops a behavior profile that it later uses to control a non-player character (NPC) that mimics the player’s own tactics and preferences. The game combines elements of behavior cloning and reinforcement learning to create an adaptive, personalized gameplay experience. Built with Pygame and scikit-learn, and optionally scalable with TensorFlow for advanced learning, this project explores the intersection of game design and AI-driven adaptive behavior.

⚠️ The desired outcome of this project is not a **FULL IMPLEMENTATION** but rather a proof-of-concept. By the end of the development period, we aim to have implemented a basic game loop consisting of a few ( < 10 ) basic levels in which the player gets to fight one (max 2) types of enemies with simple attacks and basic movement. The AI will develop its behavior based on collected data such as: `attackType`, `enemyDistance`, `playerInput`, `health` (final fields to be discussed). ⚠️

## Project Structure ##

```bash
project-root/
│
├── game/                         # Core game code
│   ├── main.py                   # Main game loop and initialization
│   ├── player.py                 # Player class, handles movement, actions
│   ├── enemy.py                  # Enemy class, handles enemy attacks and movement
│   ├── npc.py                    # NPC class, handles behavior learned from player
│   ├── environment.py            # Environment setup (levels, obstacles, etc.)
│   └── assets/                   # Game assets (images, sounds)
│       ├── images/               # Sprites and graphics
│       └── sounds/               # Sound effects and music
│
├── ml/                           # Machine learning code
│   ├── data_collection.py        # Code to collect player data
│   ├── model.py                  # Model architecture and training code
│   ├── real_time_learning.py     # Real-time training and updating
│   └── train_model.py            # Script to train or retrain model offline
│
├── config/                       # Configuration files
│   ├── settings.py               # General game settings
│   └── ml_config.py              # ML model and training settings
│
├── data/                         # Data storage for training
│   ├── player_data.csv           # CSV file to log player actions
│   └── model/                    # Folder to save trained model files
│       └── npc_behavior_model.h5 # Serialized ML model
│
├── requirements.txt              # Dependencies for the project
└── README.md                     # Project description and instructions
```

⚠️This project structure is just a starting point we have found through some online-reasearch and will probably be adapted to our needs later down the line ⚠️

## System Overview ##
The game will be structured as a standalone, single-player application, without a client-server setup. The project’s structure includes:

- Frontend (Pygame): Handles game graphics and user interactions.
- Machine Learning Module: Collects and processes gameplay data, trains an ML model, and controls NPC behavior. scikit-learn will be used for initial model.
- Database Structure: Stores gameplay data in CSV files or a local SQLite database for model training. ⚠️ Not sure if we will end up doing this or just using local variables, depends on how much data we end up colecting from the player

## Detailed Component Design

### Graphics Component (Frontend): ###

- Main Game Module (main.py): Contains the main game loop and manages user interactions.
- Player Module (player.py): Manages player movement and actions, collects gameplay data for the ML model.
- NPC Module (npc.py): Integrates the ML model and controls NPC behavior based on player data.
- Enemy Module (enemy.py): Manages enemies, spawning, attacking, etc...

The plan for the main game is to create a basic game loop using pygame that loads the levels one by one and plays them until the last level is reached where we will have a special boos-fight. [GameLoop Docs](https://www.geeksforgeeks.org/how-to-set-up-the-game-loop-in-pyggame/)
The player will be able to move around, dash, meele-attack and mabye shoot something ( mabye ) [Player movement tutorial](https://opensource.com/article/17/12/game-python-moving-player)
The enemies ( [Docs For Enemies](https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-enemies) )
 will be implemented to be able to attack and their only logic will be:

```python
while 1:
    enemy.moveToPlayer()
    if enemy.inRange(player):
        enemy.attack_move(player)
```
The NPC will be coded to have the same ablities and controls as the player but he will do something like:
```python
while 1:
    action = mlModel.predict(player.getInfo())
    enemy.execute(action)
```

### Machine Learning Module: ###

- Data Collection: The data_collection.py function collects real-time information about player actions and behavior.
- Model Training: model.py implements the prediction model and functionality to adapt the NPC’s behavior.
- Model Integration and Testing: train_model.py manages model training and adjustment to optimize NPC control.

The plan here is to have an *Object* that hold player behavior like:
```python
class PlayerInfo:
    int health;
    int attackType;
    int enemyDistance;
    int playerInput;
    int[] movement;
    int[] playerPosition;
    int[] enemyPosition;
```
and the ML algorithm will take data such as `health`, `enemyDistance`, `playerPosition`, `enemyPosition` and determine `attackType` and `movement`.
It will be trained on the data gathered from the first levels.
[Docs for predincting using SikitLearn](https://machinelearningmastery.com/make-predictions-scikit-learn/)

### Database and Data Structure: ###
- CSV/SQLite: Collected data is stored for model training and optimization. Data will be structured as state-action pairs to enable learning of the player’s behavior. ⚠️ Again, not sure if we will end up needing this

I have seen the most ML models use some sort of data-base to keep track of all the data and learn from it, but since our model will reset after every new game, i dont know if it is necessary

## Deployment and Testing ##

**Execution Requirements:** The application runs on a local system without server or domain requirements, though a GPU may be optionally used for faster training of more complex ML models. No external services are needed.

**Containerization and Configuration Variables:** ***IF*** containerization is used (⚠️it is just an if for now), Docker will be configured to include all dependencies and necessary configuration variables.

**Testing Strategy:** The application will be manually tested, assessing the NPC’s behavior and the ML model’s adaptability to different playstyles.

## Conclusions ##
The whole idea for this project started as a joke one of us came up with during the first lecture of this semester and more of a "what if" or "imagine if we did this" but slowly it grew on us and we decided to try making it a reality. We dont know if we will succede or if it will even work at all, but we will make sure to give our best and try to make this work. It is a VERY complex project, we expect it to take around 50 hours of work and we will need to learn a lot both about ML and game-desing as neither of us have had any experience in theese fields, but we hope we can learn something from this and deliver an amazing finished project.

### Copyright © 2024 Prusacov Andrei-Ionut & Luchian Albert-Calin ###