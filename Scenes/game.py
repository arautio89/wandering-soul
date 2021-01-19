# Scenes
# game.py

import pyglet

from pyglet.window import key
from pyglet.window import mouse

from config import *
from Scenes.model import *

#from scene_manager import SceneManager

pyglet.resource.path = ['Images']
pyglet.resource.reindex()

#TILE_SIZE = 32
#TILES_HOR = 25
#TILES_VER = 20

# Game Scene
class Game:
    def __init__(self, scene_manager):
        self.scene_id = 'game'
        self.scene_manager = scene_manager
        self.window = scene_manager.window

        #self.define_buttons()
        self.load_images()

        # Define My Batch
        self.my_batch = pyglet.graphics.Batch()
        # Define My Groups (Group for tiles, group for creatures)
        self.tiles_group = pyglet.graphics.OrderedGroup(0)
        self.over_tiles_group = pyglet.graphics.OrderedGroup(1)
        self.ent_group = pyglet.graphics.OrderedGroup(2)
        self.spirit_group = pyglet.graphics.OrderedGroup(3)

        self.model = Model(self)

        # Set Sprites, fill batches
        #self.set_sprites()

        # Movement Delay (in frames)
        self.max_delay = MAX_DELAY
        self.delay = 0

        self.key_handler = pyglet.window.key.KeyStateHandler()

        self.key_dict = {key.UP:(0,-1), key.DOWN:(0,1),
                    key.LEFT:(-1,0), key.RIGHT:(1,0)}

        #self.set_decorators()

    def enter_scene(self):
        self.window.push_handlers(self.key_handler)

    def exit_scene(self):
        self.window.pop_handlers() 
        
    def on_mouse_press(self, x,y, button, modifiers):
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            if button == mouse.LEFT:
                print('The left mouse button was pressed.')
                """
                for b in self.buttons:
                    if (b.x <= x <= b.x + b.w and b.y <= y <= b.y + b.h):
                        b.click()"""
              
    def on_key_press(self, symbol, modifiers):
        print("Key Pressed in Game Scene!")
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            if symbol == pyglet.window.key.ESCAPE:
                self.goto_main_menu()
                return pyglet.event.EVENT_HANDLED
            elif symbol == pyglet.window.key.SPACE:
                # Regenerate the Maze
                print("Space Bar!")
                #self.set_sprites()
            elif symbol == pyglet.window.key.TAB:
                print("Tab Key!:")
                #self.update_gfx()
            elif symbol == pyglet.window.key.U:
                self.model.undo_latest()
                

    def on_draw(self):            
        #if self.scene_manager.current_scene_id == 'game':
        if self.scene_manager.current == self:
            self.window.clear()
            #self.my_batch.draw()
            self.model.current_level.batch.draw()
        
    def update(self, dt):
        
        player = self.model.current_level.player

        """
        key_dict = {key.UP:(0,-1), key.DOWN:(0,1),
                    key.LEFT:(-1,0), key.RIGHT:(1,0)}
        """

        key_dict = self.key_dict
        
        if self.delay > 0:
            self.delay -= 1
        else:
            # Only move when exactly one arrow is pressed
            buttons_pressed = 0
            dx, dy = 0,0
            move = False
            for k in key_dict:
                if (self.key_handler[k]):
                    buttons_pressed += 1
                    if buttons_pressed == 1:
                        dx, dy = key_dict[k]
                        move = True
                    else:
                        dx, dy = 0,0
                        move = False

            if move:
                player.move_action(dx,dy)
                self.delay = self.max_delay

        if self.model.update_now:
            #self.update_gfx()

            #print(self.model.current_level.mechanisms)
            for mechanism in self.model.current_level.mechanisms:
                mechanism.check_conditions()

            for ent in self.model.current_level.entities:
                #print(ent.ent_id)
                ent.update()
            self.model.update_now = False
            

    def set_bg(self):
        #self.bg_batch.add()
        pass
        

    def load_images(self):
        self.bg_img = pyglet.resource.image('bg_forest_800x640.jpg')
        # Sprite Sheet
        sprite_sheet = pyglet.resource.image('spritesheet.png')
        sprite_sheet_seq = pyglet.image.ImageGrid(sprite_sheet, 20, 20)
        # Texture Sequence
        self.spritesheet = pyglet.image.TextureGrid(sprite_sheet_seq)
        
        print("Images Loaded!")

    def goto_main_menu(self):
        self.scene_manager.change_scene('main menu')


