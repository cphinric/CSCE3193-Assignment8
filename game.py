import pygame
import time
import os
import json

from pygame.locals import *
from time import sleep


class Sprite():
	def __init__(self, x, y, w, h, image_url):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.image = pygame.image.load(image_url)

	def isLink(self):
		return False

	def isTile(self):
		return False

	def isPot(self):
		return False

	def isBoom(self):
		return False

	def update(self):
		return


class Link (Sprite):
	def __init__(self, x, y, w, h, image_url):
		super().__init__(x, y, w, h, image_url)
		self.px = 0
		self.py = 0
		self.img = []
		self.image_url = self.image
		self.numImages = 50
		self.currentImage = 0
		self.linkR = False
		self.linkL = False
		self.linkU = False
		self.linkD = False

		for i in range(self.numImages):
			image_path = f"images/link{i+1}.png"
			image = pygame.image.load(image_path)
			self.img.append(image)

	def setPreviousPosition(self):
		self.px = self.x
		self.py = self.y

	def getOutofSprite(self, p):
		if (((self.px + self.w) <= p.x) & ((self.x + self.w) >= p.x)):
			self.x = p.x - self.w
		if ((self.px >= (p.x + p.w)) & (p.x <= (p.x + p.w))):
			self.x = p.x + p.w
		if (((self.py + self.h) <= p.y) & ((self.y + self.h) >= p.y)):
			self.y = p.y - self.h
		if (self.py >= (p.y + p.h)):
			self.y = p.y + p.h

	def updateImg(self, dir):
		if dir == 1:
			if 38 > self.currentImage >= 29:
				self.currentImage += 1
			else:
				self.currentImage = 29

			self.image = self.img[self.currentImage]
			self.linkR = False
			self.linkL = True
			self.linkU = False
			self.linkD = False
		if dir == 0:
			if 22 > self.currentImage >= 13:
				self.currentImage += 1
			else:
				self.currentImage = 13
			self.image = self.img[self.currentImage]
			self.linkR = True
			self.linkL = False
			self.linkU = False
			self.linkD = False
		if dir == 2:
			if 49 > self.currentImage >= 40:
				self.currentImage += 1
			else:
				self.currentImage = 40
			self.image = self.img[self.currentImage]
			self.linkR = False
			self.linkL = False
			self.linkU = True
			self.linkD = False
		if dir == 3:
			if 12 > self.currentImage >= 3:
				self.currentImage += 1
			else:
				self.currentImage = 3
			self.image = self.img[self.currentImage]
			self.linkR = False
			self.linkL = False
			self.linkU = False
			self.linkD = True

	def isLink(self):
		return True

	def isTile(self):
		return False

	def isPot(self):
		return False

	def isBoom(self):
		return False
	
class Tile (Sprite):
	def __init__(self, x, y, w, h, image_url):
		super().__init__(x, y, w, h, image_url)
	
	def isLink(self):
		return False

	def isTile(self):
		return True

	def isPot(self):
		return False

	def isBoom(self):
		return False
	
class Pot(Sprite):
    def __init__(self, x, y, w, h, image_url):
        super().__init__(x, y, w, h, image_url)
        self.vert_velocity = 0
        self.hor_velocity = 0
        self.isBroken = False
        self.numFrames = 0

    def update(self):
        self.x += self.vert_velocity
        self.y += self.hor_velocity

    def crack(self):
        self.isBroken = True
        #self.numFrames += 1
        self.image = pygame.image.load("images/pot_broken.png")
        self.vert_velocity = 0
        self.hor_velocity = 0
        # if self.numFrames > 20:
        #     self.numFrames = 0
	    
    def isLink(self):
        return False

    def isTile(self):
        return False

    def isPot(self):
        return True

    def isBoom(self):
        return False

class Boom (Sprite):
	def __init__(self, x, y, w, h, d, image_url):
		super().__init__(x, y, w, h, image_url)
		self.d = d
		self.x = x
		self.y = y
		self.vert_velocity = 0
		self.hor_velocity = 0
	
	def update(self):
		self.x += self.vert_velocity
		self.y += self.hor_velocity

		if self.d == 0:
			self.vert_velocity = -15
		if self.d == 1:
			self.vert_velocity = 15
		if self.d == 2:
			self.hor_velocity = -15
		if self.d == 3:
			self.hor_velocity = 15
	
	def isLink(self):
		return False

	def isTile(self):
		return False

	def isPot(self):
		return False

	def isBoom(self):
		return True
	

class Model():
	def __init__(self):
		self.sprites = []
		self.dest_x = 0
		self.dest_y = 0
		self.link = Link(50, 50, 73, 85, "images/link1.png")
		self.sprites.append(self.link)
		self.load_map("map.json")  # Load the map from JSON
		
	def load_map(self, map_file):
		with open(map_file, "r") as file:
			data = json.load(file)
			sprites = data["sprites"]
			for sprite_data in sprites:
				if "type" in sprite_data:
					if sprite_data["type"] == "tile":
						x = sprite_data["x"]
						y = sprite_data["y"]
						w = sprite_data["w"]
						h = sprite_data["h"]
						image_url = sprite_data["image_url"]
						tile = Tile(x, y, w, h, image_url)
						self.sprites.append(tile)
					elif sprite_data["type"] == "link":
						x = sprite_data["x"]
						y = sprite_data["y"]
						w = sprite_data["w"]
						h = sprite_data["h"]
						image_url = sprite_data["image_url"]
						link = Link(x, y, w, h, image_url)
						self.sprites.append(link)
					elif sprite_data["type"] == "pot":
						x = sprite_data["x"]
						y = sprite_data["y"]
						w = sprite_data["w"]
						h = sprite_data["h"]
						image_url = sprite_data["image_url"]
						pot = Pot(x, y, w, h, image_url)
						self.sprites.append(pot)



	def update(self):
		for sprite in self.sprites:
			sprite.update()
			if (self.isCollision(sprite, self.link)):
				if sprite.isTile():
					self.link.getOutofSprite(sprite)
				if sprite.isPot():
					if sprite.isBroken == False:
						if self.link.linkL:
							sprite.x = (self.link.x + self.link.w)
							sprite.vert_velocity = 20
						if self.link.linkR:
							sprite.x = (self.link.x - sprite.w)
							sprite.vert_velocity = -20
						if self.link.linkU:
							sprite.y = (self.link.y - sprite.h)
							sprite.hor_velocity = -20
						if self.link.linkD:
							sprite.y = (self.link.y + self.link.h)
							sprite.hor_velocity = 20
			if (sprite.isPot()):
				for j in self.sprites:
					if(self.isCollision(sprite, j)):
						if(j.isTile()):
							sprite.crack()
							break
						if(j.isBoom()):
							sprite.crack()
							self.sprites.remove(j)
							break
					if sprite.isBroken:
						sprite.numFrames += 1
						if sprite.numFrames > 100:
							self.sprites.remove(sprite)
							break
			if (sprite.isBoom()):
				for j in self.sprites:
					if (self.isCollision(sprite, j)):
						if(j.isTile()):
							self.sprites.remove(sprite)

	def isCollision(self, t, b):
		if (b.x + b.w <= t.x):
			return False
		if (b.x >= t.x + t.w):
			return False
		if (b.y + b.h <= t.y):
			return False
		if (b.y >= t.y + t.h):
			return False
		else:
			return True
	
	def addBoom(self):
		if(self.link.linkR == True):
			self.sprites.append(Boom(self.link.x, self.link.y + 40, 8, 12, 0, "images/boomerang1.png"))
		if(self.link.linkL == True):
			self.sprites.append(Boom(self.link.x, self.link.y + 40, 8, 12, 1, "images/boomerang1.png"))
		if(self.link.linkU == True):
			self.sprites.append(Boom(self.link.x, self.link.y + 40, 8, 12, 2, "images/boomerang1.png"))
		if(self.link.linkD == True):
			self.sprites.append(Boom(self.link.x, self.link.y + 40, 8, 12, 3, "images/boomerang1.png"))

class View():
	def __init__(self, model):
		self.scroll_x = 0
		self.scroll_y = 0
		screen_size = (1000,500)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([102,3,252])
		for sprite in self.model.sprites:
			self.screen.blit(sprite.image, (sprite.x - self.scroll_x, sprite.y - self.scroll_y))
		pygame.display.flip()

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True

	def update(self):
		self.model.link.setPreviousPosition()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_q:
					self.keep_going = False
				if event.key == K_LCTRL:
					self.model.addBoom()
			elif event.type == pygame.MOUSEBUTTONUP:
				self.model.set_dest(pygame.mouse.get_pos())
		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.link.x -= 12
			self.model.link.updateImg(0)
		if keys[K_RIGHT]:
			self.model.link.x += 12
			self.model.link.updateImg(1)
		if keys[K_UP]:
			self.model.link.y -= 12
			self.model.link.updateImg(2)
		if keys[K_DOWN]:
			self.model.link.y += 12
			self.model.link.updateImg(3)

		if (self.model.link.x > 1000):
			self.view.scroll_x = 1000
		if (self.model.link.x < 1000):
			self.view.scroll_x = 0
		if (self.model.link.y > 500):
			self.view.scroll_y = 500
		if (self.model.link.y < 500):
			self.view.scroll_y = 0

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
pygame.mixer.init()

script_directory = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(script_directory, "greatfairyfountain.mp3")

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)


m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")
