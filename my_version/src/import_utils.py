from config import *

def import_image(*path, alpha = True, format = 'png') -> pygame.surface.Surface:
	full_path = join(*path) + '.' + format
	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	return pygame.transform.scale_by(surf, 3)

def import_char(*path) -> dict:
	char_dict = {}
	for base, dirs, files in walk(join(*path)):
		for dir in dirs:
			char_dict[dir] = import_char_anim(join(base, dir))
	return char_dict

def import_char_anim(path) -> list[pygame.surface.Surface]:
	anim = []
	for base, dirs, files in walk(path):
		for file in sorted(files):
			anim.append(pygame.transform.scale_by(pygame.image.load(join(base, file)).convert_alpha(), 3))
	return anim
