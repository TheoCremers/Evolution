import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pygame as pg

class Matlab_plot:
	dpi = 100 # 100 dots per inch
	
	def __init__(self, x_list, y_list, surface, rect, 
				x_range, y_range, title, x_label, y_label, line:bool = False):
		plt.style.use('dark_background')
		self.x_list = x_list
		self.y_list = y_list
		self.surface = surface
		self.rect = rect
		width = surface.get_width()
		height = surface.get_height()
		self.size = [width , height]
		f_size = [width / self.dpi, height / self.dpi]
		self.fig = plt.figure(figsize = f_size, dpi = self.dpi) # set graph size
		self.ax = plt.axes(xlim = x_range, ylim = y_range)      # define axes for plot
		self.ax.set_title(title)
		self.ax.set_xlabel(x_label)
		self.ax.set_ylabel(y_label)
		plot_type = "g-" if line else " ro"
		# start with an empty plot (comma required)
		self.plot, = self.ax.plot([], [], plot_type, ms = 5, mew = 0, alpha = 0.5) 
		# canvas draw() needs to be called once, to allow redraws
		self.fig.canvas.draw()
		# store the graph background
		self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
		self.renderer = self.fig.canvas.get_renderer()
		self.busy = False
	
	def get_raw_data(self):
		self.plot.set_data(self.x_list, self.y_list)    # set new data values
		self.fig.canvas.restore_region(self.background) # redraw background
		self.ax.draw_artist(self.plot)                  # redraw scatterplot data
		self.fig.canvas.blit(self.ax.bbox)              # blit the canvas
		raw_data = self.renderer.tostring_rgb()         # convert canvas to rgb_string
		return raw_data
	
	def update_plot(self):
		# if not already busy, use raw image data to draw the graph in pygame
		if not self.busy:
			self.busy = True
			raw_data = self.get_raw_data()
			surface = pg.image.fromstring(raw_data, self.size, "RGB")
			self.surface.blit(surface, (0,0))
			pg.display.update(self.rect)
			self.busy = False