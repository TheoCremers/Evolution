import random
import math

class Creature:
	# shared variables
	rect = [0, 0, 0, 0]
	creature_list = []
	max_creatures = 200
	min_speed = 0.1
	max_speed = 10
	min_sight = 0.1
	max_sight = 10
	min_energy = 0
	max_energy = 5000
	sight_to_radius = 20
	aging_speed = 0.001
	grow_time = 50
	
	def __init__(self, posx:float, posy:float, speed:float = 2, 
					sight:float = 2, generation:int = 0, 
					energy:float = max_energy * 0.5):
		# personal variables
		self.x = posx
		self.y = posy
		self.speed = speed
		self.speed_sq = speed**2
		self.sight = sight
		self.sight_sq = sight**2
		self.sight_radius_sq = (sight * self.sight_to_radius)**2
		self.generation = generation
		self.energy = energy
		self.size = 10
		self.age = 0
		self.grow_time_remaining = self.grow_time
		self.color = self.color_from_energy()
		self.target_acquired = False
		self.dis_to_target = self.max_sight * self.sight_to_radius
		self.target = None
		self.direction = [0.,0.]
		self.random_direction()
	
	def report(self):
		print(" This creature has speed: " + str(self.speed) 
		+ "\n and a sight of: " + str(self.sight)
		+ "\n and an energy count of: " + str(self.energy))
	
	def random_direction(self):
		angle = 2 * math.pi * random.random()
		self.direction = [math.sin(angle), math.cos(angle)]
	
	def on_tick(self, food_array):
		# check if the creature was just spawned and is still waiting
		if self.grow_time_remaining > 0:
			self.grow_time_remaining -= 1
		else:
			# check if food is in sight range
			self.check_sight(food_array)
			
			if self.target_acquired:
				# move towards food
				self.move_forward()
				self.dis_to_target -= self.speed
				# check if food is passed
				if self.dis_to_target < 0:
					self.eat_food()
			else:
				self.move_forward()
				
			# expend energy and change color/age
			self.change_energy(self.energy_per_tick())
			self.color = self.color_from_energy()
			self.age += self.aging_speed
	
	def eat_food(self):
		self.energy += self.target.supply.energy_per_food
		self.target.on_eaten()
	
	def change_target(self, new_target, distance):
		# remove old reference
		if self.target != None:
			self.target.targeted_by.remove(self)
		# add new reference
		new_target.targeted_by.append(self)
		# set new target
		self.target_acquired = True
		self.target = new_target
		self.dis_to_target = distance
		# change direction
		dx = new_target.pos[0] - self.x
		dy = new_target.pos[1] - self.y
		self.direction = [dx / distance, dy / distance]
	
	def lose_target(self):
		self.target_acquired = False
		self.target = None
		self.dis_to_target = self.max_sight * self.sight_to_radius
		self.random_direction()
		
	def move_forward(self):
		self.x += self.direction[0] * self.speed
		self.y += self.direction[1] * self.speed
		self.check_rect()
		
	def check_rect(self):
		 # check if creature is outside boundary and adjust position accordingly
		if self.x < 0:
			self.x += self.rect.width
		if self.x > self.rect.width:
			self.x -= self.rect.width
		if self.y < 0:
			self.y += self.rect.height
		if self.y > self.rect.height:
			self.y -= self.rect.height
	
	def change_energy(self, change):
		# change creature energy and trigger events if certain conditions are met
		self.energy = self.energy + change
		if self.energy < self.min_energy:
			self.on_death()
		if self.energy > self.max_energy:
			self.reproduce()
		# coerce value between min and max
		self.energy = max(min(self.energy, self.max_energy), self.min_energy)
	
	def energy_per_tick(self):
		total = -(self.speed_sq + self.sight + self.age)
		return total
	
	def check_sight(self, food_array):
		for food in food_array:
			if food != self.target:
				# check which food is closest
				dx = abs(food.pos[0] - self.x)
				dy = abs(food.pos[1] - self.y)
				sq_distance = dx**2 + dy**2
				if sq_distance < self.sight_radius_sq:
					distance = math.sqrt(sq_distance)
					if distance < self.dis_to_target:
						self.change_target(food, distance)
	
	def color_from_energy(self):
		return [self.energy / self.max_energy * 255, 0, 0]
	
	def on_death(self):
		# remove references to self in all other objects
		if self.target_acquired:
			self.target.targeted_by.remove(self)
		self.creature_list.remove(self)
	
	def reproduce(self):
		# create a new creature with slightly mutated speed and sight attributes
		self.creature_list.append(Creature(self.x, self.y, 
			speed = self.mutate(self.speed, self.min_speed, self.max_speed),
			sight = self.mutate(self.sight, self.min_sight, self.max_sight),
			generation = self.generation + 1,
			energy = self.energy * 0.5))
		# current energy is divided evenly between new and old creature
		self.energy *= 0.5
		# check if max number of creatures is not exceeded, otherwise, kill this one
		if len(self.creature_list) > self.max_creatures:
			self.on_death()
	
	def mutate(self, gene, min_val, max_val):
		# the current mutation formula uses a random gaussian distribution
		mutation = random.gauss(0, 0.2)
		mutated_gene = gene + mutation
		coerced_gene = max(min(mutated_gene, max_val), min_val)
		return coerced_gene
	
	def __del__(self): # this was used to test if creatures were properly removed
		pass