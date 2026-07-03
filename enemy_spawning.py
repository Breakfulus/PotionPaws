import random
import consts as c

def get_possible_spawn_points():
    points = []

    for x in range(0, c.SCREEN_WIDTH):
        points.append((x, 0))
        points.append((x, c.SCREEN_HEIGHT))

    for y in range(0, c.SCREEN_HEIGHT):
        points.append((0, y))
        points.append((c.SCREEN_WIDTH, y))
    
    return points

def get_next_spawn_point():
    next_spawn = random.choice(get_possible_spawn_points())
    return next_spawn
