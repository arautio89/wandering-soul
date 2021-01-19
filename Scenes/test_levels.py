
from config import *

from Scenes.levels import *
from Scenes.tiles import *
from Scenes.entities import *
from Scenes.mechanisms import *


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

    Tile(22,15, tile_id = 'crack',
            level = level1, place_it = True, status='horizontal')
    Tile(22,14, tile_id = 'crack',
            level = level1, place_it = True, status='vertical')

    Entity(15,15, ent_id = 'player', level = level1)
    Entity(16,15, ent_id = 'bird', level = level1)
    Entity(17,15, ent_id = 'mouse', level = level1)

    level1.player = Entity(10,10, ent_id = 'spirit', level = level1)

    Entity(17,17, ent_id = 'boulder', level = level1)

    for x in range(19,21): #(1, TILES_HOR-1)
        for y in range(17,19): #(1, TILES_VER-1)
            Tile(x,y, tile_id = 'water',
            level = level1, place_it = True)

    for x in range(15,18):
        for y in range(5,8):
            Tile(x,y, tile_id = 'toggle_tile',
             level = level1, place_it = True)

    for x in range(11,14):
        for y in range(5,8):
            Tile(x,y, tile_id = 'canvas',
             level = level1, place_it = True)

    rbrush = Entity(5,8, ent_id = 'paint_brush', level = level1, status='red')
    gbrush = Entity(6,8, ent_id = 'paint_brush', level = level1, status='green')
    bbrush = Entity(7,8, ent_id = 'paint_brush', level = level1, status='blue')
        
    Tile(9,9, tile_id = 'pressure_plate',
             level = level1, place_it = True)

    Tile(2,2, tile_id = 'extractor',
             level = level1, place_it = True)

    for x in range(4,6):
        for y in range(4,6):
            Tile(x,y, tile_id = 'icy_floor',
             level = level1, place_it = True)

    Tile(6,5, tile_id = 'wall',
             level = level1, place_it = True)

    Entity(5,15, ent_id = 'lever', level = level1)
    Entity(7,15, ent_id = 'lever', level = level1, status='on')

    Entity(5,12, ent_id = 'bars', level = level1)
    Entity(6,12, ent_id = 'bars', level = level1, status='broken')

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

    # Level 3
    level3 = Level(model = model, name = 'Test Level', key = (1,0))

    for x in range(TILES_HOR): #(1, TILES_HOR-1)
        for y in range(TILES_VER): #(1, TILES_VER-1)
            Tile(x,y, tile_id = 'floor',
            level = level3, place_it = True)
        
    for x in range(TILES_HOR):
        Tile(x,0, tile_id = 'wall',
            level = level3, place_it = True)
        Tile(x,TILES_VER - 1, tile_id = 'wall',
            level = level3, place_it = True)
            
    for y in range(TILES_VER):
        Tile(0,y, tile_id = 'wall',
            level = level3, place_it = True)
        Tile(TILES_HOR - 1,y, tile_id = 'wall',
            level = level3, place_it = True)

    print("West Passage")
    print(0,TILES_VER//2)
    Tile(0,TILES_VER//2, tile_id = 'floor',
            level = level3, place_it = True)

    print("East Passage")
    print(TILES_HOR - 1,TILES_VER//2)
    Tile(TILES_HOR - 1,TILES_VER//2, tile_id = 'floor',
            level = level3, place_it = True)

    print("North Passage")
    print(TILES_HOR//2,0)
    Tile(TILES_HOR//2,0, tile_id = 'floor',
            level = level3, place_it = True)

    print("South Passage")
    print(TILES_HOR//2,TILES_VER - 1)
    Tile(TILES_HOR//2,TILES_VER - 1, tile_id = 'floor',
            level = level3, place_it = True)


    brush = Entity(15,15, ent_id = 'paint_brush', level = level3, status='red')

    """
    alphabet=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for k in range(len(alphabet)):
    	letter = alphabet[k]
    	x = k%10 + 3
    	y = 2*(k//10) + 3
    	Entity(x,y, ent_id = 'letter_block', level = level3, status=letter)
    """

    
    letters=list('DIE GROSS CRAB')
    for k in range(len(letters)):
    	letter = letters[k]
    	if letter != ' ':
    		Entity(k+3,5, ent_id = 'letter_block', level = level3, status=letter)
    
    text_result_dict = {'bridge across': [(brush, 'blue')], '*else*':[(brush, 'red')]}
    anagram_mehcanism = AnagramMechanism(text_result_dict, level3)

    """
    letters=list('ABC')
    for k in range(len(letters)):
    	letter = letters[k]
    	if letter != ' ':
    		Entity(k+3,5, ent_id = 'letter_block', level = level3, status=letter)

    text_result_dict = {'cba': [(brush, 'blue')], '*else*':[(brush, 'red')]}
    anagram_mehcanism = AnagramMechanism(text_result_dict, level3)
    """

    #return(levels)