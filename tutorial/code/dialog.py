from settings import *
from entities import Player, Character

class DialogTree:
	def __init__(self, character: Character, player: Player, all_sprites: pygame.sprite.Group, font: pygame.font.Font) -> None:
		self.player = player
		self.character = character
		self.all_sprites = all_sprites
		self.font = font

