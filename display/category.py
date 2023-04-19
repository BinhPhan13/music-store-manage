from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import font
from project_code.entity_manager import *
from page import Page

class Categories(Page):
	def __init__(self, main_frame:ttk.Frame, song_mng:SongManager):
		super().__init__(main_frame)
		self.__ref = song_mng

	def _init_frame(self):
		# change default font
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=14)

		# left frame
		category_txt = ttk.Label(text = "Categories", font=default_font)
		self.__left_frame = ttk.LabelFrame(self._frame, relief=RIDGE, borderwidth=1,
				  						labelwidget=category_txt,bootstyle='primary')
		self.__left_frame.place(x=25, y=53, width=210, height=500)

		self.__create_category_table()
		ttk.Button(self._frame, text="Show", bootstyle="success", cursor="hand2", 
	     			command=self.__show_song).place(x=25, y=573, width=210, height=35)
		
		# Song label frame
		ttk.Label(self._frame,text="Song's Details", font=(self._font,16),
	    		bootstyle = "secondary inverse",anchor = CENTER).place(x=275,y=15,width=800,height=38)
		
		# right frame
		ttk.Label(text = "Songs", font=default_font)
		self.__right_frame = ttk.Frame(self._frame)
		self.__right_frame.place(x=273,y=65,width=800,height=545)

		self.__create_song_table()
	

	def __create_category_table(self):
		col = ["Category"]
		width = [100]
		category_table = ttk.Treeview(self.__left_frame, columns=col, style='info.Treeview', selectmode='extended')

		# scroll bars
		scroll_y = ttk.Scrollbar(category_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=category_table.yview)

		# avoid resize column
		category_table.bind("<Button-1>", lambda event: "break" \
		      				if category_table.identify_region(event.x, event.y) == "separator" else "")
		
		category_table.column('#0', width=0, stretch=NO)
		for c, w in zip(col, width):
			category_table.column(c, width=w, anchor=CENTER)
			category_table.heading(c, text=c)
			
		category_table.pack(fill=BOTH,expand=1)
		self.__category_table = category_table
	
	def __create_song_table(self):
		col = ["ID", "Name","Singer","Category","Price","Quantity"]
		width = [85, 210, 200, 100, 100, 100]
		song_table = ttk.Treeview(self.__right_frame, columns=col, style='info.Treeview', selectmode='none')

		# scroll bars
		scroll_y = ttk.Scrollbar(song_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=song_table.yview)

		# avoid resize column
		song_table.bind("<Button-1>", lambda event: "break" \
		  				if song_table.identify_region(event.x, event.y) == "separator" else "")
		
		song_table.column('#0', width=0, stretch=NO)
		for c, w in zip(col, width):
			song_table.column(c, width=w, anchor=CENTER)
			song_table.heading(c, text=c)

		song_table.pack(fill=BOTH,expand=1)
		self.song_table = song_table
	
	def __update_category_table(self):
		children = self.__category_table.get_children()
		if children:
			self.__category_table.delete(*children)
		
		for category in self.__category_group.keys():
			self.__category_table.insert('', 'end', values=(category, ))

	def __update_song_table(self, L:list[str]):
		children = self.song_table.get_children()
		if children:
			self.song_table.delete(*children)
		
		song_list:list[Song] = []
		for key in L:
			st = self.__category_group[key]
			song_list += st

		for song in song_list:
			self.song_table.insert('', 'end', values=(song.id, song.name, song.singer_name,
					     							song.category, song.price, song.quantity))
	
	def __show_song(self):
		selections =  self.__category_table.selection()
		if not selections: selections = self.__category_table.get_children()
		
		selected_items = [self.__category_table.item(i, 'values')[0] for i in selections]
		self.__update_song_table(selected_items)

	def _reload(self):
		_, self.__category_group = self.__ref.group()
		self.__update_category_table()
		self.__show_song()

	