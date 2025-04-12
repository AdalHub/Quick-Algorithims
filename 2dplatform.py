import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 2D Platformer")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Define some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

class Platform(pygame.sprite.Sprite):
    """Static platform on which the player can stand."""
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    """Player character that can move left/right and jump."""
    def __init__(self, x, y):
        super().__init__()
        # Create a simple red rectangle as the player
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement attributes
        self.speed = 5         # Horizontal speed
        self.jump_speed = 15   # Jump impulse
        self.vel_y = 0         # Current vertical velocity
        self.gravity = 0.5     # How quickly the player falls

    def update(self, platforms):
        """Update the player's position based on user input and handle collisions."""
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 10:  # Terminal velocity
            self.vel_y = 10
        self.rect.y += self.vel_y

        # Check collision with platforms (vertical only)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # We collided while moving downward
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0

        # Jump logic
        if keys[pygame.K_SPACE]:
            # Check if the player is on a platform before allowing jump
            self.rect.y += 1  # Move player down 1px to detect if standing on a platform
            on_platform = any(self.rect.colliderect(p.rect) for p in platforms)
            self.rect.y -= 1  # Move back up
            if on_platform:
                self.vel_y = -self.jump_speed

def main():
    # Create a group/list of platforms
    platforms = []

    # Ground platform (stretching across the bottom)
    ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
    platforms.append(ground)

    # A few floating platforms
    platforms.append(Platform(200, 450, 100, 20))
    platforms.append(Platform(400, 350, 100, 20))
    platforms.append(Platform(600, 250, 100, 20))

    # Create a player
    player = Player(50, 50)

    # Main game loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the player
        player.update(platforms)

        # Clear screen
        screen.fill(WHITE)

        # Draw platforms
        for platform in platforms:
            screen.blit(platform.image, platform.rect)

        # Draw player
        screen.blit(player.image, player.rect)

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
