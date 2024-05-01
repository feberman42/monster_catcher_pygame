from typing import Any
from pygame import Surface
from pygame.sprite import Group
from settings import *

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos: tuple[int], surf: pygame.Surface, groups: Group) -> None:
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
	def __init__(self, pos: tuple[int], frames: list[Surface], groups: Group) -> None:
		super().__init__(pos, frames[0], groups)
		self.frame_index = 0
		self.frames = frames

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt) -> None:
		self.animate(dt)
