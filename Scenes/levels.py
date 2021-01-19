# Scenes
# levels.py

import pyglet

from config import *

#from Scenes.model import Level, Tile, Entity

class Level:
    def __init__(self, model = None, key = None, name='blank'):
        self.model = model
        self.name = name # Level's name for displaying?
        self.key = key # Used to access this level from level dict
        if self.key is not None:
            self.model.levels[self.key] = self
        """self.tiles = [[Tile('floor', self, x,y) for y in range(TILES_VER)]
                      for x in range(TILES_HOR)]"""
        self.tiles = [[None
                       for y in range(TILES_VER)]
                          for x in range(TILES_HOR)]
        self.entities = []
        self.player = None

        self.mechanisms = []

        # Define My Batch
        self.batch = pyglet.graphics.Batch()
        # Define My Groups (Group for tiles, group for creatures)
        self.tiles_group = pyglet.graphics.OrderedGroup(0)
        self.over_tiles_group = pyglet.graphics.OrderedGroup(1)
        self.ent_group = pyglet.graphics.OrderedGroup(2)
        self.spirit_group = pyglet.graphics.OrderedGroup(3)

'''
def create_test_levels(model):

    # Level 1
    level1 = Level(model = model, name = 'Test Level', key = (0,0))

    for x in range(TILES_HOR): #(1, TILES_HOR-1)
        for y in range(TILES_VER): #(1, TILES_VER-1)
            Tile(x,y, tile_id = 'floor',
            level = level1, place_it = True)
        
    for x in range(TILES_HOR):
        Tile(x,0, tile_id = 'wall',
            level = level1, place_it = True)
        Tile(x,TILES_VER - 1, tile_id = 'wall',
            level = level1, place_it = True)
            
    for y in range(TILES_VER):
        Tile(0,y, tile_id = 'wall',
            level = level1, place_it = True)
        Tile(TILES_HOR - 1,y, tile_id = 'wall',
            level = level1, place_it = True)

    Tile(0,TILES_VER//2, tile_id = 'floor',
            level = level1, place_it = True)

    Tile(TILES_HOR,TILES_VER//2, tile_id = 'floor',
            level = level1, place_it = True)

    Tile(TILES_HOR//2,0, tile_id = 'floor',
            level = level1, place_it = True)

    Tile(TILES_HOR//2,TILES_VER, tile_id = 'floor',
            level = level1, place_it = True)

    Entity(15,15, ent_id = 'player', level = level1)

    level1.player = Entity(10,10, ent_id = 'spirit', level = level1)

    # Level 2
    level2 = Level(model = model, name = 'Test Level', key = (0,-1))
    
    for x in range(TILES_HOR): #(1, TILES_HOR-1)
        for y in range(TILES_VER): #(1, TILES_VER-1)
            Tile(x,y, tile_id = 'water',
            level = level2, place_it = True)
        
    for x in range(TILES_HOR):
        Tile(x,0, tile_id = 'wall',
            level = level2, place_it = True)
        Tile(x,TILES_VER - 1, tile_id = 'wall',
            level = level2, place_it = True)
            
    for y in range(TILES_VER):
        Tile(0,y, tile_id = 'wall',
            level = level2, place_it = True)
        Tile(TILES_HOR - 1,y, tile_id = 'wall',
            level = level2, place_it = True)

    Tile(TILES_HOR//2,TILES_VER, tile_id = 'floor',
            level = level2, place_it = True)

    for x in range(TILES_HOR//2 - 2, TILES_HOR//2 + 3):
        for y in range(TILES_VER-6, TILES_VER-1):
            Tile(x,y, tile_id = 'floor',
            level = level2, place_it = True)
            if ((x == TILES_HOR//2 - 2) or (TILES_HOR//2 + 3)
                (y == TILES_VER-6)):
                Entity(x,y, ent_id = 'boulder', level = level2)
                print("Boulder placed at {},{}".format(x,y))

    levels = {(5,5):level1, (5,4):level2}

    return(levels)
'''
    
