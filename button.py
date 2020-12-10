import pygame as pg

class Button:
	inactive_color = (100, 100, 100)
	active_color = (150, 150, 150)
	surface = None
	font = None
	
	def __init__(self, rect, title, action = None):
		self.rect = rect.copy()
		self.title = title
		self.action = action
		self.mouse_over = False
		self.draw_button()
	
	def check_button(self, mouse, click):
		# Check if mouse is over button
		if self.rect.collidepoint(mouse):
			if not self.mouse_over:
				self.mouse_over = True
				self.draw_button()
			if click:
				self.action()
		else:
			if self.mouse_over:
				self.mouse_over = False
				self.draw_button()
	
	def draw_button(self):
		# the button rectangle and the button text
		color = self.active_color if self.mouse_over else self.inactive_color
		pg.draw.rect(self.surface, color, self.rect)
		pg.display.update(self.rect)
		self.draw_button_text()
		
	def draw_button_text(self):
		self.draw_text(self.title, (0,0,0), (0,0))
	
	def draw_text(self, text, color, offset):
		# generalized function to update text for a pygame button
		text_surface = self.font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = [sum(x) for x in zip(self.rect.center, offset)]
		self.surface.blit(text_surface, text_rect)
		pg.display.update(text_rect)


class Increment_button(Button): # inherits from Button
	sign_offset = 20
	
	def __init__(self, rect, title, initial_val, min_val, max_val, increment:int = 1):
		self.value = initial_val
		self.min_val = min_val
		self.max_val = max_val
		self.increment = increment
		super().__init__(rect, title, self.change_value)
		# draw the increment button title above the button, in white
		self.draw_text(str(title), (255,255,255), (0,-self.rect.height))
	
	def check_button_value(self, mouse, click):
		super().check_button(mouse, click)
		return self.value
	
	def change_value(self):
		mouse = pg.mouse.get_pos()
		if mouse[0] <= self.rect.centerx:	# left side clicked
			self.value = max(self.value - self.increment, self.min_val)
		else: 								# right side clicked
			self.value = min(self.value + self.increment, self.max_val)
		self.draw_button()
	
	def draw_button_text(self):
		# the increment button has the value and a -/+ sign on its face
		if type(self.value) is int:
			self.draw_text(str(self.value), (0,0,0), (0,0))
		else:
			self.draw_text(str(round(self.value, 4)), (0,0,0), (0,0))
		self.draw_text('-', (0,0,0), (-self.rect.width/2 + self.sign_offset,0))
		self.draw_text('+', (0,0,0), (self.rect.width/2 - self.sign_offset,0))