# Scenes
# entities.py

import pyglet

from config import *

from Scenes.creatures import creature_dict
from Scenes.objects import *

from Scenes.changes import *

# Use this???

# Entity Dictionary, keys are tile_id, values are tile properties

# sprite_dict for each entity?

# pass_small or block_small?

# 'default' properties are False for all properties
# 'default':{'solid':False, 'water':False, }

"""
entity_dict = {
    'player': {'creature':True, 'small':False},
    'human': {'strong':False, 'small':False},
    'spirit': {'spirit':True},
    'fishman': {'swims':True},
    'bird': {'flying':True},
    'claw beast': {'icewalk':True},
    'beast': {'strong':True}
    }
"""

class Entity:
    def __init__(self, x,y, ent_id = 'boulder', level = None, status=None):
        self.ent_id = ent_id # Creature ID

        self.level = level
        self.model = level.model
        self.game_scene = level.model.game_scene
        
        self.x = x
        self.y = y
        #self.direction = (0,-1) # 'up', 'down', 'left', 'right'
        #self.delay = 0

        assign_entity_data(self)
        if status:
          self.status = status
        self.set_sprite()
        #self.update()

        # Controlling spirit entity of the creature
        self.controller = None

        # Entity layer
        #self.layer = 'entity', 'overtile', 'spirit'

        # Add Entity as Occupant
        if self.layer == 'entity':
          level.tiles[x][y].occupant = self
        elif self.layer == 'overtile':
          level.tiles[x][y].overtile = self
        elif self.layer == 'spirit':
          level.tiles[x][y].spirit = self
        level.entities.append(self)

    def set_sprite(self):
        # Get the Entity sprite
        #spritesheet = self.game_scene.spritesheet
        image = self.status_to_sprite[self.status]

        #group_dict = {''}
        if self.layer == 'entity':
          group = self.level.ent_group
        elif self.layer == 'overtile':
          group = self.level.over_tiles_group
        elif self.layer == 'spirit':
          group = self.level.spirit_group
        
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.level.batch,
                            group = group)

        '''
        self.sprite = pyglet.sprite.Sprite(image,
                            batch = self.game_scene.my_batch,
                            group = group)'''
        self.sprite.x = TILE_SIZE * self.x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (self.y + 1) # Reverse!

    def update(self):
        self.sprite.image = self.status_to_sprite[self.status]
        # Update the sprite coordinates
        self.sprite.x = TILE_SIZE * self.x
        self.sprite.y = SCREEN_HEIGHT - TILE_SIZE * (self.y + 1) # Reverse!

    def change_status(self, new_status, save_change=False):
      old_status = self.status
      self.status = new_status
      if save_change:
        self.model.chain.append(ChangeStatus(self,old_status,new_status))

      self.update()

    def move(self, dx,dy, trigger = True):
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

        if self.layer == 'entity':
          tiles[x][y].occupant = None
          tiles[nx][ny].occupant = self
        elif self.layer == 'overtile':
          tiles[x][y].overtile = None
          tiles[nx][ny].overtile = self
        elif self.layer == 'spirit':
          tiles[x][y].spirit = None
          tiles[nx][ny].spirit = self

        if trigger:
          self.model.chain.append(Move(self, dx,dy))

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

        # Create a chain
        self.model.chain = []

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

        # If changes were added to the chain, append chain to changes
        if len(self.model.chain) > 0:
          self.model.update_now = True
          print("Chain added to changes:")
          print(self.model.chain)
          self.model.changes.append(self.model.chain)
    
    def move_check(self, dx,dy):
      # Entity moves if it can (check passing)
      # Return True if move possible, else otherwise

      nx = self.x + dx
      ny = self.y + dy

      # Check if Out of Bounds
      inside_bounds = (0 <= nx < TILES_HOR and 0 <= ny < TILES_VER)

      if inside_bounds:
          new_tile = self.level.tiles[nx][ny]
          passes = self.check_passing(new_tile)
          
          occupant = new_tile.occupant
          if occupant is None and passes:
            self.move(dx,dy, trigger = True)
            move_possible = True
          else:
            move_possible = False

      return(move_possible)
              
        
    def transition(self, dx,dy, trigger = True):
        # Transition to new level
        # Only player controlled creatures can transition?
        if self == self.level.player: #self.controller not None:
            # Current level key
            ku,kv = self.level.key
            # Next level key
            nu,nv = ku+dx, kv+dy

            # Check if there is another level in that direction
            if (nu,nv) in self.model.levels:
                # Add transition change to chain
                if trigger:
                  self.model.chain.append(Transition(self, dx,dy))

                print("Old level: {}".format(self.level.key))
                # Transition to the new level
                old_level = self.model.levels[(ku,kv)]
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
                self.move(0,0, trigger=False)
                print("New level: {}".format(self.level.key))

                # Remove entity from old level entities list and add it to the new one
                print(len(self.level.entities))
                old_level.entities.remove(self)
                new_level.entities.append(self)

                # Change batch
                self.sprite.batch = self.level.batch
                # Change corresponding groups?

                if self.layer == 'entity':
                  group = self.level.ent_group
                elif self.layer == 'overtile':
                  group = self.level.over_tiles_group
                elif self.layer == 'spirit':
                  group = self.level.spirit_group

                self.sprite.group = group

                # Change current level
                print("Current Level key: {}".format(self.model.current_level.key))
                print("Current coordinates: {},{}".format(self.x,self.y))
                print("Current sprite coordinates: {},{}".format(self.sprite.x,self.sprite.y))
                self.model.current_level = self.level
                print("Current Level key: {}".format(self.model.current_level.key))
                print("Current coordinates: {},{}".format(self.x,self.y))
                #self.update()
                print("Current sprite coordinates: {},{}".format(self.sprite.x,self.sprite.y))

    def check_passing(self, tile):
        # Check if the creature can walk to the tile
        # Depends on creature and tile properties
        #cre = self.creature

        """
        solid_spirit = (cre.spirit
                        and not tile.electricity and tile.solid)
        water_swim = (cre.swims and tile.water)"""
        
        if self.creature:
          is_spirit = self.creature['spirit']
        else:
          is_spirit = False

        if is_spirit:
          passes = not tile.properties['electricity']
        else:
          passes = not tile.properties['solid']

          if (tile.properties['pass_small']):
            passes = self.creature['small']

          if tile.overtile:
            has_bridge = (tile.overtile.status == 'bridge')
          else:
            has_bridge = False

          if (tile.properties['water'] and not has_bridge):
            passes = (self.creature['swims'] or self.creature['flying'])

          if has_bridge: #tile.bridge:
            print("Bridge: {}".format(tile.overtile))
            print(tile.overtile.x, tile.overtile.y)

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
        self.model.chain.append(Possess(self, cre_ent))

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

        self.model.chain.append(Depossess(spirit, self))

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

    def destroy(self):
        # Remove creature from the list of creatures
        self.level.entities.remove(self)
        # Creature no longer occupies its tile
        self.level.tiles[self.x][self.y].occupant = None
        # Creature drops all items in its inventory
        #self.model.tiles[self.x][self.y].items += self.inventory

def assign_entity_data(ent):
    # ent is the input Entity
    ent_id = ent.ent_id

    # Assign entity layer
    ent.layer = entity_dict[ent_id]['layer']

    # Assign entity type
    ent.type = entity_dict[ent_id]['type']
    # Assign creature properties
    ent.creature = entity_dict[ent_id]['creature']
    # Assign object properties
    ent.object = entity_dict[ent_id]['object']
    # Assign interactor component
    if entity_dict[ent_id]['interactor'] is not None:
        ent.interactor = entity_dict[ent_id]['interactor'](ent)
    else:
        ent.interactor = None
    # Assign lander component
    if entity_dict[ent_id]['lander'] is not None:
        ent.lander = entity_dict[ent_id]['lander'](ent)
    else:
        ent.lander = None
    
    # Assign initial status
    ent.status = entity_dict[ent_id]['status']
    # Assign status to sprite mapping
    spritesheet = ent.game_scene.spritesheet
    status_to_sprite_ind = entity_dict[ent_id]['status_to_sprite_ind']
    ent.status_to_sprite = {k:spritesheet[v]
                            for k,v in status_to_sprite_ind.items()}

entity_dict = {
    'player': {'type':'creature',
                'layer':'entity',
               'creature':creature_dict['player'],
               'object':None,
               'status':'default',
               'status_to_sprite_ind':{'default':(3,3)},
               'interactor':None,
               'lander':None}, #enterer?
    'spirit': {'type':'spirit', #creature?
                'layer':'spirit',
               'creature':creature_dict['spirit'],
               'object':None,
               'status':'default',
               'status_to_sprite_ind':{'default':(2,2)},
               'interactor':None,
               'lander':None}, #enterer?
    'bird': {'type':'creature', #creature?
              'layer':'entity',
               'creature':creature_dict['bird'],
               'object':None,
               'status':'default',
               'status_to_sprite_ind':{'default':(5,6)},
               'interactor':None,
               'lander':None}, #enterer?
    'mouse': {'type':'creature', #creature?
                'layer':'entity',
               'creature':creature_dict['mouse'],
               'object':None,
               'status':'default',
               'status_to_sprite_ind':{'default':(5,5)},
               'interactor':None,
               'lander':None}, #enterer?
    'boulder': {'type':'object',
                'layer':'entity',
               'creature':None,
               'object':None, #object_dict['boulder'],
               'status':'default',
               'status_to_sprite_ind':{'default':(4,4), 'bridge':(3,5)},
               'interactor':Pushable,
                'lander':Sinker},
    'lever': {'type':'object',
                'layer':'entity',
               'creature':None,
               'object':None, #object_dict['boulder'],
               'status':'off',
               'status_to_sprite_ind':{'off':(7,5), 'on':(7,6)},
               'interactor':Lever,
                'lander':None},
    'bars': {'type':'object',
                'layer':'overtile',
               'creature':None,
               'object':None, #object_dict['boulder'],
               'status':'default',
               'status_to_sprite_ind':{'default':(9,5), 'broken':(8,5)},
               'interactor':Breakable,
                'lander':None},
    'paint_brush': {'type':'object',
                'layer':'entity',
               'creature':None,
               'object':None, #object_dict['boulder'],
               'status':'default',
               'status_to_sprite_ind':{'default':(7,1), 'red':(7,2), 'green':(7,3), 'blue':(7,4)},
               'interactor':Pushable,
                'lander':Painter},
    'letter_block': {'type':'object',
                'layer':'entity',
               'creature':None,
               'object':None, #object_dict['boulder'],
               'status':'default',
               'status_to_sprite_ind':{'default':(4,11), 'A': (9, 10), 'B': (9, 11), 'C': (9, 12), 'D': (9, 13), 
               'E': (9, 14), 'F': (8, 10), 'G': (8, 11), 'H': (8, 12), 'I': (8, 13), 'J': (8, 14), 'K': (7, 10), 
               'L': (7, 11), 'M': (7, 12), 'N': (7, 13), 'O': (7, 14), 'P': (6, 10), 'Q': (6, 11), 'R': (6, 12), 
               'S': (6, 13), 'T': (6, 14), 'U': (5, 10), 'V': (5, 11), 'W': (5, 12), 'X': (5, 13), 'Y': (5, 14), 
               'Z': (4, 10)},
               'interactor':Pushable,
                'lander':None}
}
