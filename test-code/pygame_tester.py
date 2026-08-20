# Source - https://stackoverflow.com/a/64630102
# Posted by Rabbid76, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-19, License - CC BY-SA 4.0

import pygame as pg


def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def draw_circle_alpha(surface, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pg.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


# pg.init()
window = pg.display.set_mode((250, 250))
clock = pg.time.Clock()

background = pg.Surface(window.get_size())
ts, w, h, c1, c2 = 50, *window.get_size(), (160, 160, 160), (192, 192, 192)
tiles = [((x * ts, y * ts, ts, ts), c1 if (x + y) % 2 == 0 else c2) for x in range((w + ts - 1) // ts) for y in range((h + ts - 1) // ts)]
for rect, color in tiles:
    pg.draw.rect(background, color, rect)

run = True
while run:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    window.blit(background, (0, 0))

    draw_rect_alpha(window, (0, 0, 255, 127), (55, 90, 140, 140))
    draw_circle_alpha(window, (255, 0, 0, 127), (150, 100), 80)
    draw_polygon_alpha(window, (255, 255, 0, 127), [(100, 10), (100 + 0.8660 * 90, 145), (100 - 0.8660 * 90, 145)])

    pg.display.flip()

pg.quit()
exit()
