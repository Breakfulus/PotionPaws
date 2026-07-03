import random
import consts as c

def get_possible_spawn_points():
    points = []

    for x in range(0, c.SCREEN_WIDTH):
        points.append((x, 0)) # Top
        points.append((x, c.SCREEN_HEIGHT)) # Bottom

    for y in range(0, c.SCREEN_HEIGHT):
        points.append((0, y)) # Left
        points.append((c.SCREEN_WIDTH, y)) # Rigth
    
    return points # List containing all possible spawn points

def get_next_spawn_point():
    next_spawn = random.choice(get_possible_spawn_points())
    return next_spawn
