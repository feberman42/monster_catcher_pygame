from typing import Any
from pygame.sprite import Group
from settings import *

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos: tuple[int], frames: dict, start_dir: str, groups: Group) -> None:
		super().__init__(groups)
		self.z_layer = WORLD_LAYERS['main']

		# graphics
		self.frame_index, self.frames = 0, frames
		self.facing_direction = start_dir

		# movement
		self.direction = vector()
		self.speed = 250

		# sprite setup
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		self.y_sort = self.rect.bottom

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]

	def get_state(self):
		moving = bool(self.direction)
		if (self.direction.x < 0): self.facing_direction = 'left'
		elif (self.direction.x > 0): self.facing_direction = 'right'
		if (self.direction.y < 0): self.facing_direction = 'up'
		elif (self.direction.y > 0): self.facing_direction = 'down'

		return (f'{self.facing_direction}{"" if moving else "_idle"}')

class Character(Entity):
	def __init__(self, pos: tuple[int], frames: dict, start_dir: str, groups: Group) -> None:
		super().__init__(pos, frames, start_dir, groups)
	
	def update(self, dt) -> None:
		pass

class Player(Entity):
	def __init__(self, pos: tuple[int], frames:dict, start_dir: str, groups: Group) -> None:
		super().__init__(pos, frames, start_dir, groups)

	def input(self) -> None:
		keys = pygame.key.get_pressed()
		input_vector = vector()
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		self.direction = input_vector

	def move(self, dt: float) -> None:
		self.rect.center += self.direction * 200 * dt

	def update(self, dt: float) -> None:
		self.y_sort = self.rect.bottom
		self.input()
		self.move(dt)
		self.animate(dt)
