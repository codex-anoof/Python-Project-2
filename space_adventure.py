
import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Adventure")
clock = pygame.time.Clock()

# Dummy values for player/enemy
player = pygame.Rect(400, 500, 50, 50)
player_speed = 5
lives = 3
score = 0

# Power-up logic
power_up_active = False
power_up_timer = 0

bullets = []
enemies = [pygame.Rect(random.randint(0, WIDTH-50), 0, 50, 50) for _ in range(3)]

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
    if keys[pygame.K_SPACE]:
        bullets.append(pygame.Rect(player.x + 20, player.y, 5, 10))
    if keys[pygame.K_DOWN]:
        lives -= 1
        pygame.time.delay(300)

    # Keep player on screen (Issue #1 - previously fixed)
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH

    # Power-up collection logic (Issue #3)
    if not power_up_active and random.random() < 0.01:
        power_up = pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 30, 30)
        power_up_active = True
        power_up_timer = pygame.time.get_ticks()
    else:
        power_up = None

    # Game logic
    screen.fill((0, 0, 30))

    # Draw player and bullets
    pygame.draw.rect(screen, (0, 255, 0), player)
    for bullet in bullets[:]:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)
        pygame.draw.rect(screen, (255, 255, 0), bullet)

    # Enemies + destruction logic (Issue #4)
    for enemy in enemies[:]:
        enemy.y += 1
        pygame.draw.rect(screen, (255, 0, 0), enemy)
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    # Power-up effect shown
    if power_up_active:
        if pygame.time.get_ticks() - power_up_timer < 5000:
            pygame.draw.rect(screen, (0, 255, 255), power_up)
        else:
            power_up_active = False

    # Game over logic (Issue #2)
    if lives <= 0:
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(60)
