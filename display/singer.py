from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import font
from project_code.entity import Song
from project_code.entity_manager import *
from display.page import Page

class Singers(Page):
	def __init__(self, main_frame:ttk.Frame, song_mng = SongManager):
		super().__init__(main_frame)
		self.__ref = song_mng
	
	def _init_frame(self):
		# change default font
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=14)

		# left frame
		singer_txt = ttk.Label(text = "Singers", font=default_font)
		self.__left_frame = ttk.LabelFrame(self._frame, relief=RIDGE, borderwidth=1,
				  						labelwidget=singer_txt,bootstyle='primary')
		self.__left_frame.place(x=25, y=53, width=210, height=500)

		self.__create_singer_table()
		ttk.Button(self._frame, text="Show", bootstyle="success", cursor="hand2", 
	     			command=self.__show_song).place(x=25, y=573, width=210, height=35)
		
		#Song label frame
		ttk.Label(self._frame,text="Song's Details", font=(self._font,16),
	    		bootstyle = "secondary inverse",anchor = CENTER).place(x=273,y=15,width=800,height=38)

		# right frame
		ttk.Label(text = "Songs", font=default_font)
		self.__right_frame = ttk.Frame(self._frame)
		self.__right_frame.place(x=273,y=65,width=800,height=545)

		self.__create_song_table()
	
	def __create_singer_table(self):
		col = ["Singer"]
		width = [100]
		singer_table = ttk.Treeview(self.__left_frame, columns=col, style='info.Treeview', selectmode='extended')

		# scroll bars
		scroll_y = ttk.Scrollbar(singer_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=singer_table.yview)

		# avoid resize column
		singer_table.bind("<Button-1>", lambda event: "break" \
		      				if singer_table.identify_region(event.x, event.y) == "separator" else "")
		
		singer_table.column('#0', width=0, stretch=NO)
		for c, w in zip(col, width):
			singer_table.column(c, width=w, anchor=CENTER)
			singer_table.heading(c, text=c)
			
		singer_table.pack(fill=BOTH,expand=1)
		self.__singer_table = singer_table
	
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
	
	def __update_singer_table(self):
		children = self.__singer_table.get_children()
		if children:
			self.__singer_table.delete(*children)

		for singer in self.__singer_group.keys():
			self.__singer_table.insert('', 'end', values=(singer, ))

	def __update_song_table(self, L:list[str]):
		children = self.song_table.get_children()
		if children:
			self.song_table.delete(*children)

		song_list:list[Song] = []
		for key in L:
			st = self.__singer_group[key]
			song_list += st

		for song in song_list:
			self.song_table.insert('', 'end', values=(song.id, song.name, song.singer_name,
					     							song.category, song.price, song.quantity))
	
	def __show_song(self):
		selections =  self.__singer_table.selection()
		if not selections: selections = self.__singer_table.get_children()

		selected_items = [self.__singer_table.item(i, 'values')[0] for i in selections]
		self.__update_song_table(selected_items)
	
	def _reload(self):
		self.__singer_group, _ = self.__ref.group()
		self.__update_singer_table()
		self.__show_song()
	