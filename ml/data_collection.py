import pandas as pd
from sklearn.preprocessing import StandardScaler
import pygame

# Initialize an empty DataFrame to store game data
data = pd.DataFrame(columns=[
    'player_x', 'player_y', 'player_health', 'player_speed', 'time_since_last_attack', 'game_time',
    'closest_enemy_x', 'closest_enemy_y', 'closest_enemy_health', 'closest_enemy_speed', 'closest_enemy_distance',
    'player_action'
])

# Initialize the scaler
scaler = StandardScaler()

def collect_game_data(player, enemies):
    # Collect player data
    player_x, player_y = player.get_position()
    player_health = player.health
    player_speed = player.speed
    time_since_last_attack = pygame.time.get_ticks() - player.last_attack_time
    game_time = pygame.time.get_ticks()

    # Identify the closest enemy
    closest_enemy = min(enemies, key=lambda enemy: pygame.math.Vector2(player_x, player_y).distance_to(enemy.get_position()))
    closest_enemy_x, closest_enemy_y = closest_enemy.get_position()
    closest_enemy_health = closest_enemy.health
    closest_enemy_speed = closest_enemy.speed
    closest_enemy_distance = pygame.math.Vector2(player_x, player_y).distance_to((closest_enemy_x, closest_enemy_y))

    # Collect player action
    player_action = player.current_action  # Replace with actual logic to get the player's action

    return [player_x, player_y, player_health, player_speed, time_since_last_attack, game_time,
            closest_enemy_x, closest_enemy_y, closest_enemy_health, closest_enemy_speed, closest_enemy_distance,
            player_action]

def preprocess_data(data):
    X = data.drop('player_action', axis=1)
    y = data['player_action']
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y