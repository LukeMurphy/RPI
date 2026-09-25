import hub75
import random
import time

WIDTH = 64
HEIGHT = 64

matrix = hub75.Hub75(WIDTH, HEIGHT)
INTERVAL = 0.02
brt = 0.8
matrix.start()
maxb = 180

for r in range(0, 64, 1):
    for c in range(0, 64, 1):
        # matrix.set_pixel(c, r, random.randint(0,maxb), random.randint(0,maxb), random.randint(0,maxb))
        pass
r1 = random.randint(100, 600)
r2 = random.randint(100, 600)

grid = []
for r in range(0, 64, 2):
    for c in range(0, 64, 3):
        matrix.set_pixel(c, r, random.randint(200, 255), random.randint(0, 50), random.randint(0, 100))
        #grid.append([c, r])
# for r in range(0, 64, 2):
#     for c in range(1, 64, 3):
#         matrix.set_pixel(c, r, random.randint(0, 0), random.randint(100, 250), random.randint(0, 100))
#         grid.append([c, r])
# for r in range(0, 64, 2):
#     for c in range(2, 64, 3):
#         matrix.set_pixel(c, r, random.randint(0, 0), random.randint(0, 0), random.randint(200, 250))
#         grid.append([c, r])
while True:
    for _ in range(r1):
        _r = random.randint(0, 64)
        _c = random.randint(0, 64)

        if [_c, _r] not in grid:
            matrix.set_pixel(_c, _r, random.randint(0, maxb), random.randint(0, maxb), random.randint(0, maxb))
    for _ in range(r2):
        _r = random.randint(0, 64)
        _c = random.randint(0, 64)
        if [_c, _r] not in grid:
            matrix.set_pixel(_c, _r, 0,0,0)

    if random.random() < 0.01:
        r1 = random.randint(100, 480)
        r2 = random.randint(100, 480)
        for r in range(0, 64, 1):
            for c in range(0, 64, 1):
                if r % 2 == 0 and c % 2 == 0:
                    if random.random() < .5 :matrix.set_pixel(c, r, random.randint(200, 255), random.randint(0, 50), random.randint(0, 100))
                else :
                    if random.random() < .5 : matrix.set_pixel(c, r, 0,0,0)

    time.sleep(INTERVAL)

