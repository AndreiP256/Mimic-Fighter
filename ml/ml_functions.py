import pygame

def get_current_state(player, enemyList):
    # Example state: player's position and health, and positions of all enemies
    state = [
        player.rect.x,
        player.rect.y,
        player.health
    ]
    for enemy in enemyList:
        state.extend([enemy.rect.x, enemy.rect.y, enemy.health])
    return state

def calculate_reward(player, enemyList):
    # Example reward: positive for defeating enemies, negative for taking damage
    reward = 0
    for enemy in enemyList:
        if enemy.health <= 0:
            reward += 10  # Reward for defeating an enemy
    if player.isDead:
        reward -= 50  # Penalty for player death
    return reward

def check_if_done(player, enemyList):
    # Example done condition: player is dead or all enemies are defeated
    if player.isDead:
        return True
    if all(enemy.health <= 0 for enemy in enemyList):
        return True
    return False

ACTION_MAPPING = {
    pygame.K_w: 1,
    pygame.K_s: 2,
    pygame.K_a: 3,
    pygame.K_d: 4,
    pygame.K_UP: 5,
    pygame.K_DOWN: 6,
    pygame.K_LEFT: 7,
    pygame.K_RIGHT: 8,
    pygame.K_LSHIFT: 9,
    pygame.K_SPACE: 10,
    pygame.MOUSEBUTTONDOWN: 11,
    pygame.MOUSEBUTTONUP: 12,
    pygame.KEYDOWN: 13,
    pygame.KEYUP: 14
}
def transform_action(action):
    if action.type == pygame.KEYDOWN or action.type == pygame.KEYUP:
        if action.key in ACTION_MAPPING:
            return ACTION_MAPPING[action.key]
    elif action.type == pygame.MOUSEBUTTONDOWN or action.type == pygame.MOUSEBUTTONUP:
        if action.button in ACTION_MAPPING:
            return ACTION_MAPPING[action.button]
    return 0  # Generic "other" action

def log_action(player, action, enemyList, collected_data):
    state = get_current_state(player, enemyList)
    reward = calculate_reward(player, enemyList)
    next_state = get_current_state(player, enemyList)
    done = check_if_done(player, enemyList)
    transformed_action = transform_action(action)
    collected_data.append((state, transformed_action, reward, next_state, done))