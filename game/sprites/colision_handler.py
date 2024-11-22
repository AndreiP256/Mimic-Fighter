import pygame
from game.player import player

class ColisionHandler:
    def __init__(self, enemies):
        self.enemies = enemies
        self.last_resolve_time = pygame.time.get_ticks()

    def check_collision(self, enemy):
        next_position = pygame.Rect(enemy.rect)
        next_position.center += enemy.direction * enemy.speed

        for other_enemy in self.enemies:
            if other_enemy != enemy and next_position.colliderect(other_enemy.rect):
                return True
        return False

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def resolve_overlaps(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_resolve_time >= 5000:  # 5 seconds
            for enemy in self.enemies:
                for other_enemy in self.enemies:
                    if enemy != other_enemy and enemy.rect.colliderect(other_enemy.rect):
                        overlap_vector = pygame.math.Vector2(enemy.rect.center) - pygame.math.Vector2(other_enemy.rect.center)
                        if overlap_vector.length() > 0:
                            overlap_vector.normalize_ip()
                            move_distance = overlap_vector * 5  # Move them apart by a small distance
                            enemy.rect.center += move_distance
                            other_enemy.rect.center -= move_distance
            self.last_resolve_time = current_time

    def enemies_in_cone(self, player, cone_angle=45, cone_distance=200):
        enemies_in_cone = []
        player_direction = pygame.math.Vector2(0, -1)  # Assuming 'up' is the default direction
        if player.prevDirection == 'right':
            player_direction = pygame.math.Vector2(1, 0)
        elif player.prevDirection == 'left':
            player_direction = pygame.math.Vector2(-1, 0)
        elif player.prevDirection == 'down':
            player_direction = pygame.math.Vector2(0, 1)
        elif player.prevDirection == 'up_right':
            player_direction = pygame.math.Vector2(1, -1).normalize()
        elif player.prevDirection == 'up_left':
            player_direction = pygame.math.Vector2(-1, -1).normalize()
        elif player.prevDirection == 'down_right':
            player_direction = pygame.math.Vector2(1, 1).normalize()
        elif player.prevDirection == 'down_left':
            player_direction = pygame.math.Vector2(-1, 1).normalize()

        for enemy in self.enemies:
            to_enemy = pygame.math.Vector2(enemy.rect.center) - pygame.math.Vector2(player.rect.center)
            distance_to_enemy = to_enemy.length()
            if(distance_to_enemy == 0):
                enemies_in_cone.append(enemy)
                continue
            if distance_to_enemy <= cone_distance:
                to_enemy.normalize_ip()
                angle = player_direction.angle_to(to_enemy)
                if abs(angle) <= cone_angle / 2:
                    enemies_in_cone.append(enemy)

        return enemies_in_cone
    def slash_attack(self, player: player):
        for enemy in self.enemies_in_cone(player, cone_angle=90, cone_distance=100):
            if player.rect.colliderect(enemy.rect):
                enemy.take_damage(player.slash_damage)
        

    def chop_attack(self, player: player):
        for enemy in self.enemies_in_cone(player, cone_angle=45, cone_distance=100):
            if player.rect.colliderect(enemy.rect):
                enemy.take_damage(player.chop_damage)