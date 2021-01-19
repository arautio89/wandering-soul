# mechanisms.py

from config import *

class Mechanism:
	def __init__(self, conditions, results):
		self.conditions = conditions
		self.results = results

		level.mechanisms.append(self)

	def check_conditions(self):
		cond_met = all([ent.status == status for ent,status in self.conditions])
		if cond_met:
			for ent,new_status in results:
				ent.change_status(new_status, save_change=True)

class AnagramMechanism:
	def __init__(self, text_result_dict, level):
		self.text_result_dict = text_result_dict
		self.level = level

		level.mechanisms.append(self)

	def check_conditions(self):
		level_string = get_text_from_level(self.level)
		print(level_string)

		if level_string in self.text_result_dict:
			results = self.text_result_dict[level_string]
		else:
			results = self.text_result_dict['*else*']
		for ent,new_status in results:
			ent.change_status(new_status, save_change=True)


def from_grid_to_string(grid):
    # Grid (list of lists)
    list_of_row_strings = ["".join(row) for row in grid]
    raw_string = " ".join(list_of_row_strings)

    final_string = " ".join(raw_string.split()).lower()

    return(final_string)

def get_text_from_level(level):
	tiles = level.tiles

	# Create a grid of letters, letters come from letter blocks, ' ' otherwise
	
	letter_grid = [[tiles[x][y].occupant.status
	 if tiles[x][y].occupant and tiles[x][y].occupant.ent_id == 'letter_block'
	 else ' ' for x in range(TILES_HOR)] for y in range(TILES_VER)]
	 
	"""
	 for x in range(TILES_HOR):
	 	for y in range(TILES_VER):
	"""
	
	level_string = from_grid_to_string(letter_grid)

	return(level_string)