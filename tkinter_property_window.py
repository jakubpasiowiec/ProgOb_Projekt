import tkinter as tk
import tkinter.ttk as ttk
import tkinter.colorchooser as cch
import tkinter.filedialog as fd
import tkinter.messagebox as msb
from collections import OrderedDict

class propertyRecord:
	def __init__(self, parent, y, width, height, name, value):
		print("name = {name}, value = {value}".format(name = name, value = value))
		
		self.property_name_var = tk.StringVar()
		self.property_name_var.set(name)
		self.property_name_wnd = tk.Entry(parent, background = "#aaaaaa", textvariable = self.property_name_var, state=tk.DISABLED)
		self.property_name_wnd.place(x = 0, y = y, relwidth = .5, in_ = parent, height = height)
		
		self.property_value_var = tk.StringVar()
		self.property_value_var.set(value)
		self.property_value_wnd = tk.Entry(parent, textvariable = self.property_value_var)
		self.property_value_wnd.place(relx = .5, y = y, height = height, relwidth = 0.5, in_ = parent)

class propertyWnd:
	def __init__(self, canvas, obj_id, parent = None):
		self.property_dict = canvas.itemconfig(obj_id)
		self.property_dict = OrderedDict(sorted(self.property_dict.items(), key = lambda t: t[0])) 
		self.canvas = canvas
		self.obj_id = obj_id
		self.window = tk.Toplevel(parent)
		self.window.grab_set()

		self.record = []

		i = 0
		height = 20
		width = 100

		for iproperty in self.property_dict.items():
			self.record += [propertyRecord(self.window, i * height, width, height, iproperty[0], iproperty[1][4])]
			i += 1

		self.window.geometry("{width}x{height}".format(height =  height * (i + 4), width = width * 2))
		
		self.tx_coords = tk.Text(self.window)
		self.tx_coords.place(x = 0, y = height * i, in_ = self.window, relwidth = 1., relheight = 1., height = - height * (i + 2))
		self.tx_coords.insert("end", self.canvas.coords(self.obj_id))
		
		self.bt_ok = tk.Button(self.window, text = "ok", command = self.on_ok_click)
		self.bt_ok.place(x = 0, in_ = self.window, relwidth = 1., y = - height * 2, rely = 1., height = height * 2)
		# self.window.mainloop()
	def on_ok_click(self):
		try:
			for item in self.record:
				self.canvas.itemconfig(self.obj_id, {item.property_name_var.get(): item.property_value_var.get()})
			coords = self.tx_coords.get(1.0, "end").strip().strip("[").strip("]").split(",")
			for i in range(len(coords)):
				coords[1] = coords[1].strip()
			self.canvas.coords(self.obj_id, tuple(coords))
		except:
			msb.showerror("Info", "Coś nie tak!")
		self.window.destroy()
# pr = propertyWnd({"a1": ("a1", 0, 0, 0, "tekst"), "a2": ("a1", 0, 0, 0, "tekst2")})
