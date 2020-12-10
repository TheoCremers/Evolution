from random import randint

class Food_supply:
	def __init__(self, interval, increase, rect, max_food:int = 100, energy_per_food:float = 1000):
		self.interval = interval
		self.counter = interval
		self.increase = increase
		self.rect = rect
		self.size = 5
		self.color = [100, 255, 100]
		self.max_food = max_food
		self.food_array = []
		self.energy_per_food = energy_per_food
	
	def add_food(self, amount):
		# check that food count is not increase beyond the max
		current_food = len(self.food_array)
		if current_food + amount > self.max_food:
			amount = self.max_food - current_food
		# add the food to the array at random positions
		for i in range(0,amount):
			x = randint(0, self.rect.width)
			y = randint(0, self.rect.height)
			self.food_array.append(Food(x, y, self))
	
	def on_tick(self):
		# add food at intervals
		self.counter -= 1
		if self.counter <= 0:
			self.add_food(self.increase)
			self.counter = self.interval
			
class Food:
	def __init__(self, x, y, supply):
		self.pos = (x, y)
		self.targeted_by = []
		self.supply = supply
	
	def on_eaten(self):
		for creature in self.targeted_by:
			creature.lose_target()
		# Clear all references to and from this food
		self.targeted_by.clear()
		self.supply.food_array.remove(self)
		del(self.supply)
		
	def __del__(self):# this was used to test if food was properly removed
		pass