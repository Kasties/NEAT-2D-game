import neat
import pygame
import neat
import os
import sys
import math
import pickle
frames = 2000
pygame.init()

screen_width = 1000
screen_height = 1000


clock = pygame.time.Clock()	
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Test')

tile_size = 50
generation = 0
lavas = []
fit = []

#load images
bg_img = pygame.image.load('C:/Users/xmakam27/Desktop/ai/gp/background.png')

class Player:
	x_pos = 130
	y_pos = 130
	jump = -15
	def __init__(self,x,y):

		img = pygame.image.load('C:/Users/xmakam27/Desktop/ai/gp/guy.png')
		self.image = pygame.transform.scale(img, (40, 80))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.up = True
		self.dead = 0

	def update(self):
		dx = 0
		dy = 0
		if self.dead == 0:
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			self.up = True
			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.up = False

			if pygame.sprite.spritecollide(self,slut_group,False):
				self.dead = 1	
				
			if pygame.sprite.spritecollide(self,lava_group,False):
				self.dead = -1


			

			self.rect.x += dx
			self.rect.y += dy

			screen.blit(self.image, self.rect)
			pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


	def is_alive(self):
		return self.dead
	def jumps(self):
		if self.jumped == False and self.up == False:
			self.vel_y = -15
			self.jumped = True
		elif self.jumped == True and self.up == False:
			self.jumped = False
			


class World:
	def __init__(self, data):
		self.tile_list = []
		dirt_img = pygame.image.load('C:/Users/xmakam27/Desktop/ai/gp/dirt.png')
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)

				if tile == 2:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)

				if tile == 3:
					slut = Slut(col_count * tile_size, row_count * tile_size)
					slut_group.add(slut)
					

				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('C:/Users/xmakam27/Desktop/ai/gp/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		if y != 75:
			lavas.append([x,y])


class Slut(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('C:/Users/xmakam27/Desktop/ai/gp/dirt.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2], 
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2], 
[2, 0, 0, 0, 1, 2, 2, 1, 2, 2, 1, 0, 1, 0, 2, 2, 2, 2, 2, 2], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


lava_group = pygame.sprite.Group()
slut_group = pygame.sprite.Group()
lava = Lava(1,1)
world = World(world_data)
player = Player(120,960)
slut = Slut(1,1)
def remove(index):
    players.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(player_pos,Slut):
	dy = (player_pos[1]+79)
	dx = (player_pos[0]+39)
	sluts = (math.sqrt((Slut[1]-dy)**2+(Slut[0]-dx)**2))
	# print(Slut[1])
	# pygame.draw.line(screen,(0,255,0),[dx,dy],(Slut[1],Slut[0]),1)
	# pygame.display.update()
	return sluts

def distance_lava(player_pos,lava):
	dy = (player_pos[1]+79)
	dx = (player_pos[0]+39)
	lava_kort = []
	for i in range(len(lava)):
		Lava = (math.sqrt((lava[i][1]-dy)**2+(lava[i][0]-dx)**2))
		lava_kort.append(Lava)
		#Visa vad den
	# 	pygame.draw.line(screen,(0,255,0),[dx,dy],lava[i],1)
	# pygame.display.update()
	return min(lava_kort)

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj

def save_best_generation_instance(instance, filename='trained/best_generation_instances.pickle'):
    instances = []
    if os.path.isfile(filename):
        instances = load_object(filename)
    instances.append(instance)
    save_object(instances, filename)


def main(genome,config):
	global obstacles ,players ,ge ,nets
	clock = pygame.time.Clock()
	obstacles = []
	players = []
	ge = []
	nets = []
	count_frames = 0

	for id,g in genome:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		players.append(Player(130,920))
		ge.append(g)
		nets.append(net)
		g.fitness = 0
		
	screen = pygame.display.set_mode((screen_width, screen_height))
	
	run = True
	while run:
		count_frames += 1
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("Quittin")
				save_object(pop, "C:/Users/xmakam27/Desktop/ai/gp/trained/population.dat")  ## export population
				pygame.quit()
				sys.exit()
		if len(players) == 0:
			break
		for i, player in enumerate(players):

			if player.is_alive() == -1:
				ge[i].fitness -= abs(distance((player.rect.x,player.rect.y),(slut.rect.x,slut.rect.y)))
				fit.append(ge[i].fitness)
				remove(i)

			elif count_frames > 1000:
				ge[i].fitness -= abs(distance((player.rect.x,player.rect.y),(slut.rect.x,slut.rect.y)))*2
				fit.append(ge[i].fitness)
				remove(i)

			elif player.is_alive() == 1:
				ge[i].fitness += abs(distance((player.rect.x,player.rect.y),(slut.rect.x,slut.rect.y)))
				fit.append(ge[i].fitness)
				save_object(pop, "C:/Users/xmakam27/Desktop/ai/gp/trained/population.dat")
				pygame.quit()
				sys.exit()
		for i, player in enumerate(players):
			output = nets[players.index(player)].activate((player.rect.x,player.rect.y,(distance((player.rect.x,player.rect.y),(slut.rect.x,slut.rect.y))),distance_lava((player.rect.x,player.rect.y),lavas)))
			if output[0] > 0.2:
				pass
				# player.rect.x += 4.5
			if output[1] > 0.2:
				pass
					# player.jumps()
			if output[2] > 0.2:
				pass
				# player.rect.x -= 4.5

		clock.tick(frames)
		screen.blit(bg_img, (0, 0))
		# screen.blit(sun_img, (100, 100))

		world.draw()
		lava_group.draw(screen)
		slut_group.draw(screen)
		for player in players:
			player.update()	
		
		pygame.display.update()

def run(config_path):
	global pop
	config = neat.config.Config(
		neat.DefaultGenome,
		neat.DefaultReproduction,
		neat.DefaultSpeciesSet,
		neat.DefaultStagnation,
		config_path
	)
	pop = neat.Population(config)

	pop.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	pop.add_reporter(stats)
	pop.run(main, 2)
if __name__ == '__main__':
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'C:/Users/xmakam27/Desktop/ai/gp/neat.txt')
	run(config_path)