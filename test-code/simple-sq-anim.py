import pygame
import sys
import colorsys

# --- config ---
WIDTH, HEIGHT = 800, 400
SQUARE_SIZE = 300
SPEED = 0  # pixels per second
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 1)
clock = pygame.time.Clock()

x = -SQUARE_SIZE + 100
y = (HEIGHT - SQUARE_SIZE) // 2
hue = 0.0

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update position
    x += SPEED * dt
    if x > WIDTH:
        x = -SQUARE_SIZE

    # update color (HSV → RGB)
    hue = (hue + dt * 0.3) % 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    color = (int(r * 255), int(g * 255), int(b * 255))

    # draw
    screen.fill((0, 0, 0, 10))
    pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE), 10,20)
    pygame.display.flip()

pygame.quit()