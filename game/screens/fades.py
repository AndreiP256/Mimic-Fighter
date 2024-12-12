import pygame

def fade_out(screen, width, height, tile_map, all_sprites, enemyList, player):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    screen.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.fill((0, 0, 0))
        all_sprites.draw(player.rect.center)
        player.healthBar.draw(screen)
        player.abilityBar.draw(screen)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_in(screen, width, height, tile_map, all_sprites, enemyList, player):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    screen.fill((0, 0, 0))
    for alpha in range(255, 0, -5):
        fade.set_alpha(alpha)
        screen.fill((0, 0, 0))
        all_sprites.draw(player.rect.center)
        player.healthBar.draw(screen)
        player.abilityBar.draw(screen)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)