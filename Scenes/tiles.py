# Scenes
# tiles.py

import pyglet

from config import *
from Scenes.changes import *

# Tile Dictionary, keys are tile_id, values are tile properties

# sprite_ind
tile_properties = ['solid', 'water', 'slippery', 'pass_small', 'electricity']

# pass_small or block_small?

# 'default' properties are False for all properties
# 'default':{'sprite_ind':(0,0), 'solid':False, 'water':False, }

"""
tile_dict = {
    'floor': {'sprite_ind':(3,1), 'solid':False},
    'wall': {'sprite_ind':(3,2), 'solid':True, 'pass_small':False},
    'water': {'sprite_ind':(5,1), 'water':True},
    'icy_floor': {'sprite_ind':(1,3), 'slippery':True}
    }
"""

class Tile:
    # tile_id = 'floor'
    def __init__(self, x,y, tile_id = 'floor', level = None, place_it = True, status=None): # , blocked = False
        self.tile_id = tile_id
        self.x = x # ???
        self.y = y # ???
        
        self.level = level
        self.model = level.model
        self.game_scene = level.model.game_scene

        if place_it:
            level.tiles[x][y] = self # ???

        assign_tile_data(self)
        if status:
          self.status = status
        self.set_sprite()
        
        # Occupying Creature
        self.occupant = None
        self.spirit = None
        #self.sprite = None

        # Is there an object that works as a bridge?
        #self.bridge = None
        self.overtile = None

    def set_sprite(self):
        # Get the Entity sprite
        #spritesheet = self.game_scene.spritesheet
        image = self.status_to_sprite[self.status]
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.level.batch,
                            group = self.level.tiles_group)
        '''
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = self.game_scene.tiles_group)'''
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

    def change_status(self, new_status, save_change=False):
      old_status = self.status
      self.status = new_status
      if save_change:
        self.model.chain.append(ChangeStatus(self,old_status,new_status))

      self.update()

tile_properties_dict = {
    'floor': {'solid':False},
    'wall': {'solid':True, 'pass_small':False},
    'crack': {'solid':True, 'pass_small':True},
    'water': {'water':True},
    'icy_floor': {'slippery':True}
    }

for k,v in tile_properties_dict.items():
    for p in tile_properties:
        if p not in v:
            v[p] = False

class Extractor:
    def __init__(self, owner):
        self.owner = owner

    def enter(self, entity, dx,dy):
        # Call this function when entity lands on tile
        # Extracts the spirit from the Possessed Creature
        if entity.type == 'creature':
            entity.depossess()

    def exit(self, entity, dx,dy): #leave?
        # Call this function when entity lands on tile
        pass

class PressurePlate:
    def __init__(self, owner):
        self.owner = owner
        #self.switch = False
        #self.mapping = {False:'off', True:'on'}

    def enter(self, entity, dx,dy):
        # Call this function when entity lands on tile
        self.check_pressure()

    def exit(self, entity, dx,dy): #leave?
        # Call this function when entity lands on tile
        self.check_pressure()

    def check_pressure(self):
        occupant = self.owner.occupant
        old_status = self.owner.status
        if occupant: #is not None:
            weight = True
            if occupant.creature:
              weight = not occupant.creature['flying']

            if occupant.type == 'spirit':
              weight = False

            #self.switch = True
            #self.owner.status = 'on'
            if weight:
              new_status = 'on'
            else:
              new_status = 'off'
        else:
            #self.switch = False
            #self.owner.status = 'off'
            new_status = 'off'
        #self.owner.status = new_status
        #self.owner.status = self.mapping[self.switch]
        #self.owner.model.chain.append(ChangeStatus(self.owner,old_status,new_status))
        #self.owner.update()
        if old_status != new_status:
          self.owner.change_status(new_status, save_change=True)

class ToggleTile:
    def __init__(self, owner):
        self.owner = owner
        #self.switch = False
        self.mapping = {'on':'off', 'off':'on'}

    def enter(self, entity, dx,dy):
        # Call this function when entity lands on tile
        if (entity.type == 'creature' and entity.creature is not None):
            if (entity.creature['spirit'] == False
                and entity.creature['flying'] == False):
                #self.switch = (not self.switch)
                old_status = self.owner.status
                new_status = self.mapping[old_status]
                #self.owner.status = self.mapping[self.owner.status]
                #self.owner.status = new_status
                #self.owner.model.chain.append(ChangeStatus(self.owner,old_status,new_status))
                #self.owner.change_status(new_status, save_change=True)
                #self.owner.update()
                self.owner.change_status(new_status, save_change=True)
                print("Tile toggled:",self.owner.status)

    def exit(self, entity, dx,dy): #leave?
        pass
        
class Slippery:
    def __init__(self, owner):
        self.owner = owner

    def enter(self, entity, dx,dy):
        # Call this function when entity lands on tile
        # Slippery
        if entity.type == 'creature' and not entity.creature['flying'] and not entity.creature['icewalk']:
          entity.move_check(dx,dy)

    def exit(self, entity, dx,dy): #leave?
        # Call this function when entity lands on tile
        pass

def assign_tile_data(tile):
    # ent is the input Entity
    tile_id = tile.tile_id

    # Assign tile type
    #tile.type = entity_dict[ent_id]['type']
    # Assign tile properties
    tile.properties = tile_dict[tile_id]['properties']
    # Assign lander component
    if tile_dict[tile_id]['lander'] is not None:
        tile.lander = tile_dict[tile_id]['lander'](tile)
    else:
        tile.lander = None
    # Assign initial status
    tile.status = tile_dict[tile_id]['status']
    # Assign status to sprite mapping
    spritesheet = tile.game_scene.spritesheet
    status_to_sprite_ind = tile_dict[tile_id]['status_to_sprite_ind']
    tile.status_to_sprite = {k:spritesheet[v]
                            for k,v in status_to_sprite_ind.items()}

tile_dict = {
    'floor': {'properties':tile_properties_dict['floor'],
               'status':'default',
               'status_to_sprite_ind':{'default':(3,1)},
               'lander':None},
    'wall': {'properties':tile_properties_dict['wall'],
               'status':'default',
               'status_to_sprite_ind':{'default':(3,2)},
               'lander':None},
    'crack': {'properties':tile_properties_dict['crack'],
               'status':'horizontal',
               'status_to_sprite_ind':{'default':(4,6), 'horizontal':(4,6), 'vertical':(3,6)},
               'lander':None},
    'water': {'properties':tile_properties_dict['water'],
               'status':'default',
               'status_to_sprite_ind':{'default':(5,1)},
               'lander':None},
    'icy_floor': {'properties':tile_properties_dict['floor'],
               'status':'default',
               'status_to_sprite_ind':{'default':(1,3)},
               'lander':Slippery},
    'pressure_plate': {'properties':tile_properties_dict['floor'],
               'status':'off',
               'status_to_sprite_ind':{'off':(2,3), 'on':(2,4)},
               'lander':PressurePlate},
    'toggle_tile': {'properties':tile_properties_dict['floor'],
               'status':'off',
               'status_to_sprite_ind':{'off':(2,6), 'on':(2,5)},
               'lander':ToggleTile},
    'canvas': {'properties':tile_properties_dict['floor'],
               'status':'white',
               'status_to_sprite_ind':{'white':(1,7), 'blue':(2,7),
                                       'green':(3,7), 'red':(4,7),
                                       'yellow':(2,8), 'purple':(3,8),
                                       'cyan':(4,8)},
               'lander':None},
    'extractor': {'properties':tile_properties_dict['floor'],
               'status':'default',
               'status_to_sprite_ind':{'default':(1,9)},
               'lander':Extractor},
}
