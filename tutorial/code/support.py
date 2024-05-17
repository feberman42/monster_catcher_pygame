from settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from entities import Entity

# imports 
def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	return surf

def import_folder(*path):
	frames = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames.append(surf)
	return frames

def import_folder_dict(*path):
	frames = {}
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames[image_name.split('.')[0]] = surf
	return frames

def import_sub_folders(*path):
	frames = {}
	for _, sub_folders, __ in walk(join(*path)):
		if sub_folders:
			for sub_folder in sub_folders:
				frames[sub_folder] = import_folder(*path, sub_folder)
	return frames

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames

def coast_importer(cols, rows, *path):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	terrains = ['grass', 'grass_i', 'sand_i', 'sand', 'rock', 'rock_i', 'ice', 'ice_i']
	sides = {
		'topleft': (0, 0), 'top': (1, 0), 'topright': (2, 0),
		'left': (0, 1), 'right': (2, 1),
		'bottomleft': (0, 2), 'bottom': (1, 2), 'bottomright': (2, 2)
	}
	for index, terrain in enumerate(terrains):
		new_dict[terrain] = {}
		for key, pos in sides.items():
			new_dict[terrain][key] = [frame_dict[(pos[0] + index * 3, pos[1] + row)] for row in range(0, rows, 3)]
	return new_dict

def character_import(cols: int, rows: int, *path: tuple[str]):
	frame_dict = import_tilemap(cols, rows, *path)
	new_dict = {}
	for row, direction in enumerate(('down', 'left', 'right', 'up')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(cols)]
		new_dict[f'{direction}_idle'] = [frame_dict[0, row]]
	return new_dict

def all_characters_import(*path: tuple[str]):
	new_dict = {}
	for dir_path, dir_names, file_names in walk(join(*path)):
		for file in file_names:
			image_name = file.split('.')[0]
			new_dict[image_name] = character_import(4, 4, *path, image_name)
	return new_dict


# game functions

def check_connection(radius: float, entity: Entity, target: Entity, tolerance = 30) -> bool:
	relation = vector(target.rect.center) - vector(entity.rect.center)
	if relation.length() < radius:
		if abs(relation.y) < tolerance:
			if ((entity.facing_direction == 'left' and relation.x < 0) or 
				(entity.facing_direction == 'right' and relation.x > 0)):
				return True
		elif abs(relation.x) < tolerance:
			if ((entity.facing_direction == 'up' and relation.y < 0) or 
				(entity.facing_direction == 'down' and relation.y > 0)):
				return True
	return False