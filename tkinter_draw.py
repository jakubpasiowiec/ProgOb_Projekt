###########################################################
# PROJEKT:			PROGRAMOWANIE OBIEKTOWE
# ZESPOL NR:		Z06
# 					-Jakub Pasiowiec
# 					-Grzegorz Majewski
# 					-Paweł Gąciarz
# 					-Konrad Janowski
# TEMAT PROJEKTU:	2 - Prosty edytor grafiki wektorowej
###########################################################

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser as cch
import tkinter.filedialog as fd
import tkinter.messagebox as msb
import tkinter_property_window as pw

################################################################################
# function strToDict ###########################################################
################################################################################
def strToDict(string):
	"""
	This function change string to a dictionary. String must be in form:
	key1="value1";key2="value2"
	example:
	string = 'key1="value1";key2="value2"'
	dictionary = strToDict(string) <- this retur dictionary
	{key1: "value1", key2: "value2"}
	"""
	strList = string.split("\";")
	dictionary = {}
	for item in strList:
		l = item.split("=\"", 1)
		dictionary[l[0]] = l[1].strip('\n').strip('"')
	return dictionary
################################################################################
# DrawingObject class ##########################################################
################################################################################
class DrawingObject:
	def __init__(self, id, canvas, object_tree, typename):
		"""
		Each drawing object class like a Ellipse or Rectangle etc. must have
		this class as a parent. Constructor of this class get two parameters
		id - id of canvas object
		canvas - Canvas class object
		object_tree - Treeobject widtget to show info about object
		"""
		self.id = id
		self.canvas = canvas
		self.object_tree = object_tree
		self.object_tree.insert("Obiekty", "end", str(self.id), text = str(self.id))
		self._typename = typename
	def remove(self):
		self.canvas.delete(self.id)
	def __eq__(self, other):
		return other == self.id
	def __del__(self):
		try:
			self.object_tree.delete(str(self.id))
			self.canvas.delete(self.id)
		except:
			pass
	def __str__(self):
		coords = self.canvas.coords(self.id)
		str_coords = ""
		for i in coords:
			str_coords += "{i},".format(i = i)
		str_coords = str_coords.strip(",")
		config = self.canvas.itemconfig(self.id)
		str_config = ""
		for item in config.items():
			str_config += "{name}=\"{value}\";".format(name = item[0], value = item[1][4])
		str_config = str_config.strip(";")
		return "type=\"{typename}\";coords=\"{coords}\";{config}".format(typename = self._typename, coords = str_coords, config = str_config)
	def setCoords(self, coords):
		try:
			self.canvas.coords(self.id, tuple(coords))
			return True
		except:
			return False
	def toSvg(self):
		config = self.canvas.itemconfig(self.id)
		style = "style = \""
		if "outline" in config:
			style += "fill:{fill};stroke:{stroke}".format(fill = config["fill"][4] if len(config["fill"][4]) else "none", stroke = config["outline"][4] if len(config["outline"][4]) else "none")
		else:
			style += "fill:none;stroke:{fill}".format(fill = config["fill"][4] if len(config["fill"][4]) else "none")
		style += ";stroke-width:{width}".format(width = config["width"][4])
		style += ";stroke-linejoin:{joinstyle}".format(joinstyle = config["joinstyle"][4])
		capstyle = {"butt": "butt", "projecting": "square", "round": "round"}
		if config["capstyle"][4] in capstyle:
			style += ";stroke-linecap:{capstyle}".format(capstyle = config["capstyle"][4])
		style += "\""
		if len(config["dash"][4]):
			dashArray = config["dash"][4].replace(" ", ",")
			style += " stroke-dasharray = \"{dashArray}\"".format(dashArray = dashArray)
		return style
	@staticmethod
	def GetCoords(dictionary):
		coords = dictionary["coords"].strip(",").split(",")
		print(coords)
		if len(coords) == 0 or len(coords) % 2:
			return None
		for i in range(len(coords)):
			coords[i] = float(coords[i])
		return coords
################################################################################
# Rectangle class ##############################################################
################################################################################
class Rectangle(DrawingObject):
	command = ["Rectangle", "rectangle", "Prostokąt", "prostokąt"]
	def __init__(self, coords, canvas, object_tree, **kwargs):
		"""
		Rectangle calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Rectnagle(coords, canvas, fill, outline, width)
		coordinate arguments:
		coords - list or tuple of rectangle coordinate
		Canvas:
		canvas - object of class Canvas widget
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_rectangle(coords, kwargs), canvas, object_tree, "Rectangle")
		self.x = coords[0]
		self.y = coords[1]
		self.object_tree.item(str(self.id),text = "Prostokąt {id}".format(id = self.id))
	def setEnd(self, x2, y2):
		width = x2 - self.x
		height = y2 - self.y
		self.canvas.coords(self.id, min(x2, self.x), min(y2, self.y), max(x2, self.x), max(y2, self.y))
	def toSvg(self):
		coords = self.canvas.coords(self.id)
		points = points.strip()
		return "<polygon x = \"{x}\" y = \"{y}\" width = \"{width}\" height = \"{height}\" {style}/>".format(x = coords[0], y = coords[1], width = coords[0] - coords[2], height = coords[1] - coords[3],  style = DrawingObject.toSvg(self))
	@staticmethod
	def GetObject(dictionary, canvas, object_tree, setvar = None):
		if dictionary["type"] in Rectangle.command:
			if not (setvar is None):
				setvar.set(Rectangle.command[0])
			coords = DrawingObject.GetCoords(dictionary)
			del(dictionary["coords"])
			del(dictionary["type"])
			return Rectangle(coords, canvas, object_tree, **dictionary)
		return None
################################################################################
# Ellipse class ################################################################
################################################################################
class Ellipse(DrawingObject):
	command = ["Ellipse", "ellipse", "Elipsa", "elipsa"]
	def __init__(self, coords, canvas, object_tree, **kwargs):
		"""
		Ellipse calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Ellipse(coords, canvas, fill, outline, width)
		coordinate arguments:
		coords - tuple or list of coordinate
		Canvas:
		canvas - object of Canvas class
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_oval(coords, kwargs), canvas, object_tree, "Ellipse")
		self.object_tree.item(str(self.id),text = "Elipsa {id}".format(id = self.id))
	def center(self):
		coords = self.canvas.coords(self.id)
		return ((coords[2] - coords[0]) * .5 + coords[0], (coords[1] - coords[3]) * .5 + coords[3])
	def rays(self, center, x2, y2):
		rx = center[0] - x2
		rx = -rx if rx < 0 else rx;
		ry = center[1] - y2
		ry = -ry if ry < 0 else ry;
		print("rx = {rx}, ry = {ry}".format(rx = rx, ry = ry))
		return ( rx , ry )
	def setEnd(self, x2, y2):
		center = self.center()
		rays = self.rays(center, x2, y2)
		self.canvas.coords(self.id, center[0] - rays[0], center[1] - rays[1], center[0] + rays[0], center[1] + rays[1])
	def toSvg(self):
		coords = self.canvas.coords(self.id)
		points = points.strip()
		return "<polygon cx = \"{cx}\" cy = \"{cy}\" rx = \"{rx}\" ry = \"{ry}\" {style}/>".format(cx = (coords[0] + coords[2]) / 2, cy = (coords[1] + coords[3]) / 2, rx = abs((coords[0] - coords[2]) / 2), ry = abs((coords[1] - coords[3]) / 2),  style = DrawingObject.toSvg(self))
	@staticmethod
	def GetObject(dictionary, canvas, object_tree, setvar = None):
		if dictionary["type"] in Ellipse.command:
			if not (setvar is None):
				setvar.set(Ellipse.command[0])
			coords = DrawingObject.GetCoords(dictionary)
			del(dictionary["coords"])
			del(dictionary["type"])
			return Ellipse(coords, canvas, object_tree, **dictionary)
		return None
################################################################################
# Line class ###################################################################
################################################################################
class Line(DrawingObject):
	command = ["Line", "line", "Linia", "linia"]
	def __init__(self, coords, canvas, object_tree, **kwargs):
		"""
		Line calss need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Line(coords, canvas, outline, width)
		coordinate arguments:
		coords - coordineto of line points (tuple or list)
		Canvas:
		canvas - class object of Canvas widget
		other settings:
		fill - color of line, example "#ff0000" <- red color
		width - size of line (in px)
		"""
		DrawingObject.__init__(self, canvas.create_line(coords, kwargs), canvas, object_tree, "Line")# dash=(20,5) )
		self.object_tree.item(str(self.id),text = "Linia {id}".format(id = self.id))
	def setEnd(self, x2, y2):
		coords = self.canvas.coords(self.id)
		self.canvas.coords(self.id, coords[0], coords[1], x2, y2)
	def toSvg(self):
		points = ""
		coords = self.canvas.coords(self.id)
		for i in range(len(coords) // 2):
			points += " {x},{y}".format(x = coords[i * 2], y = coords[i * 2 + 1])
		points = points.strip()
		return "<polyline points = \"{points}\" {style}/>".format(points = points, style = DrawingObject.toSvg(self))
	@staticmethod
	def GetObject(dictionary, canvas, object_tree, setvar = None):
		if dictionary["type"] in Line.command:
			if not (setvar is None):
				setvar.set(Line.command[0])
			coords = DrawingObject.GetCoords(dictionary)
			del(dictionary["coords"])
			del(dictionary["type"])
			if "outline" in dictionary:
				dictionary["fill"] = dictionary["outline"]
				del(dictionary["outline"])
			return Line(coords, canvas, object_tree, **dictionary)
		return None
################################################################################
# Polygon class ################################################################
################################################################################
class Polygon(DrawingObject):
	command = ["Polygon", "polygon", "Wielokąt", "wielokąt"]
	def __init__(self, coords, canvas, object_tree, **kwargs):
		"""
		Polygon class need to story information about object and set or get some
		info about them. Constructor get few important arguments:
		Polygon(coords, canvas, outline, fill, width)
		coordinate arguments:
		coords - tuple or list of points [1, 3, 10, 5, 8, 6]
		Canvas:
		canvas - object of class Canvas
		other settings:
		fill - color of fill example "#ff0000" <- red color
		outline - color of border line
		width - size of border line (in px)
		"""
		print(coords)
		DrawingObject.__init__(self, canvas.create_polygon(coords, kwargs), canvas, object_tree, "Polygon")
		self.object_tree.item(str(self.id),text = "Wielokąt {id}".format(id = self.id))
	def setEnd(self, x2, y2):
		coords = self.canvas.coords(self.id)
		coords += x2, y2
		self.canvas.coords(self.id, tuple(coords))
	def toSvg(self):
		points = ""
		coords = self.canvas.coords(self.id)
		for i in range(len(coords) // 2):
			points += " {x},{y}".format(x = coords[i * 2], y = coords[i * 2 + 1])
		points = points.strip()
		return "<polygon points = \"{points}\" {style}/>".format(points = points, style = DrawingObject.toSvg(self))

	def GetObject(dictionary, canvas, object_tree, setvar = None):
		if dictionary["type"] in Polygon.command:
			if not (setvar is None):
				setvar.set(Polygon.command[0])
			coords = DrawingObject.GetCoords(dictionary)
			del(dictionary["coords"])
			del(dictionary["type"])
			print(dictionary)
			return Polygon(coords, canvas, object_tree, **dictionary)
		return None
################################################################################
# Toolbar class ################################################################
################################################################################
class Toolbar(tk.Frame):
	def __init__(self, parent):
		"""
		Create toolbar control witch have inside togle buttons to control action of
		program
		Toolbar(parent)
		arguments:
		parent - parent widget.
		"""
		self.button_size = 25
		
		tk.Frame.__init__(self, parent)
		tk.Frame.place(self, in_ = parent, x = 0, y = 0, relwidth = 1., height = self.button_size)
		
		self.valueset = tk.StringVar()
		self.images = []
		
		self.buttons = []
	def add_button(self, title, image = ""):
		
		if len(self.buttons) == 0:
			self.valueset.set(title)
		button = tk.Radiobutton(self, text = title, indicatoron = 0, variable = self.valueset, value = title)
		button.place(x = self.button_size * len(self.buttons), y = 0, width = self.button_size, relheight = 1.)
		self.buttons.extend([button])
		if len(image):
			self.images += [tk.PhotoImage(file = image)]
			button.config(image = self.images[-1])
	def set_on_buttons_change(self, fu):
		self.valueset.trace("w", fu)
	@property
	def height(self):
		return self.button_size
	@property
	def getvalueset(self):
		return self.valueset.get()
################################################################################
# Application class ############################################################
################################################################################
class Application:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Prosty edytor grafiki wektorowej")
		self.window.geometry("800x400")
	
		########################################################################
		# MENU #################################################################
		########################################################################
		
		self.menu = tk.Menu(self.window)
		
		menu_file = tk.Menu(self.menu, tearoff = 0)
		menu_file.add_command(label = "Zapisz", command = self.menu_save_to_file)
		menu_file.add_command(label = "Otwórz", command = self.menu_open_file)
		menu_file.add_command(label = "Eksportuj do svg", command = self.menu_export_to_svg)
		
		self.menu.add_cascade(label = "Plik", menu = menu_file)
		
		self.window.config(menu = self.menu)
		
		########################################################################
		# END MENU #############################################################
		########################################################################
		
		########################################################################
		# TOOLBAR ##############################################################
		########################################################################
		
		self.toolbar = Toolbar(self.window)
		self.toolbar.add_button("Line", image = "buttons/line.gif")
		self.toolbar.add_button("Ellipse", image = "buttons/ellipse.gif")
		self.toolbar.add_button("Rectangle", image = "buttons/rectangle.gif")
		self.toolbar.add_button("Polygon", image = "buttons/polygon.gif")
		self.toolbar.add_button("M", image = "buttons/select.gif")
		self.toolbar.place(x = self.toolbar.height * 4)
		
		self.fillcolor = "#ffffff"
		self.fillcolorbutton = tk.Button(self.window, background = self.fillcolor, command = self.on_color_fill)
		self.fillcolorbutton.place(in_ = self.window, x = self.toolbar.height * 2, y = 0, width = self.toolbar.height, height = self.toolbar.height)
		
		self.strokecolor = "#000000"
		self.strokecolorbutton = tk.Button(self.window, background = self.strokecolor, command = self.on_color_stroke)
		self.strokecolorbutton.place(in_ = self.window, x = self.toolbar.height * 3, y = 0, width = self.toolbar.height, height = self.toolbar.height)
		
		self.strokewidth = tk.IntVar()
		self.strokewidth.set(1)
		self.strokewidthspin = tk.Spinbox(self.window, from_ = 0, to = 10, textvariable = self.strokewidth, command = self.on_width_changed)
		self.strokewidthspin.place(in_ = self.window, x = 0, y = 0, width = self.toolbar.height * 2, height = self.toolbar.height)
		
		########################################################################
		# END TOOLBAR ##########################################################
		########################################################################
		
		self.canvas = tk.Canvas(self.window, background = "#ffffff", cursor = "tcross")
		self.canvas.place(x = 250, y = self.toolbar.height, relwidth = 1., relheight = 1., height = - self.toolbar.height - 100, width = -250)
		
		self.object_tree = ttk.Treeview(self.window)
		self.object_tree.place(x = 0, y = self.toolbar.height, width = 250, relheight = 1., height = - self.toolbar.height * 2)
		self.object_tree.bind("<Double-Button-1>", self.on_double_click_object_tree)
		
		self.object_tree.insert("", "end", "Obiekty", text = "Obiekty")
		
		self.mouse_position_on_canvas = tk.StringVar()
		self.lb_mouse_position_on_canvas = tk.Label(self.window, textvariable = self.mouse_position_on_canvas)
		self.lb_mouse_position_on_canvas.place( x = 5, y = -25, rely = 1.)
		
		self.draw_object = []
		
		self.selected = None
		
		self.lastpoint = [0,0]
		self.addObject = False
		
		self.mousepointclicked = [0,0]
		self.coords = []
		
		self.canvas.bind("<B1-Motion>", self.on_mousemoveb1)
		self.canvas.bind("<Motion>", self.on_mousemove)
		self.canvas.bind("<Button-1>", self.on_lbc)
		self.canvas.bind("<ButtonRelease-1>", self.on_lbr)
		self.canvas.bind("<Double-Button-1>", self.on_double_canvas_click)
		self.canvas.bind("<Return>", self.on_return_canvas_click)
		
		self.canvas.bind("<Button-3>", self.on_rbc)
		self.canvas.bind("<Delete>", self.on_delete)
		
		self.toolbar.set_on_buttons_change(self.on_toolbar_mode_changed)
		
		self.commandlinevar = tk.StringVar()
		self.commandline = tk.Entry(self.window, textvariable = self.commandlinevar)
		self.commandline.place(x = 250, y = - 50, rely = 1., in_ = self.window, relwidth = 1., width = - 250, height = 25)
		self.commandline.bind("<Return>", self.on_return_commandline_click)
		
		self.commandhistory = tk.Text(self.window)
		self.commandhistory.place(in_ = self.window, x = 250, y = - 100, rely = 1., width = -250, relwidth = 1., height = 50)
		
		self.drConstructors = [Rectangle.GetObject, Ellipse.GetObject, Line.GetObject, Polygon.GetObject]
		
		self.window.mainloop()
	def on_mousemoveb1(self, event):
		if self.toolbar.getvalueset == "M":
			self.canvas.move(self.selected, event.x - self.mousepointclicked[0],event.y - self.mousepointclicked[1])
			self.mousepointclicked = [event.x, event.y]
	def on_mousemove(self, event):
		self.mouse_position_on_canvas.set("x = {x}, y = {y}".format(x = event.x, y = event.y))
		if self.addObject:
			if self.toolbar.getvalueset == "Rectangle" or self.toolbar.getvalueset == "Ellipse" or self.toolbar.getvalueset == "Line" or self.toolbar.getvalueset == "Polygon":
				self.draw_object[-1].setCoords(self.coords + [event.x, event.y])
	def on_return_canvas_click(self, event):
		self.commandlinevar.set("")
		self.on_return_commandline_click(event)
		#self.addObject = False
		#if self.toolbar.getvalueset == "Rectangle" or self.toolbar.getvalueset == "Ellipse":
		#	if len(self.coords) != 4:
		#		del(self.draw_object[-1])
		#	else:
		#		self.draw_object[-1].setCoords(self.coords)
		#	self.coords = []
		#elif self.toolbar.getvalueset == "Line" or self.toolbar.getvalueset == "Polygon":
		#	if len(self.coords) < 4:
		#		del(self.draw_object[-1])
		#	else:
		#		self.draw_object[-1].setCoords(self.coords)
		#	self.coords = []
	def on_return_commandline_click(self, event):
		self.commandhistory.insert("end", "\n" + self.commandline.get() if self.commandhistory.get(1., "end") != "\n" else self.commandline.get())
		self.commandhistory.see("end")
		if self.addObject == False:
			command = self.commandlinevar.get()
			if len(command):
				coords = command.split(" ")
				if len(coords) > 0:
					command = coords[0]
					if len(coords) > 1 and len(coords) % 2 == 1:
						coordst = coords[1:]
						globalpt = True
						if coordst[0].find("@") > -1:
							print("global")
							globalpt = False
							coordst[0] = coordst[0][1:]
						coords = ""
						self.coords = []
						i = 0
						for coord in coordst:
							if globalpt:
								self.coords += [float(coord)]
								coords += ",{0}".format(coord)
								self.lastpoint[i % 2] = self.coords[-1]
							else:
								self.coords += [float(coord) + self.lastpoint[i % 2]]
								coords += ",{0}".format(float(coord) + self.lastpoint[i % 2])
								self.lastpoint[i % 2] = self.coords[-1]
							i += 1
						print(self.coords)
					if len(self.coords) == 0:
						coords = "{0},{1}".format(self.lastpoint[0], self.lastpoint[1])
						coords += ",{0},{1}".format(self.lastpoint[0], self.lastpoint[1])
					elif len(self.coords) == 2:
						coords += ",{0},{1}".format(self.lastpoint[0], self.lastpoint[1])
					coords = coords.strip(",")
					dictionary = {"type": command, "coords": coords, "fill": self.fillcolor, "outline": self.strokecolor, "width": self.strokewidth.get()}
					for constructor in self.drConstructors:
						obj = constructor(dictionary, self.canvas, self.object_tree, self.toolbar.valueset)
						if not (obj is None):
							self.draw_object += [obj]
							self.commandlinevar.set("")
							self.addObject = True
							break;
					print("c2={0}".format(self.coords))
					if self.addObject == False:
						self.coords = []
						self.commandhistory.insert("end","\nBłąd podczas wstawiania elementu!")
		else:
			coords = self.commandline.get().split(" ")
			self.commandlinevar.set("")
			if coords[0] == "c" and len(self.coords) > 1:
				if len(self.coords) > 2:
					self.lastpoint = self.coords[-4:-2]
				else:
					self.lastpoint = [0, 0]
				self.coords = self.coords[:-2]
				if len(self.coords) == 2:
					self.draw_object[-1].setCoords(self.coords + self.lastpoint)
				else:
					self.addObject = self.draw_object[-1].setCoords(self.coords)
			elif len(coords) > 1 and len(coords) % 2 == 0:
				globalpt = True
				if coords[0].find("@") > -1:
					globalpt = False
					coords[0] = coords[0][1:]
				print(coords)
				i = 0
				for coord in coords:
					if globalpt:
						self.coords += [float(coord)]
					else:
						self.coords += [float(coord) + self.lastpoint[i % 2]]						
					self.lastpoint[i % 2] = self.coords[-1]
					i += 1
				print(self.coords)
				if len(self.coords) % 2 == 0:
					if len(self.coords) == 2:
						self.draw_object[-1].setCoords(self.coords + self.lastpoint)
					else:
						self.addObject = self.draw_object[-1].setCoords(self.coords)
			else:
				if len(self.coords) < 4:
					del(self.draw_object[-1])
				else:
					self.draw_object[-1].setCoords(self.coords)
				self.coords = []
				self.addObject = False
		
	def on_toolbar_mode_changed(self, *args):
		#if self.addObject:
		#	del(self.draw_object[-1])
		self.addObject = False
		#self.coords = []
	def on_lbc(self, event):
		self.canvas.focus_set()
		
		if not self.addObject:
			if self.toolbar.getvalueset == "M":
				self.addObject = False
			else:
				self.lastpoint = [event.x, event.y]
			self.coords = [event.x, event.y]
			if self.toolbar.getvalueset == "Rectangle":
				self.commandlinevar.set("Rectangle {0} {1}".format(event.x, event.y))
				self.on_return_commandline_click(event)
			elif self.toolbar.getvalueset == "Ellipse":
				self.commandlinevar.set("Ellipse {0} {1}".format(event.x, event.y))
				self.on_return_commandline_click(event)
			elif self.toolbar.getvalueset == "Line":
				self.commandlinevar.set("Line {0} {1}".format(event.x, event.y))
				self.on_return_commandline_click(event)
			elif self.toolbar.getvalueset == "Polygon":
				self.commandlinevar.set("Polygon {0} {1}".format(event.x, event.y))
				self.on_return_commandline_click(event)
		else:
			if self.toolbar.getvalueset != "M":
				print("{0} {1}".format(event.x, event.y))
				self.commandlinevar.set("{0} {1}".format(event.x, event.y))
				self.on_return_commandline_click(event)
				if self.toolbar.getvalueset in ["Rectangle", "Ellipse"]:
					self.commandlinevar.set("")
					self.on_return_commandline_click(event)
				#self.lastpoint = [event.x, event.y]
		
		if self.toolbar.getvalueset == "M":
			self.selected = self.canvas.find_closest(event.x, event.y)
			if self.selected:
				config = self.canvas.itemconfig(self.selected)
				self.object_tree.selection() 	# "set", str(self.selected[0])
				self.strokewidth.set(int(float(config["width"][4])))
				
				if "outline" in config:
					self.strokecolor = config["outline"][4]
					if config["outline"][4]:
						self.strokecolorbutton.config(background = self.strokecolor)
					else:
						self.strokecolorbutton.config(background = "#aaaaaa", text = "x")
					self.fillcolor = config["fill"][4]
					if config["fill"][4]:
						self.fillcolorbutton.config(background = self.fillcolor, text = "")
					else:
						self.fillcolorbutton.config(background = "#aaaaaa", text = "x")
				else:
					self.strokecolor = config["fill"][4]
					if config["fill"][4]:
						self.strokecolorbutton.config(background = config["fill"][4], text = "")
					else:
						self.strokecolorbutton.config(background = "#aaaaaa", text = "x")
		self.mousepointclicked = [event.x, event.y]
	def on_double_click_object_tree(self, event):
		selected = self.object_tree.selection()
		if len(selected) == 1:
			if selected[0].isnumeric():# msb.showinfo("Info", "{selected}".format(selected = self.canvas.coords(int(selected[0]))))
				pw.propertyWnd(self.canvas, int(selected[0]), self.window)
	def on_double_canvas_click(self, event):
		if self.toolbar.getvalueset == "M":
			current = self.canvas.find_withtag(tk.CURRENT)
			if current:
				pw.propertyWnd(self.canvas, current[0], self.window)
	def on_lbr(self, event):
		pass
	def on_color_fill(self):
		fc = cch.askcolor()[1]
		self.fillcolor = fc if fc else self.fillcolor
		self.fillcolorbutton.config(background = self.fillcolor, text = "")
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, fill = fc)
	def on_color_stroke(self):
		fc = cch.askcolor()[1]
		self.strokecolor = fc if fc else self.strokecolor
		self.strokecolorbutton.config(background = self.strokecolor, text = "")
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, outline = fc)
	def on_rbc(self, events):
		if len(self.draw_object):
			self.addObject = False
			self.coords = []
			print(str(self.draw_object[-1]))
			self.draw_object[-1].remove()
			del(self.draw_object[-1])
	def on_width_changed(self):
		if self.toolbar.getvalueset == "M" and self.selected != None:
			self.canvas.itemconfig(self.selected, width = self.strokewidth.get())
	def on_delete(self, event):
		if self.toolbar.getvalueset == "M" and self.selected != None:
			for i in self.draw_object:
				if i.id == self.selected[0]:
					self.draw_object.remove(i)
			self.canvas.delete(self.selected)
			
	# for menu methods		
	def menu_save_to_file(self):
		if len(self.draw_object):
			filename = fd.asksaveasfilename(filetypes=[("Plik tekstowy","*.txt")], defaultextension = "*.txt")
			
			if filename:
				newfile = open(filename, "w", -1, "utf-8")
				for i in range(len(self.draw_object)):
					newfile.write(str(self.draw_object[i]))
					if i < len(self.draw_object) - 1:
						newfile.write("\n")
				newfile.close()
	def menu_open_file(self):
		if len(self.draw_object) and msb.askyesno("Powiadomienie", "Czy chcesz zapisać bierzące dane do pliku?"):
			self.menu_save_to_file()
		filename = fd.askopenfilename(filetypes=[("Plik tekstowy","*.txt")], defaultextension = "*.txt")
		
		if filename:
			self.draw_object.clear()
			self.canvas.delete(tk.ALL)
			with open(filename, "r", -1, "utf-8") as openfile:
				lines = openfile.readlines()
				for line in lines:
					dictObj = strToDict(line)
					for constructor in self.drConstructors:
						newobject = constructor(dictObj, self.canvas, self.object_tree)
						if newobject != None:
							self.draw_object += [newobject]
							break
	def menu_export_to_svg(self):
		if len(self.draw_object):
			filename = fd.asksaveasfilename(filetypes=[("Plik svg","*.svg")], defaultextension = "*.svg")
			
			if filename:
				svgfile = open(filename, "w", -1, "utf-8")
				svgfile.write("<svg width = \"2100\" height = \"2970\">\n")
				for i in range(len(self.draw_object)):
					svgfile.write("{0}\n".format(self.draw_object[i].toSvg()))
				svgfile.write("</svg>")
				svgfile.close()

apl = Application()
