from settings import *
from support import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from os.path import join
from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite
from entities import Player, Character
from groups import AllSprites
from game_data import TRAINER_DATA

class Game:
	def __init__(self) -> None:
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Monster Catcher')
		self.clock = pygame.time.Clock()

		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')

	def import_assets(self) -> None:
		self.tmx_maps = {
			'world': load_pygame(join('data', 'maps', 'world.tmx')),
			'hospital': load_pygame(join('data', 'maps', 'hospital.tmx'))
			}
		
		self.overworld_frames = {
			'water': import_folder('graphics', 'tilesets', 'water'),
			'coast': coast_importer(24, 12, 'graphics', 'tilesets', 'coast'),
			'characters': all_characters_import('graphics', 'characters')
		}

		self.fonts = {
			'dialog': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 30)
		}

	def setup(self, tmx_map: TiledMap, player_start_position: str) -> None:
		# terrain
		for layer in ['Terrain', 'Terrain Top']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

		# water
		for obj in tmx_map.get_layer_by_name('Water'):
			for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
				for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
					AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])

		# coast
		for obj in tmx_map.get_layer_by_name('Coast'):
			terrain = obj.properties['terrain']
			side = obj.properties['side']
			AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'])

		# objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
			else:
				CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

		# collision obj
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# grass patches
		for obj in tmx_map.get_layer_by_name('Monsters'):
			MonsterPatchSprite((obj.x, obj.y), obj.image, self.all_sprites, obj.properties['biome'])

		# entities
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player' and obj.properties['pos'] == player_start_position:
				self.player = Player(
					pos = (obj.x, obj.y),
					frames = self.overworld_frames['characters']['player'],
					start_dir = obj.properties['direction'],
					collision_sprites = self.collision_sprites,
					groups = self.all_sprites)
			elif obj.name == 'Character':
				Character(
					pos = (obj.x, obj.y),
					frames = self.overworld_frames['characters'][obj.properties['graphic']],
					start_dir = obj.properties['direction'],
					groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
					character_data = TRAINER_DATA[obj.properties['character_id']])

	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE]:
			for character in self.character_sprites:
				if check_connection(100, self.player, character):
					self.player.block()
					character.change_facing_direction(self.player.rect.center)
					print('dialog')

	def run(self) -> None:
		while True:
			dt = self.clock.tick() / 1000
			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# game logic
			self.input()
			self.all_sprites.update(dt)
			self.display_surface.fill('black')
			self.all_sprites.draw(self.player.rect.center)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()