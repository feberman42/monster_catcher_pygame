from config import *
import pytmx
from sys import exit
from sprites import Sprite
from groups import VisibleSprites
from enitities import Player
from import_utils import *

class Game:
	def __init__(self) -> None:
		pygame.init()
		self.display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.Clock()

		self.visible_sprites = VisibleSprites()

		self.import_assets()
		self.setup()

	def import_assets(self) -> None:
		# tmx maps
		self.tmx_maps = {
			'test': pytmx.load_pygame(join(PATH ,'..', 'data', 'tmx', 'world.tmx'))
		}

		# character frames
		self.character_frames = {
			'player': import_char(PATH, '..', 'graphics', 'characters', 'player')
		}

	def setup(self) -> None:
		# ground
		for x, y, surf in self.tmx_maps['test'].get_layer_by_name('Ground').tiles():
			Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.visible_sprites)

		# objects
		for obj in self.tmx_maps['test'].get_layer_by_name('props'):
			Sprite((int(obj.x), int(obj.y)), obj.image, self.visible_sprites)

		# entities
		self.player = Player((0, 0), self.character_frames['player'], self.visible_sprites)

	
	def run(self) -> None:
		while (True):
			dt = self.clock.tick() / 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
			self.visible_sprites.update(dt)
			self.visible_sprites.draw(self.player.rect.center)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
