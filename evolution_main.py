import pygame as pg
from pygame.locals import *
from creature import *
from matlab_plot import *
from food_supply import *
from button import *
import random
import time


def main():
	#--------------------------------------------------------------------------#
	#			Initiation and boundaries
	#--------------------------------------------------------------------------#
	# initiate pygame
	pg.init()
	default_font = init_font("Carlito-Regular.ttf", 40)
	display = [1500, 800]					# set display format
	window = pg.display.set_mode(display)	# start a pygame window
	pg.display.set_caption("Evolution")		# set window title
	global display_on 						# initiate the display variable
	display_on = True
	
	# define a change function (to be used by a button)
	def change_display_state():
		global display_on
		display_on = not display_on
	
	# divide the window into three parts: the buttons, the simulation and the graphs
	margin = 20
	button_bar_width = 300
	plot_width = 400
	plot_height = 400
	sim_width = display[0] - margin*2 - plot_width - button_bar_width
	sim_height = display[1] - margin*2
	sim_rect = pg.Rect(margin + button_bar_width, margin, sim_width, sim_height) 
	sim_surface = window.subsurface(sim_rect)
	background_color = (50, 50, 50)
	sim_surface.fill(background_color)
	
	#--------------------------------------------------------------------------#
	#			Creatures and food
	#--------------------------------------------------------------------------#
	# prepare creature list and define modify functions
	creatures = []
	initial_aging_speed = 0.001
	Creature.creature_list = creatures
	Creature.rect = sim_rect
	Creature.aging_speed = initial_aging_speed
	def add_creature():
		x = random.uniform(0, sim_rect.width)
		y = random.uniform(0, sim_rect.height)
		creatures.append(Creature(x, y))
	
	def halve_creatures():
		number_of_creatures = len(creatures)
		for i in range(int(number_of_creatures/2)):
			creatures[0].on_death()
			
	def remove_creatures():
		number_of_creatures = len(creatures)
		for i in range(int(number_of_creatures)):
			creatures[0].on_death()
	
	# Start food system
	initial_food_delay = 100 # in ticks
	initial_food_amount = 20
	food_supply = Food_supply(initial_food_delay, initial_food_amount, sim_rect)
	food_array = food_supply.food_array
	
	#--------------------------------------------------------------------------#
	#			Buttons
	#--------------------------------------------------------------------------#
	button_width = 250
	button_height = 40
	Increment_button.surface = window
	Increment_button.font = default_font
	Button.surface = window
	Button.font = default_font
	action_buttons = []
	
	# tick delay button
	button_rect = pg.Rect((button_bar_width - button_width)/2, 
						button_height*2, button_width, button_height)
	initial_tick_speed = 5
	min_tick_speed = 0
	max_tick_speed = 100
	tick_button = Increment_button(button_rect, "tick delay (ms)",
							initial_tick_speed, min_tick_speed, max_tick_speed)
	# food delay button
	button_rect = button_rect.move(0, button_height*2)
	min_food_delay = 10
	max_food_delay = 500
	fdelay_button = Increment_button(button_rect, "food delay (ticks)",
							initial_food_delay, min_food_delay, max_food_delay, 10)
	# food amount button
	button_rect = button_rect.move(0, button_height*2)
	min_food_amount = 0
	max_food_amount = 100
	famount_button = Increment_button(button_rect, "food amount",
							initial_food_amount, min_food_amount, max_food_amount)
	# aging speed button
	button_rect = button_rect.move(0, button_height*2)
	min_aging_speed = 0
	max_aging_speed = 0.1
	aging_button = Increment_button(button_rect, "aging speed",
							initial_aging_speed, min_aging_speed, max_aging_speed, 0.001)
	# spawn creature button
	button_rect = button_rect.move(0, button_height*2)
	action_buttons.append(Button(button_rect, "+1 creature", 
						add_creature))
	# halve creature button
	button_rect = button_rect.move(0, button_height*1.5)
	action_buttons.append(Button(button_rect, "1/2 creatures",
						halve_creatures))
	# remove creatures button
	button_rect = button_rect.move(0, button_height*1.5)
	action_buttons.append(Button(button_rect, "remove creatures",
						remove_creatures))
	# display state button
	button_rect = button_rect.move(0, button_height*1.5)
	action_buttons.append(Button(button_rect, "(un)freeze display", 
						change_display_state))
	
	#--------------------------------------------------------------------------#
	#			Graphs
	#--------------------------------------------------------------------------#
	# Define attribute graph boundary
	plot_rect = pg.Rect(display[0] - 400, 0, plot_width, plot_height)
	plot_surface = window.subsurface(plot_rect)
	plot_surface.fill((255,255,255))
	pg.display.update(plot_rect)
	
	# Start plot
	x_range = (0, Creature.max_speed)
	y_range = (0, Creature.max_sight)
	x_sc = []
	y_sc = []
	plot1 = Matlab_plot(x_sc, y_sc, plot_surface, plot_rect, x_range, y_range,
						"Creature attributes", "speed", "sight")
	
	def update_attributes_plot():
		x_sc.clear()
		y_sc.clear()
		for creature in creatures:
			x_sc.append(creature.speed)
			y_sc.append(creature.sight)
	
	# Define population graph boundary
	plot2_rect = pg.Rect(display[0] - 400, plot_height, plot_width, plot_height)
	plot2_surface = window.subsurface(plot2_rect)
	plot2_surface.fill((255,255,255))
	pg.display.update(plot2_rect)
	
	# Start plot
	population_history_size = 100
	x_range = (-population_history_size, 0)
	y_range = (0, Creature.max_creatures)
	ticks, population = [], []
	for i in range (population_history_size):
		ticks.append(-i)
		population.append(0)
	plot2 = Matlab_plot(ticks, population, plot2_surface, plot2_rect, 
					x_range, y_range, "Population", "plot history", "", True)
	
	def update_population_plot():
		population.pop()
		population.insert(0, len(creatures))
	
	#--------------------------------------------------------------------------#
	#			Simulation loop
	#--------------------------------------------------------------------------#
	# Set initial tick time
	dt = initial_tick_speed
	tick = 0
	tick_position = (margin, display[1] - margin)
	plot_refresh_time = 0.5
	plot_time_start = time.time() - plot_refresh_time  
	
	while True:
		click = False
		# Check for pygame events (only quit and click event is used)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				quit()
			if event.type == pg.MOUSEBUTTONDOWN:
				click = True
		
		# Progress food system
		food_supply.on_tick()
		
		# Creatures behaviour
		for creature in creatures:
			creature.on_tick(food_array)
		
		if display_on:
			# redraw the background
			sim_surface.fill(background_color)
			# draw the food
			for food in food_array:
				pg.draw.circle(sim_surface, food_supply.color, food.pos, food_supply.size)
			# draw the creatures
			for creature in creatures:
				pg.draw.circle(sim_surface, creature.color, (int(creature.x), int(creature.y)), creature.size)
			# Update displays
			pg.display.update(sim_rect)
		
		# wait for the tick delay duration
		pg.time.wait(dt)
		tick += 1
		
		# Display current tick count
		draw_text(window, "tick: " + str(tick), default_font, (255,255,255), tick_position)
		
		# Check buttons
		mouse = pg.mouse.get_pos()
		dt = tick_button.check_button_value(mouse, click)
		food_supply.interval = fdelay_button.check_button_value(mouse, click)
		food_supply.increase = famount_button.check_button_value(mouse, click)
		Creature.aging_speed = aging_button.check_button_value(mouse, click)
		for button in action_buttons:
			button.check_button(mouse, click)
		
		# Update plots
		if (time.time() - plot_time_start) > plot_refresh_time:
			update_attributes_plot()
			update_population_plot()
			plot1.update_plot()
			plot2.update_plot()
			plot_time_start = time.time()

def init_font(font_name, size):
	# initiate a pygame font
	font_path = pg.font.match_font(font_name,0,0)
	font = pg.font.Font(font_path, size)
	return font

def draw_text(surface, text, font, color, position):
	# draw some text on a pygame surface
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midleft = position
	text_rect = text_rect.inflate(10,10)
	pg.draw.rect(surface, (0,0,0), text_rect)
	surface.blit(text_surface, text_rect)
	pg.display.update(text_rect)

if __name__ == '__main__':
	main()


