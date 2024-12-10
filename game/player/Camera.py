import pygame


class Camera:
    def __init__(self, width, height, screen_width, screen_height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # The camera's view of the map
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, target):
        """Apply the camera offset to a target."""
        return target.rect.move(-self.camera_rect.topleft)

    def update(self, player):
        """Update the camera to follow the player."""
        # Define the edges where the camera starts moving
        left_edge = self.camera_rect.left + self.screen_width // 4
        right_edge = self.camera_rect.left + 3 * self.screen_width // 4
        top_edge = self.camera_rect.top + self.screen_height // 4
        bottom_edge = self.camera_rect.top + 3 * self.screen_height // 4

        # Update the camera position only if the player is near the edges
        if player.rect.centerx < left_edge:
            self.camera_rect.left = max(player.rect.centerx - self.screen_width // 4, 0)
        if player.rect.centerx > right_edge:
            self.camera_rect.left = min(player.rect.centerx - 3 * self.screen_width // 4, self.camera_rect.width - self.screen_width)
        if player.rect.centery < top_edge:
            self.camera_rect.top = max(player.rect.centery - self.screen_height // 4, 0)
        if player.rect.centery > bottom_edge:
            self.camera_rect.top = min(player.rect.centery - 3 * self.screen_height // 4, self.camera_rect.height - self.screen_height)

        # Clamp the camera to not go outside the level boundaries
        self.camera_rect.left = max(0, min(self.camera_rect.left, self.camera_rect.width - self.screen_width))
        self.camera_rect.top = max(0, min(self.camera_rect.top, self.camera_rect.height - self.screen_height))
