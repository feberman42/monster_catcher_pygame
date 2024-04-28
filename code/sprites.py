from pygame.sprite import Group
from settings import *

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos: tuple[int], surf: pygame.Surface, groups: Group) -> None:
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft = pos)