from config import *
from pygame import sprite

class VisibleSprites(sprite.Group):
	def __init__(self) -> None:
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = vector()

	def draw(self, player_pos: tuple[int]) -> None:
		self.offset.x = -(player_pos[0] - WIN_WIDTH / 2)
		self.offset.y = -(player_pos[1] - WIN_HEIGHT / 2)

		self.display_surface.fill('black')
		for sprite in self:
			self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
