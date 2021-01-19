# Scenes
# game.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

from config import *

from Scenes.entities import *
from Scenes.tiles import *
#from Scenes.creatures import *
#from Scenes.objects import *

#from Scenes.levels import create_test_levels
from Scenes.test_levels import create_test_levels

#from scene_manager import SceneManager

pyglet.resource.path = ['Images']
pyglet.resource.reindex()

#TILE_SIZE = 32
#TILES_HOR = 25
#TILES_VER = 20

class Model:
    def __init__(self, game_scene):
        # Game Scene
        self.game_scene = game_scene

        """
        self.tiles = [[Tile() for y in range(TILES_VER)]
                      for x in range(TILES_HOR)]
        self.entities = []
        #self.creatures = []
        """

        ## Levels exist in a data structure, list? dictionary? list of lists?
        self.levels = {} #[]
        self.current_level = None

        # Test Level Content
        #test_level = self.test_level()
        #self.levels[(5,5)] = test_level
        #self.current_level = test_level
        create_test_levels(self)
        print(self.levels)
        self.current_level = self.levels[(0,0)]
        self.update_now = True

        ### Model changes
        self.changes = []

        #self.player = Entity('player', self, TILES_HOR//2, TILES_VER - 1)

        # Update the Graphics because the game state has changed visibly
        #self.update_now = False

    def undo_latest(self):
        # Undo the latest chain of changes
        changes = self.changes
        if changes:
            chain = changes.pop()

            if chain:
                print("Undo move!")
                print(type(chain))
                print(chain)
                for change in reversed(chain):
                    change.undo()



    '''
    def generate_maze(self):
        maze = maze_generator()
        for x in range(TILES_HOR):
            for y in range(TILES_VER):
                self.tiles[x][y].blocked = maze[x][y]
        self.update_now = True

    def test_level(self):
        # Create a test level

        test_level = Level(model = self, name = 'Test Level', key = (0,0))

        """
        test_level.tiles = [[Tile('floor', test_level, x,y)
                             for y in range(TILES_VER)]
                              for x in range(TILES_HOR)]"""
        test_level.entities = []

        for x in range(TILES_HOR): #(1, TILES_HOR-1)
            for y in range(TILES_VER): #(1, TILES_VER-1)
                Tile(x,y, tile_id = 'floor',
                     level = test_level, place_it = True)
        
        for x in range(TILES_HOR):
            Tile(x,0, tile_id = 'wall',
                 level = test_level, place_it = True)
            Tile(x,TILES_VER - 1, tile_id = 'wall',
                 level = test_level, place_it = True)
            #test_level.tiles[x][0] = Tile('wall', test_level, x,0)
            #test_level.tiles[x][TILES_VER - 1] = Tile('wall', test_level, x,TILES_VER - 1)

        for y in range(TILES_VER):
            Tile(0,y, tile_id = 'wall',
                 level = test_level, place_it = True)
            Tile(TILES_HOR - 1,y, tile_id = 'wall',
                 level = test_level, place_it = True)
            #test_level.tiles[0][y] = Tile('wall', test_level, 0,y)
            #test_level.tiles[TILES_HOR - 1][y] = Tile('wall', test_level, TILES_HOR - 1,y)

        #test_level.tiles[5][5] = Tile('wall', test_level, 5,5)
        Tile(5,5, tile_id = 'wall',
                 level = test_level, place_it = True)

        for x in range(12,17):
            for y in range(12,17):
                #test_level.tiles[x][y] = Tile('water', test_level, x,y)
                Tile(x,y, tile_id = 'water',
                 level = test_level, place_it = True)

        #bridge = Entity(16,15, ent_id = 'boulder', level = test_level)
        #bridge.sprite.group = self.game_scene.over_tiles_group

        """
        image = self.game_scene.spritesheet[(3,5)]
        sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = self.game_scene.over_tiles_group)
        sprite.x = 128
        sprite.y = 128"""

        for x in range(15,18):
            for y in range(5,8):
                Tile(x,y, tile_id = 'toggle_tile',
                 level = test_level, place_it = True)

        for x in range(11,14):
            for y in range(5,8):
                Tile(x,y, tile_id = 'canvas',
                 level = test_level, place_it = True)
            
        Tile(9,9, tile_id = 'pressure_plate',
                 level = test_level, place_it = True)

        Tile(2,2, tile_id = 'extractor',
                 level = test_level, place_it = True)

        Entity(4,4, ent_id = 'player', level = test_level)

        # Player starting coords
        sx, sy = TILES_HOR//2, TILES_VER - 2
        #test_level.player = Entity(sx,sy, ent_id = 'player', level = test_level)
        test_level.player = Entity(sx,sy, ent_id = 'spirit', level = test_level)
        
        #Entity('boulder', test_level, 5,10)
        #Entity('boulder', test_level, 7,10)

        Entity(5,10, ent_id = 'boulder', level = test_level)
        Entity(7,10, ent_id = 'boulder', level = test_level)

        rbrush = Entity(5,8, ent_id = 'paint_brush', level = test_level)
        gbrush = Entity(6,8, ent_id = 'paint_brush', level = test_level)
        bbrush = Entity(7,8, ent_id = 'paint_brush', level = test_level)

        #gbrush.lander.color = 'green'
        #bbrush.lander.color = 'blue'
        gbrush.status = 'green'
        bbrush.status = 'blue'

        return(test_level)
        '''
            
'''
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
'''        
        
'''
class Tile:
    # tile_id = 'floor'
    def __init__(self, x,y, tile_id = 'floor', level = None, place_it = True): # , blocked = False
        self.tile_id = tile_id
        self.x = x # ???
        self.y = y # ???
        
        self.level = level
        self.model = level.model
        self.game_scene = level.model.game_scene

        if place_it:
            level.tiles[x][y] = self # ???

        assign_tile_data(self)
        self.set_sprite()

        """
        # Tile properties
        self.tile_properties = None
        # Status
        self.status = None
        # Enter component (function for entering this tile)
        self.enter = None
        # Exit component (function for exiting this tile)
        self.exit = None

        #self.lander = None # Lander component
        
        # Load tile properties based on tile_id

        self.change(tile_id)

        self.sprite.x = TILE_SIZE * x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (y + 1) # Reverse!
        """
        
        # Occupying Creature
        self.occupant = None
        self.spirit = None
        #self.sprite = None

        # Is there an object that works as a bridge?
        self.bridge = None

    def set_sprite(self):
        # Get the Entity sprite
        #spritesheet = self.game_scene.spritesheet
        image = self.status_to_sprite[self.status]
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = self.game_scene.tiles_group)
        self.sprite.x = TILE_SIZE * self.x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (self.y + 1) # Reverse!

    def update(self):
        self.sprite.image = self.status_to_sprite[self.status]

    def change(self, tile_id):
        ### Change tile to another type
        # Get the tile data from the tile dictionary
        tile_data = tile_dict[tile_id]

        # Get the tile sprite
        #spritesheet = self.game_scene.spritesheet
        spritesheet = self.game_scene.spritesheet
        image = spritesheet[tile_data['sprite_ind']]
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = self.game_scene.tiles_group)
        
        # Set the Tile Properties
        for p in tile_properties:
            # setattr(..) <== ???
            p_value = (tile_data[p] or False)
            setattr(self, p, p_value)
            #self.p = (tile_data[p] or False)
'''

'''
class Entity:
    def __init__(self, x,y, ent_id = 'boulder', level = None):
        self.ent_id = ent_id # Creature ID

        self.level = level
        self.model = level.model
        self.game_scene = level.model.game_scene
        
        self.x = x
        self.y = y
        #self.direction = (0,-1) # 'up', 'down', 'left', 'right'
        #self.delay = 0

        assign_entity_data(self)
        self.set_sprite()
        #self.update()

        # Controlling spirit entity of the creature
        self.controller = None

        """
        # Entity type
        self.type = 'object' # ['creature', 'object']
        # Status
        self.status = None #{''}
        # Interactor Component
        self.interactor = None

        if (ent_id in creature_dict):
            self.type = 'creature'
            #self.creature = True
            # Get the tile data from the tile dictionary
            #cre_data = creature_dict[ent_id]
            ent_data = creature_dict[ent_id]
            ent_properties = creature_properties
        elif (ent_id in object_dict):
            self.type = 'object'
            #self.object = True
            #obj_data = obj_dict[ent_id]
            ent_data = object_dict[ent_id]
            ent_properties = object_properties

        # Set the Entity Properties
        for p in ent_properties:
            # setattr(..) <== ???
            setattr(self, p, (ent_data[p] or False))
            #self.p = (tile_data[p] or False)
        """

        # Add Entity as Occupant
        level.tiles[x][y].occupant = self
        level.entities.append(self)

    def set_sprite(self):
        # Get the Entity sprite
        #spritesheet = self.game_scene.spritesheet
        image = self.status_to_sprite[self.status]

        #group_dict = {''}
        if self.type == 'spirit':
            group = self.game_scene.spirit_group
        else:
            group = self.game_scene.ent_group
        
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = group)
        self.sprite.x = TILE_SIZE * self.x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (self.y + 1) # Reverse!

    def update(self):
        self.sprite.image = self.status_to_sprite[self.status]
        # Update the sprite coordinates
        self.sprite.x = TILE_SIZE * self.x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (self.y + 1) # Reverse!

    def move(self, dx,dy):
        tiles = self.level.tiles #self.model.tiles

        ### Entity leaves the tile, triggering tile function
                
        # Only call if checks have been made!
        x = self.x
        y = self.y
        old_tile = tiles[x][y]
        nx = x + dx
        ny = y + dy
        new_tile = tiles[nx][ny]
        #tiles[x][y].occupant = None
        self.x = nx
        self.y = ny
        #tiles[nx][ny].occupant = self
        self.model.update_now = True # <--- ???
        if self.type == 'spirit':
            tiles[x][y].spirit = None
            tiles[nx][ny].spirit = self
        else:
            tiles[x][y].occupant = None
            tiles[nx][ny].occupant = self

        ### Entity lands on a tile, triggering functions of the Entity
        if self.lander is not None:
            self.lander.landing(dx,dy)
        ### Entity exits a tile, triggering functions of the Tile
        if old_tile.lander is not None:
            old_tile.lander.exit(self, dx,dy)
        ### Entity lands on a tile, triggering functions of the Tile
        if new_tile.lander is not None:
            new_tile.lander.enter(self, dx,dy)

    def move_action(self, dx,dy):
        # Entity tries to move and possibly acts
        # Takes into account environment

        nx = self.x + dx
        ny = self.y + dy

        # Check if Out of Bounds
        inside_bounds = (0 <= nx < TILES_HOR and 0 <= ny < TILES_VER)

        if inside_bounds:
            new_tile = self.level.tiles[nx][ny]
            passes = self.check_passing(new_tile)
            
            occupant = new_tile.occupant
            if occupant is not None:
                # Only non-spirits interact with objects?
                if self.type != 'spirit':
                    if occupant.interactor is not None:
                        occupant.interactor.interaction(self, dx,dy)
                else:
                    self.move(dx,dy)
                    if occupant.type == 'creature':
                        self.possess(occupant)
            elif passes:
                self.move(dx,dy)
        else:
            # Transition to next level if possible
            self.transition(dx,dy)
            
        
    def transition(self, dx,dy):
        # Transition to new level
        # Only player controlled creatures can transition?
        if self == self.level.player: #self.controller not None:
            # Current level key
            ku,kv = self.level.key
            # Next level key
            nu,nv = ku+dx, kv+dy

            # Check if there is another level in that direction
            if (nu,nv) in self.model.levels:
                print("Old level: {}".format(self.level.key))
                # Transition to the new level
                new_level = self.model.levels[(nu,nv)]
                self.level = new_level
                self.level.player = self

                nx = self.x + dx
                ny = self.y + dy
                
                nx %= TILES_HOR
                ny %= TILES_VER
                self.x = nx
                self.y = ny
                #self.level.tiles[nx][ny].occupant = self
                self.move(0,0)
                print("New level: {}".format(self.level.key))
                print(len(self.level.entities))

    def move_action_old(self, dx,dy):
        # Entity tries to move and possibly acts
        # Takes into account environment

        nx = self.x + dx
        ny = self.y + dy

        # Check if Out of Bounds
        if (0 <= nx < TILES_HOR and 0 <= ny < TILES_VER):
            inside_bounds = True
        else:
            inside_bounds = False

        free_move = False
        # Check if new tile passable
        if inside_bounds:
            #new_tile = self.model.tiles[nx][ny]
            new_tile = self.level.tiles[nx][ny]
            passes = self.check_passing(new_tile)
            if passes:
                # Check if there are obstacle entities
                if new_tile.occupant is None:
                    free_move = True
                elif new_tile.occupant is not None and self.type == 'spirit':
                    free_move = True
                else:
                    # Is the Entity occupying the Tile pushable?
                    push_move = self.pushing(dx,dy)
                    free_move = push_move

        if free_move:
            self.move(dx,dy)
            
        
        pass

    def check_passing(self, tile):
        # Check if the creature can walk to the tile
        # Depends on creature and tile properties
        #cre = self.creature

        """
        solid_spirit = (cre.spirit
                        and not tile.electricity and tile.solid)
        water_swim = (cre.swims and tile.water)"""
        
        if (tile.properties['solid'] == False):
            passes = True           
        else:
            passes = (self.creature['spirit']
                      and not tile.properties['electricity']) #cre.spirit

        if (tile.properties['water'] and tile.bridge is None):
            passes = (self.creature['swims'] or self.creature['flying'])

        #print(passes)
        return(passes)
        
    def possess(self, cre_ent):
        # Player in Spirit Form possesses the Creature Entity
        cre_ent.controller = self # Creature is controlled by spirit
        self.level.player = cre_ent # Player is the Creature
        tile = self.level.tiles[self.x][self.y] # Spirit tile
        tile.spirit = None # Spirit is no longer on the tile
        self.sprite.visible = False # Spirit is not visible
        #self.occupant

    def depossess(self):
        # Spirit leaves the Controlled Creature Entity
        spirit = self.controller # Reference to spirit
        self.controller = None # Creature is no longer possessed
        self.level.player = spirit # Player is the Creature
        tile = self.level.tiles[self.x][self.y] # Tile
        tile.spirit = spirit # Spirit enters the tile
        spirit.sprite.visible = True
        spirit.x = self.x
        spirit.y = self.y

    def move_level(self):
        # Move between levels
        pass

    def pushing(self, dx, dy):
        tiles = self.level.tiles
        # New coordinates of the Pushing Creature,
        # old coordinates of the pushable Entity
        nx = self.x + dx
        ny = self.y + dy
        new_tile = tiles[nx][ny]

        push_move = False
        
        # Check if the pushable Entity
        #pushable = new_tile.occupant
        if (new_tile.occupant.pushable):            
            # Potential Coordinates for the pushable Entity
            nnx = nx + dx
            nny = ny + dy
            # Check if inside bounds for the pushable Entity
            if (0 <= nnx < TILES_HOR and 0 <= nny < TILES_VER):
                # Check if the new tile is solid
                if (tiles[nnx][nny].solid == False):
                    # Check if the Tile is not occupied
                    if (tiles[nnx][nny].occupant is None):
                        push_move = True

        """
        push_move = (new_tile.occupant.pushable                  
                        and 0 <= nnx < TILES_HOR
                        and 0 <= nny < TILES_VER
                        and not model.tiles[nnx][nny].blocked
                        and model.tiles[nnx][nny].occupant == None
                        and self.cre.strong)
        """

        if push_move:
            new_tile.occupant.move(dx,dy)

        return(push_move)

    def move_push(self, dx,dy): # <<<===!!!!!
        # Entity moves and possibly pushes a boulder
        model = self.model
        # Move Entity
        # Limit to TILES_HOR, TILES_VER
        nx = max(0, min(self.x + dx, TILES_HOR - 1))
        ny = max(0, min(self.y + dy, TILES_VER - 1))
        # New coordinates for pushed boulder
        nnx = nx + dx
        nny = ny + dy

        # Is the move a free move (move to empty space)
        # or a boulder push (move to boulder, boulder to empty)
        new_tile = model.tiles[nx][ny]
        free_move = not new_tile.blocked and new_tile.occupant == None
        if new_tile.occupant != None:
            boulder_push = (new_tile.occupant.ent_id == 'boulder'                  
                            and 0 <= nnx < TILES_HOR
                            and 0 <= nny < TILES_VER
                            and not model.tiles[nnx][nny].blocked
                            and model.tiles[nnx][nny].occupant == None)
        else:
            boulder_push = False

        boulder = None
        if boulder_push:
            boulder = new_tile.occupant
            boulder.move(dx,dy)

        if free_move or boulder_push:
            self.move(dx,dy)
            #level.moves.append(("Move", dx, dy, boulder))

    """
    def change_direction(self, direction):
        self.direction = direction
        if self.vision != None:
            self.vision.update_fov()

        self.model.update_now = True
    """

    def destroy(self):
        # Remove creature from the list of creatures
        self.level.entities.remove(self)
        # Creature no longer occupies its tile
        self.level.tiles[self.x][self.y].occupant = None
        # Creature drops all items in its inventory
        #self.model.tiles[self.x][self.y].items += self.inventory
'''

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

    print("West Passage")
    print(0,TILES_VER//2)
    Tile(0,TILES_VER//2, tile_id = 'floor',
            level = level1, place_it = True)

    print("East Passage")
    print(TILES_HOR - 1,TILES_VER//2)
    Tile(TILES_HOR - 1,TILES_VER//2, tile_id = 'floor',
            level = level1, place_it = True)

    print("North Passage")
    print(TILES_HOR//2,0)
    Tile(TILES_HOR//2,0, tile_id = 'floor',
            level = level1, place_it = True)

    print("South Passage")
    print(TILES_HOR//2,TILES_VER - 1)
    Tile(TILES_HOR//2,TILES_VER - 1, tile_id = 'floor',
            level = level1, place_it = True)

    Entity(15,15, ent_id = 'player', level = level1)

    level1.player = Entity(10,10, ent_id = 'spirit', level = level1)

    # Level 2
    level2 = Level(model = model, name = 'Test Level 2', key = (0,-1))
    
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

    Tile(TILES_HOR//2,TILES_VER - 1, tile_id = 'floor',
            level = level2, place_it = True)

    for x in range(TILES_HOR//2 - 2, TILES_HOR//2 + 3):
        for y in range(TILES_VER-6, TILES_VER-1):
            Tile(x,y, tile_id = 'floor',
            level = level2, place_it = True)
            if ((x == TILES_HOR//2 - 2) or (x == TILES_HOR//2 + 2)
                or (y == TILES_VER-6)):
                Entity(x,y, ent_id = 'boulder', level = level2)
                print("Boulder placed at {},{}".format(x,y))

    #levels = {(5,5):level1, (5,4):level2}

    #return(levels)
'''

"""
class Creature:
    # Creature component for Creature Entities
    # Mostly holds Creature properties
    # Ue this or use add properties directly to Entity?
    def __init__(self, entity, cre_id):
        pass"""

