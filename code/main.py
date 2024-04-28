from settings import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from os.path import join
from sprites import Sprite
from entities import Player

class Game:
	def __init__(self) -> None:
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Catcher')
		self.clock = pygame.time.Clock()

		self.all_sprites = pygame.sprite.Group()

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')

	def import_assets(self) -> None:
		self.tmx_maps = {'world': load_pygame(join('data', 'maps', 'world.tmx'))}

	def setup(self, tmx_map: TiledMap, player_styart_position: str) -> None:
		for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
			Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player' and obj.properties['pos'] == player_styart_position:
				Player((obj.x, obj.y), self.all_sprites)

	def run(self) -> None:
		while True:
			dt = self.clock.tick() / 1000
			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# game logic
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()