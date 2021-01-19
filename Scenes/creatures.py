# Scenes
# creatures.py

# Creature Dictionary, keys are tile_id, values are tile properties

# sprite_dict for each creature?
creature_properties = ['strong', 'small', 'swims', 'icewalk', 'flying',
                       'wallclimb', 'spirit']

# pass_small or block_small?

# 'default' properties are False for all properties
# 'default':{'solid':False, 'water':False, }

creature_dict = {
    'player': {'strong':True, 'small':False},
    'human': {'strong':False, 'small':False},
    'spirit': {'spirit':True, 'flying':True},
    'fishman': {'swims':True},
    'bird': {'flying':True},
    'mouse': {'small':True},
    'claw beast': {'icewalk':True},
    'beast': {'strong':True}
    }

"""
creature_dict = {
    'player': {'sprite_ind':(3,3), 'strong':True, 'small':False},
    'human': {'sprite_ind':(3,3), 'strong':False, 'small':False},
    'spirit': {'spirit':True},
    'fishman': {'swims':True},
    'bird': {'flying':True},
    'claw beast': {'icewalk':True},
    'beast': {'strong':True}
    }
"""
for k,v in creature_dict.items():
    for p in creature_properties:
        if p not in v:
            v[p] = False
