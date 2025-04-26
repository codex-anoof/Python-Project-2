
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Dummy player object for simulation
player = pygame.Rect(400, 500, 50, 50)
player_speed = 5
lives = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # ✅ Issue #1: Keep player on screen
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.display.flip()

    # Simulate player losing a life when pressing down arrow (for testing Issue #2)
    if keys[pygame.K_DOWN]:
        lives -= 1
        pygame.time.delay(200)
        print(f"Lives: {lives}")

    # ✅ Issue #2: End game when out of lives
    if lives <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()

    clock.tick(60)
