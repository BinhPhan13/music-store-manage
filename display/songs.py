from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap import font
from project_code.entity_manager import SongManager
from project_code.entity import Song
from display.page import Page

class SongDisplay(Page):
	def __init__(self, main_frame:ttk.Frame, song_manager:SongManager):
		super().__init__(main_frame)

		self.__update_entry()
		self.song_mng = song_manager

	def _init_frame(self):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=14)

		ttk.Label(self._frame, text = "Song's Details", font=(self._font, 16),
	    		bootstyle = "secondary inverse",anchor="center").place(x=35,y=30,width=1035, height=50)

		# name entry
		ttk.Label(self._frame, text="Name", font=default_font).place(x=63, y=100, height=35)
		self.txt_name = ttk.Entry(self._frame,font=default_font)
		self.txt_name.place(x=153,y=100,width=180,height=35)

		# singer entry
		ttk.Label(self._frame,text="Singer",font=default_font).place(x=363,y=100,height=35)
		self.txt_singer = ttk.Entry(self._frame,font=default_font)
		self.txt_singer.place(x=453,y=100,width=180,height=35)

		# category entry
		ttk.Label(self._frame,text="Category",font=default_font).place(x=63,y=180,height=35)
		self.txt_category = ttk.Entry(self._frame,font=default_font)
		self.txt_category.place(x=153,y=180,width=100,height=35)

		# price entry
		ttk.Label(self._frame,text="Price",font=default_font).place(x=263,y=180,height=35)
		self.txt_price = ttk.Entry(self._frame,font=default_font)
		self.txt_price.place(x=323,y=180,width=100,height=35)
		
		# quantity entry
		ttk.Label(self._frame,text="Quantity",font=default_font).place(x=443,y=180,height=35)
		self.txt_quantity = ttk.Entry(self._frame,font=default_font)
		self.txt_quantity.place(x=533, y=180, width=100,height=35)

		# 1st row buttons
		ttk.Button(self._frame,text="Add", bootstyle="success",cursor="hand2",
	     		command=self.__add_song).place(x=673,y=100,width=100,height=35)
		ttk.Button(self._frame,text="Update", bootstyle="success",cursor="hand2",
	     		command=self.__update_song).place(x=803,y=100,width=100,height=35)
		ttk.Button(self._frame,text="Delete", bootstyle="success",cursor="hand2",
	     		command=self.__delete).place(x=933,y=100,width=100,height=35)
		
		# 2nd row buttons
		ttk.Button(self._frame,text="Search", bootstyle="success",cursor="hand2",
	     		command=self.__search).place(x=673,y=180,width=100,height=35)
		
		self.hide_show = ttk.Button(self._frame,text="Show", bootstyle="success",cursor="hand2",
			      					command=self.__show_table)
		self.hide_show.place(x=803,y=180,width=230,height=35)

		self.__create_table()

	def __create_table(self):
		col = ["ID", "Name", "Singer", "Category"," Price", "Quantity"]
		width = [100, 230, 200, 200, 200, 100]
		song_table = ttk.Treeview(self._frame, columns=col, style='info.Treeview', selectmode='browse')

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
			
		self.__song_table = song_table
	
	def __update_entry(self):
		'''Add variables to entry'''
		self.name = ttk.StringVar()
		self.singer = ttk.StringVar()
		self.category = ttk.StringVar()
		self.price = ttk.StringVar()
		self.quantity = ttk.StringVar()

		self.txt_name.configure(textvariable=self.name)
		self.txt_singer.configure(textvariable=self.singer)
		self.txt_category.configure(textvariable=self.category)
		self.txt_price.configure(textvariable=self.price)
		self.txt_quantity.configure(textvariable=self.quantity)

	def __update_table(self, L:list[Song]):
		'''Delete old and create new view base on input list'''
		children = self.__song_table.get_children()
		if children:
			self.__song_table.delete(*children)
		for song in L:
			self.__song_table.insert('', 'end', values=(song.id, song.name, song.singer_name, song.category, 
					     							song.price, song.quantity))
	
	def __hide_table(self):
		self.__song_table.place_forget()
		self.hide_show.configure(text="Show", command=self.__show_table)
	def __show_table(self):
		self.__song_table.place(x=35,y=250,width=1035,height=360)
		self.hide_show.configure(text="Hide", command=self.__hide_table)

	def __clear_input(self):
		self.txt_name.delete(0, END)
		self.txt_category.delete(0,END)	
		self.txt_singer.delete(0, END)	
		self.txt_price.delete(0, END)
		self.txt_quantity.delete(0, END)

	def __pull_info(self):
		''' Pull the input from entries and store in manager temp info'''
		name = self.name.get().strip()
		category = self.category.get().strip()
		singer = self.singer.get().strip()
		price = self.price.get().strip()
		quantity = self.quantity.get().strip()

		self.song_mng.get_info(name, singer, category, price, quantity)
		
	def __visible_table(self):
		try:
			self.__song_table.info()
			return True
		except Exception:
			return False

	def __search(self):
		self.__pull_info()
		song_info = self.song_mng._temp_info
		result = self.song_mng.search(*song_info)
		if not result: 
			return Messagebox.show_info("No result!", "Search query")
		
		self.__clear_input()
		self.__update_table(result)

		if not self.__visible_table():
			self.__show_table()

	def __add_song(self):
		self.__pull_info()
		add_error = self.song_mng.add()
		if add_error:
			return Messagebox.show_error(add_error,"Error")
		self.__clear_input()
		self._reload()
		return 1

	def __update_song(self):
		i = self.__song_table.focus()
		if not i: 
			return Messagebox.show_error("No song selected!", "Error")
		
		self.__pull_info()

		selected_row = self.__song_table.item(i, 'values')
		song_id = selected_row[0]
		update_error = self.song_mng.update(song_id)

		if update_error:
			return Messagebox.show_error(update_error, "Error")
		
		self.__clear_input()
		self._reload()
		return 1
	
	def __delete(self):
		i = self.__song_table.focus()
		if not i: 
			Messagebox.show_error("No user selected!","Error")
			return
		
		selected_row = self.__song_table.item(i, 'values')
		song_id = selected_row[0]
		self.song_mng.delete(song_id)
		
		self.__clear_input()
		self._reload()
		return 1
	
	def _reload(self):
		self.__update_table(self.song_mng.values)