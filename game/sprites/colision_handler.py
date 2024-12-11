import pygame
from game.player import player
from config.game_settings import SLASH_DIMENSIONS, CHOP_DIMENSIONS

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

    def enemies_in_cone(self, player, cone_angle, cone_distance):
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
            if distance_to_enemy <= cone_distance:
                to_enemy.normalize_ip()
                angle = player_direction.angle_to(to_enemy)
                if abs(angle) <= cone_angle / 2:
                    enemies_in_cone.append(enemy)
        return enemies_in_cone

    def enemies_in_rectangle(self, player, rect_width, rect_height):
        enemies_in_rectangle = []
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

        start_pos = pygame.math.Vector2(player.rect.center)
        rect_center = start_pos + player_direction * rect_height / 2
        angle = player_direction.angle_to(pygame.math.Vector2(0, -1))

        rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        rotated_rect = pygame.transform.rotate(rect, angle)
        rect_pos = rotated_rect.get_rect(center=rect_center)

        attack_rect = pygame.Rect(rect_pos.x, rect_pos.y, rect_width, rect_height)

        for enemy in self.enemies:

            if attack_rect.colliderect(enemy.rect):
                enemies_in_rectangle.append(enemy)
        return enemies_in_rectangle

    def slash_attack(self, player: player):
        for enemy in self.enemies_in_rectangle(player, SLASH_DIMENSIONS[0], SLASH_DIMENSIONS[1]):
            if player.rect.colliderect(enemy.rect):
                enemy.take_damage(player.slash_damage)

    def chop_attack(self, player: player):
        for enemy in self.enemies_in_rectangle(player, CHOP_DIMENSIONS[0], CHOP_DIMENSIONS[1]):
            if player.rect.colliderect(enemy.rect):
                enemy.take_damage(player.chop_damage)

    def draw_rectangle(self, screen, player, rect_width, rect_height, color):
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

        start_pos = pygame.math.Vector2(player.rect.center)
        rect_center = start_pos + player_direction * (rect_height / 2 - 10)  # Move the rectangle 10 units behind the player
        angle = player_direction.angle_to(pygame.math.Vector2(0, -1))

        rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        pygame.draw.rect(rect, color, rect.get_rect(), 2)  # Draw the outline with thickness 2
        rotated_rect = pygame.transform.rotate(rect, angle)
        rect_pos = rotated_rect.get_rect(center=rect_center)

        screen.blit(rotated_rect, rect_pos.topleft)

    def draw_cone(self, screen, player, cone_angle=45, cone_distance=200):
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

        start_pos = pygame.math.Vector2(player.rect.center)
        left_boundary = player_direction.rotate(-cone_angle / 2) * cone_distance
        right_boundary = player_direction.rotate(cone_angle / 2) * cone_distance

        points = [
            start_pos,
            start_pos + left_boundary,
            start_pos + right_boundary
        ]

        pygame.draw.polygon(screen, (255, 0, 0), points, 2)  # Draw the cone with red color and a thickness of 2