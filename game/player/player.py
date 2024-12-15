# game/player.py
import math
import string

from game.player.vortex_attack import AnimatedVortex
from game.sounds.sound_manager import SoundManager

from game.healthbars.ability_bar import AbilityBar
from config.game_settings import *
from game.healthbars.player_healthbar import PlayerHealthBar
from game.sprites.sprite import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, collision_tiles=None, sprite_group=None):
        super().__init__(sprite_group)
        self.direction = None
        self.collision_tiles = collision_tiles
        self.sprite_group = sprite_group
        self.spritesheet = Spritesheet(HERO_SPRITESHEET)
        self.sound_manager = SoundManager()
        self.baseSpeed = HERO_SPEED
        self.speed = HERO_SPEED
        self.max_health = HERO_MAX_HEALTH
        self.health = HERO_MAX_HEALTH
        self.vortex_damage = VORTEX_DAMAGE
        self.slash_damage = HERO_SLASH_DAMAGE
        self.chop_damage = HERO_CHOP_DAMAGE
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = HERO_FRAMERATE
        self.base_frame_rate = HERO_FRAMERATE
        self.roll_frame_rate = HERO_ROLL_FRAMERATE
        self.animations = self.load_animations(*HERO_FRAME_SIZE)
        self.current_animation = 'idle_down'
        self.frames = self.animations[self.current_animation]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.collision_rect = pygame.Rect(0, 0, int(self.rect.width * 0.3), int(self.rect.height * 0.25))
        self.collision_rect.center = self.rect.center
        self.prevDirection : string = 'down'
        self.direction : string = None
        self.isRunning : bool = False
        self.attack_move = None
        self.vortex_radius = VORTEX_RADIUS
        self.isAttacking = False
        self.isRolling = False
        self.healthBar = PlayerHealthBar(PLAYER_BAR_X, PLAYER_BAR_Y, PLAYER_BAR_WIDTH, PLAYER_BAR_HEIGHT, self.health)
        self.abilityBar = AbilityBar(ABILITY_BAR_X, ABILITY_BAR_Y, PLAYER_BAR_WIDTH, PLAYER_BAR_HEIGHT, SPECIAL_ENEMIES_KILLED)
        self.last_roll_time = 0
        self.isDying = False
        self.isDead = False
        self.last_attack_time = 0
        self.enemies_killed = 0
        self.vortex_move : AnimatedVortex = None
        self.isSpecialAttacking = False

    def update_animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        if self.current_animation == 'dying' and self.current_frame == len(self.frames) - 1:
            self.isDead = True
        if self.isRolling or self.isAttacking:
            if self.current_frame == len(self.frames) - 1:
                self.stop_attack()
                self.stop_roll()
                self.do_idle()



    def load_animations(self, frame_width : int, frame_height : int) -> dict:
        animations = {}
        directions = ['up', 'right', 'down', 'left']
        actions = ['idle', 'move', 'run', 'chop', 'slash', 'roll']
        frame_counts = {
            'idle': 12,
            'move': 8,
            'run': 8,
            'chop': 4,
            'slash': 7,
            'roll': 8
        }
        for i, direction in enumerate(directions):
            for action in actions:
                row = i * len(actions) + actions.index(action)
                if direction == 'left':
                    animations[f'{action}_{direction}'] = [pygame.transform.flip(frame, True, False) for frame in
                                                           animations[f'{action}_right']]
                else:
                    nr_frames = frame_counts[action]
                    if f'{action}_{direction}' == 'slash_right':
                        nr_frames = 5
                    if f'{action}_{direction}' == 'roll_right':
                        nr_frames = 6
                    animations[f'{action}_{direction}'] = self.load_frames(frame_width, frame_height,
                                                                           nr_frames, row)
        for action in actions:
            animations[f'{action}_up_right'] = animations[f'{action}_right']
            animations[f'{action}_down_right'] = animations[f'{action}_right']
            animations[f'{action}_up_left'] = animations[f'{action}_left']
            animations[f'{action}_down_left'] = animations[f'{action}_left']
        animations['dying'] = self.load_frames(frame_width, frame_height, 13, 18)
        return animations

    def update(self, delta_time):
        self.healthBar.update_details(self.health)
        self.abilityBar.update_details(self.enemies_killed)
        if self.isDead:
            return
        if self.isDying:
            self.update_animation(delta_time)
            return
        if not self.isSpecialAttacking:
            self.attack()
            if self.isRolling:
                self.direction = self.prevDirection
            self.move(delta_time)
            if self.direction is not None:
                self.prevDirection = self.direction
        else:
            self.do_special_attack()
        self.update_animation(delta_time)

    def draw_debug(self, screen):
        # Draw the player's sprite rectangle (red)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red rectangle for the full sprite

        # Draw the collision rectangle (green)
        pygame.draw.rect(screen, (0, 255, 0), self.collision_rect, 2)  # Green rectangle for collision

    def get_position(self):
        return self.rect.center

    def load_frames(self, frame_width : int, frame_height : int, num_frames : int, row : int, flip=False) -> list:
        frames = []
        for i in range(num_frames):
            x = i * frame_width
            y = row * frame_height
            frame = self.spritesheet.get_image(x, y, frame_width, frame_height)
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)
        return frames

    def set_animation(self, animation):
        if animation in self.animations and self.current_animation != animation:
            self.current_animation = animation
            self.frames = self.animations[self.current_animation]
            self.current_frame = 0

    def take_damage(self, damage : int) -> bool:
        if self.isRolling:
            return False
        else:
            self.health -= damage
            self.sound_manager.play_sound('human_damage')
            if self.health <= 0:
                self.isDying = True
                self.set_animation('dying')
        return True

    def move_right(self):
        if self.direction == 'up':
            self.direction = 'up_right'
        elif self.direction == 'down':
            self.direction = 'down_right'
        elif self.direction is None:
            self.direction = 'right'


    def move_left(self):
        if self.direction == 'up':
            self.direction = 'up_left'
        elif self.direction == 'down':
            self.direction = 'down_left'
        elif self.direction is None:
            self.direction = 'left'

    def move_down(self):
        if self.direction == 'right':
            self.direction = 'down_right'
        elif self.direction == 'left':
            self.direction = 'down_left'
        elif self.direction is None:
            self.direction = 'down'

    def move_up(self):
        if self.direction == 'right':
            self.direction = 'up_right'
        elif self.direction == 'left':
            self.direction = 'up_left'
        elif self.direction is None:
            self.direction = 'up'

    def stop(self):
        self.direction = None

    def sprint(self):
        if not self.isRunning:
            self.speed = self.baseSpeed * HERO_SPRINT_MULTIPLIER
        self.isRunning = True

    def stop_sprint(self):
        self.speed = self.baseSpeed
        self.isRunning = False

    def do_chop(self):
        if self.can_attack():
            self.sound_manager.play_sound('chop')
            self.attack_move = 'chop'

    def do_slash(self):
        if self.can_attack():
            self.sound_manager.play_sound('slash')
            self.attack_move = 'slash'

    def roll(self):
        if self.can_roll():
            self.sound_manager.play_sound('roll')
            self.frame_rate = self.roll_frame_rate
            self.isRolling = True
            self.last_roll_time = pygame.time.get_ticks()

    def stop_roll(self):
        self.isRolling = False
        self.direction = None
        self.speed = self.baseSpeed
        self.frame_rate = self.base_frame_rate

    def attack(self):
        if self.attack_move is not None:
            if self.prevDirection is None:
                self.set_animation(self.attack_move + '_up')
            else:
                self.set_animation(self.attack_move + '_' + self.prevDirection)
            self.isAttacking = True
            self.last_attack_time = pygame.time.get_ticks()
        self.attack_move = None

    def stop_attack(self):
        self.isAttacking = False
        self.do_idle()

    def move(self, delta_time):
        if self.isRolling:
            self.speed = self.baseSpeed * HERO_ROLL_MULTIPLIER
        diagonal_speed = self.speed / math.sqrt(2)
        original_position = self.rect.topleft

        if self.direction == 'right':
            self.rect.x += self.speed * delta_time
        elif self.direction == 'left':
            self.rect.x -= self.speed * delta_time
        elif self.direction == 'up':
            self.rect.y -= self.speed * delta_time
        elif self.direction == 'down':
            self.rect.y += self.speed * delta_time
        elif self.direction == 'up_right':
            self.rect.x += diagonal_speed * delta_time
            self.rect.y -= diagonal_speed * delta_time
        elif self.direction == 'up_left':
            self.rect.x -= diagonal_speed * delta_time
            self.rect.y -= diagonal_speed * delta_time
        elif self.direction == 'down_right':
            self.rect.x += diagonal_speed * delta_time
            self.rect.y += diagonal_speed * delta_time
        elif self.direction == 'down_left':
            self.rect.x -= diagonal_speed * delta_time
            self.rect.y += diagonal_speed * delta_time

        self.collision_rect.center = self.rect.center


        if any(self.collision_rect.colliderect(tile.rect) for tile in self.collision_tiles):
            # Revert to the original position if there's a collision
            self.rect.topleft = original_position
            self.collision_rect.center = self.rect.center

        # Update animation based on movement
        if not self.isAttacking:
            if self.direction is not None:
                animation = 'move_' + self.direction
                if self.isRunning:
                    animation = 'run_' + self.direction
                if self.isRolling:
                    animation = 'roll_' + self.direction
                self.set_animation(animation)
            elif self.prevDirection is not None:
                if self.isRolling:
                    self.set_animation('roll_' + self.prevDirection)
                else:
                    self.do_idle()

    def do_idle(self):
        if self.prevDirection is None:
            self.set_animation('idle_up')
        elif 'right' in self.prevDirection:
            self.set_animation('idle_right')
        elif 'left' in self.prevDirection:
            self.set_animation('idle_left')
        elif self.prevDirection == 'up':
            self.set_animation('idle_up')
        else:
            self.set_animation('idle_down')

    def can_attack(self):
        if pygame.time.get_ticks() - self.last_attack_time < ATTACK_COOLDOWN:
            return False
        return not self.isAttacking and not self.isRolling and not self.isDying

    def can_roll(self):
        return pygame.time.get_ticks() - self.last_roll_time > ROLL_COOLDOWN and not self.isDying

    def is_dead(self):
        return self.isDead

    def add_kill(self):
        self.enemies_killed += 1

    def can_special_attack(self):
        return self.enemies_killed >= SPECIAL_ENEMIES_KILLED and not self.isSpecialAttacking

    def start_special_attack(self):
        self.isSpecialAttacking = True
        self.sound_manager.play_sound('vortex')
        self.vortex_move = AnimatedVortex(*self.rect.center, self.sprite_group)

    def do_special_attack(self):
        self.enemies_killed = 0
        self.do_idle()
        if self.vortex_move.is_done():
            self.isSpecialAttacking = False

    def draw_kills(self, screen):
        font = pygame.font.Font(None, 36)  # Use a default font with size 36
        kills_text = font.render(f'Kills: {self.enemies_killed}', True, (255, 255, 255))  # Render the text in white
        screen.blit(kills_text, (20, 20))  # Draw the text at the top-left corner of the screen