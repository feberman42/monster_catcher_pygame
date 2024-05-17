from config import *
from pygame import sprite, surface

class Sprite(sprite.Sprite):
	def __init__(self, pos: tuple[int], surface: surface.Surface, *groups: tuple[sprite.Group]) -> None:
		super().__init__(*groups)
		self.image = pygame.transform.scale2x(surface)
		self.rect = self.image.get_frect(topleft = (pos[0] * 2, pos[1] * 2))
