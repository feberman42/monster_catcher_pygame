from config import *
from pygame import sprite

class VisibleSprites(sprite.Group):
	def __init__(self) -> None:
		super().__init__()
		self.display_surface = pygame.display.get_surface()

	def draw(self) -> None:
		for sprite in self:
			self.display_surface.blit(sprite.image, sprite.rect)
