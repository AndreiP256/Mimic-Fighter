import pygame

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
