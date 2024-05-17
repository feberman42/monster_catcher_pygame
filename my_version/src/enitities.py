from typing import Any
from pygame import Surface
from pygame.sprite import Group
from config import *
from sprites import Sprite

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos: tuple[int], frames: dict, *groups: tuple[Group]) -> None:
		super().__init__(*groups)
		self.facing_direction = 'down'
		self.frame_index = 0
		self.frames = frames
		self.animation_speed = 8
		self.image = self.frames['down'][0]
		self.rect = self.image.get_frect(midbottom = (pos[0] * 2, pos[1] * 2))
		self.direction = vector()
		self.move_speed = 250

	def animate(self, dt: float) -> None:
		moving = bool(self.direction)
		key = self.facing_direction if moving else self.facing_direction + '_idle'
		self.frame_index += dt * self.animation_speed
		self.image = self.frames[key][int(self.frame_index % len(key))]
		self.rect = self.image.get_frect()
	
	def update(self, dt: float) -> None:
		self.animate(dt)

class Player(Entity):
	def __init__(self, pos: tuple[int], frames: dict, *groups: tuple[Group]) -> None:
		super().__init__(pos, frames, *groups)

	def input(self) -> None:
		keys = pygame.key.get_pressed()
		input_vector = vector()
		if (keys[pygame.K_UP] or keys[pygame.K_w]): input_vector.y -= 1
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]): input_vector.y += 1
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]): input_vector.x -= 1
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]): input_vector.x += 1
		self.direction = input_vector
		if (self.direction):
			self.direction.normalize_ip()

	def move(self, dt: float) -> None:
		self.rect.centerx += self.direction.x * dt * self.move_speed
		self.rect.centery += self.direction.y * dt * self.move_speed

	def update(self, dt: float) -> None:
		super().update(dt)
		self.input()
		self.move(dt)


