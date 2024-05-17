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
		self.blocked = False

		# sprite setup
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		self.hitbox = self.rect.inflate(-self.rect.width / 2, -60)
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
	
	def change_facing_direction(self, target_pos):
		relation = vector(target_pos) - vector(self.rect.center)
		if abs(relation.y) < 30:
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		elif abs(relation.x) < 30:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		self.blocked = True
		self.direction = vector(0, 0)
	
	def unblock(self):
		self.blocked = False

class Character(Entity):
	def __init__(self, pos: tuple[int], frames: dict, start_dir: str, groups: Group, character_data) -> None:
		super().__init__(pos, frames, start_dir, groups)
		print(character_data)
	
	def update(self, dt) -> None:
		self.animate(dt)

class Player(Entity):
	def __init__(self, pos: tuple[int], frames:dict, start_dir: str, groups: Group, collision_sprites) -> None:
		super().__init__(pos, frames, start_dir, groups)
		self.collision_sprites = collision_sprites

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
		if self.direction:
			self.direction.normalize_ip()

	def move(self, dt: float) -> None:
		self.rect.centerx += self.direction.x * 200 * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')
		self.rect.centery += self.direction.y * 200 * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	def collisions(self, axis):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if axis  == 'horizontal':
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					else:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				elif axis == 'vertical':
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					else:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def update(self, dt: float) -> None:
		self.y_sort = self.rect.bottom
		if not self.blocked:
			self.input()
			self.move(dt)
		self.animate(dt)
