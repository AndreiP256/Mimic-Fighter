import pygame

def fade_out(screen, width, height, tile_map, all_sprites, enemyList, player):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.fill((0, 0, 0))
        tile_map.render(screen)
        all_sprites.draw(screen)
        for enemy in enemyList:
            if enemy.health_bar is not None:
                enemy.health_bar.draw(screen)
        player.healthBar.draw(screen)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_in(screen, width, height, tile_map, all_sprites, enemyList, player):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(255, 0, -5):
        fade.set_alpha(alpha)
        screen.fill((0, 0, 0))
        tile_map.render(screen)
        all_sprites.draw(screen)
        for enemy in enemyList:
            if enemy.health_bar is not None:
                enemy.health_bar.draw(screen)
        player.healthBar.draw(screen)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)