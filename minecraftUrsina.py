#created by Tobie Rathbun

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

#loading textures
grass_texture	= load_texture('img/grass_block.png')
stone_texture	= load_texture('img/stone_block.png')
brick_texture	= load_texture('img/brick_block.png')
dirt_texture	= load_texture('img/dirt_block.png')
sky_texture		= load_texture('img/skybox.png')
arm_texture		= load_texture('img/arm_texture.png')
punch_sound	= Audio('img/punch_sound', loop = False, autoplay = False)

#hide fps counter
window.fps_counter.enabled = False
#hide exit button
window.exit_button.visible = False

block_pick = 1

def update():
	global block_pick
	
	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()
	
	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4


class Voxel(Button):
	#define a voxel to be placed
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'img/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
				#adds random colors for each block
			highlight_color = color.lime,
			scale = 0.5,
			)
	
	#listens to input
	def input(self,key):
		if self.hovered:
			#placing voxel cubes
			if key == 'left mouse down':
				punch_sound.play()
				if block_pick == 1:	#reads block pick
					voxel = Voxel(
						position = self.position + mouse.normal, 
						texture = grass_texture)	#assigns texture
				if block_pick == 2:
					voxel = Voxel(
						position = self.position + mouse.normal, 
						texture = stone_texture)
				if block_pick == 3:
					voxel = Voxel(
						position = self.position + mouse.normal, 
						texture = brick_texture)
				if block_pick == 4:
					voxel = Voxel(
						position = self.position + mouse.normal, 
						texture = dirt_texture)
			#deleting voxel cubes
			if key == 'right mouse down':
				punch_sound.play()
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True
			)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'img/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.6,-0.7)
			)
			
	def active(self):
		self.position = Vec2(0.5,-0.6)
		
	def passive(self):
		self.position = Vec2(0.6,-0.7)


for z in range(20):
	for x in range(20):
		voxel = Voxel((x,0,z))

player = FirstPersonController()

sky = Sky()
hand = Hand()

app.run()
