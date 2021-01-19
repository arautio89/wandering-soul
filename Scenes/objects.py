# Scenes
# objects.py

from config import *
from Scenes.changes import *

# objects are inanimate, boulders, doors, etc.

# sprite_dict for each creature?
#object_properties = ['pushable']

# pass_small or block_small?

# 'default' properties are False for all properties
# 'default':{'solid':False, 'water':False, }

"""
object_dict = {
    'boulder': {'sprite_ind':(4,4), 'pushable':True}
    }
"""

"""
object_dict = {
    'boulder': {'sprite_ind':(4,4), 'interactor':Pushable}
    }

for k,v in object_dict.items():
    for p in object_properties:
        if p not in v:
            v[p] = False
"""

### Interaction components

class Pushable:
    def __init__(self, owner):
        self.owner = owner
        pass

    def interaction(self, actor, dx, dy):
        # actor: the pusher, dx,dy push direction
        tiles = self.owner.level.tiles

        # Coordinates of the Pushable Entity
        ex, ey = self.owner.x, self.owner.y
        # Possible New Coordinates for the Pushable Entity
        nx, ny = ex + dx, ey + dy

        # CHECK ACTOR STRENGTH AND PUSHABLE WEIGHT???

        push_move = False
        # Check if inside bounds for the pushable Entity
        if (0 <= nx < TILES_HOR and 0 <= ny < TILES_VER):
            ### Check if the Pusher can pass onto the tile!!!
            #etile = tiles[ex][ey]
            passes = actor.check_passing(tiles[ex][ey])
            if passes:
                # Check if the new tile is solid
                if (tiles[nx][ny].properties['solid'] == False):
                    # Check if the Tile is not occupied
                    if (tiles[nx][ny].occupant is None):
                        push_move = True

        if push_move:
            # Move the Pushable Entity
            self.owner.move(dx,dy)
            # Move the actor (Pusher)
            actor.move(dx,dy)
            # Update
            self.owner.update()

class Breakable:
    def __init__(self, owner):
        self.owner = owner
        #self.broken = False
        pass

    def interaction(self, actor, dx, dy):
        # actor: the breaker, dx,dy break direction

        # CHECK ACTOR STRENGTH AND BREAKABLE WEIGHT???
        if actor.creature['strong']:
            new_status = 'broken'
            self.owner.change_status(new_status, save_change=True)

class Lever:
    def __init__(self, owner):
        self.owner = owner
        #self.lever = False
        self.mapping = {'on':'off', 'off':'on'}
        pass

    def interaction(self, actor, dx, dy):
        #self.owner.status = self.mapping[self.owner.status]
        old_status = self.owner.status
        new_status = self.mapping[old_status]
        self.owner.change_status(new_status, save_change=True)

"""
class Possessor:
    def __init__(self, owner):
        self.owner = owner

    def interaction(self, actor, dx, dy):
        # actor: 
"""

class Painter:
    # Painting Brush
    def __init__(self, owner): #color
        self.owner = owner
        #self.color = color
        #self.color = 'red'
        #self.owner.color = 'red'

    def landing(self, dx, dy):
        tiles = self.owner.level.tiles
        # Entity lands on a tile
        x = self.owner.x
        y = self.owner.y

        # Check if landing tile is a canvas / has canvas True
        tile = tiles[x][y]
        if tile.tile_id == 'canvas':
            #old_status = tile.status
            new_status = self.owner.status
            #tile.status = new_status #self.color
            #self.owner.model.chain.append(ChangeStatus(tile,old_status,new_status))
            tile.change_status(new_status, save_change=True)
            #tile.update()
        # tiles[x][y].???.color = self.color
            
class Sinker:
    # Object that falls to water and creates a bridge
    def __init__(self, owner):
        self.owner = owner

    def landing(self,dx,dy):
        # Entity lands on a tile
        x = self.owner.x
        y = self.owner.y

        tile = self.owner.level.tiles[x][y]

        if tile.properties['water']:
            # Is the a bridge in the water already?
            if tile.overtile is None: #tile.bridge is None:
                # Object sinks into the water, creating a bridge
                print("{} sunk into {}".format(self.owner.ent_id, tile.tile_id))
                print("Entity xy: {},{}, Tile xy: {},{}".format(self.owner.x,self.owner.y, tile.x, tile.y))
                #tile.bridge = self.owner
                tile.overtile = self.owner
                #self.owner.status = 'sunken'
                self.owner.status = 'bridge'
                self.owner.sprite.group = self.owner.game_scene.over_tiles_group

                #new_status = 
                #self.owner.change_status(new_status, save_change=True)

                # Object is no longer an occupant
                tile.occupant = None

                self.owner.update()

                self.owner.model.chain.append(Sink(self))

    def undo_sink(self):
        # Entity gets "unsunk"
        x = self.owner.x
        y = self.owner.y

        tile = self.owner.level.tiles[x][y]

        # Object unsinks out of the water
        #tile.bridge = None
        tile.overtile = None
        self.owner.status = 'default'
        self.owner.sprite.group = self.owner.game_scene.ent_group

        # Object is no longer an occupant
        tile.occupant = self.owner

        self.owner.update()
        print("{} unsunk from {}".format(self.owner.ent_id, tile.tile_id))
        print("Entity xy: {},{}, Tile xy: {},{}".format(self.owner.x,self.owner.y, tile.x, tile.y))