import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ttkbootstrap import font
from project_code.entity_manager import UserManager, SongManager
from project_code.entity import Song
from project_code.sale import SaleManager 
from project_code.entity import User
from tkinter import *
from datetime import datetime
from page import Page


class Bill(Page):
	def __init__(self, main_frame:ttk.Frame, user_manager:UserManager, 
	      				song_mng:SongManager, sale_mng:SaleManager):
		
		super().__init__(main_frame)
		self.__update_entry()

		self.user_manager = user_manager
		self.song_manager = song_mng
		self.sale_mng = sale_mng
	
	def _init_frame(self):
		self.__init_first_frame()
		self.__init_second_frame()
	
	def __init_first_frame(self):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=13)

		input_text = ttk.Label(text="Search Users", font=(self._font,18))
		
		self.__first_frame = ttk.LabelFrame(self._frame,relief=RIDGE, borderwidth=1,
				     						labelwidget=input_text,bootstyle='primary')
		
		# 1st row
		ttk.Label(self.__first_frame, text="Name", font=default_font).place(x=40, y=12, height=35)
		self.txt_user_name = ttk.Entry(self.__first_frame, font=default_font)
		self.txt_user_name.place(x=120,y=12,width=220,height=35)

		ttk.Label(self.__first_frame, text="Phone", font=default_font).place(x=420, y=12, height=35)
		self.txt_phone = ttk.Entry(self.__first_frame, font=default_font)
		self.txt_phone.place(x=500,y=12,width=220,height=35)

		# 2nd row
		ttk.Label(self.__first_frame, text="Gender", font=default_font).place(x=40,y=77,height=35)
		gender_options = ["","Female", "Male"]
		self.txt_gender = ttk.Combobox(self.__first_frame, values = gender_options,
				 						state='readonly',justify='center',font=default_font)
		self.txt_gender.current(0)
		self.txt_gender.place(x=120,y=77,width=220,height=35)

		ttk.Label(self.__first_frame, text="Year", font=default_font).place(x=420,y=77,height=35)
		self.txt_year = ttk.Entry(self.__first_frame, font=default_font)
		self.txt_year.place(x=500,y=77,width=220,height=35)

		# buttons
		ttk.Button(self.__first_frame, text="Confirm", bootstyle="secondary",cursor="hand2",
	     			command=self.__next).place(x=800,y=12,width=230,height=35)
		ttk.Button(self.__first_frame, text="Search", bootstyle="secondary",cursor="hand2",
	     			command=self.__search_user).place(x=800,y=77,width=230,height=35)
		
		self.__create_user_table()

	def __create_user_table(self):
		col = ['ID', 'Name', 'Gender', 'Year', 'Phone']
		width = [100, 230, 100, 100, 100]
		user_table = ttk.Treeview(self.__first_frame, columns=col, style='info.Treeview', selectmode='browse')

		# scroll bars
		scroll_y = ttk.Scrollbar(user_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=user_table.yview)

		# avoid resize column
		user_table.bind("<Button-1>", lambda event: "break" \
		  				if user_table.identify_region(event.x, event.y) == "separator" else "")
		user_table.column('#0', width=0, stretch=NO)
		
		for c, w in zip(col, width):
			user_table.column(c, width=w, anchor=CENTER)
			user_table.heading(c, text=c)
		user_table.place(x=15, y=140, width=1030, height=435)
		self.__user_table = user_table

	def __init_second_frame(self):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=13)
		
		self.__second_frame = ttk.Frame(self._frame)

		# song frame
		song_txt = ttk.Label(text = "Song's Details", font=(self._font,18))
		self.song_frame = ttk.LabelFrame(self.__second_frame, relief=RIDGE, borderwidth=1,
				    						labelwidget=song_txt,bootstyle='primary')
		self.song_frame.place(x=0, y=0, width=1060, height=350)

		## entries
		ttk.Label(self.song_frame,text="Name",font=default_font).place(x=8, y=10,height=33)
		self.txt_song_name = ttk.Entry(self.song_frame, font=default_font)
		self.txt_song_name.place(x=67,y=10,width=170,height=35)
		
		ttk.Label(self.song_frame,text="Singer",font=default_font).place(x=270,y=10,height=33)
		self.txt_singer = ttk.Entry(self.song_frame, font=default_font)
		self.txt_singer.place(x=335,y=10,width=170,height=35)
		
		ttk.Label(self.song_frame,text="Category",font=default_font).place(x=538,y=10,height=33)
		self.txt_category = ttk.Entry(self.song_frame, font=default_font)
		self.txt_category.place(x=628,y=10,width=170,height=35)
		
		ttk.Label(self.song_frame,text="Price",font=default_font).place(x=830,y=10,height=33)
		self.txt_price = ttk.Entry(self.song_frame,font=default_font)
		self.txt_price.place(x=880,y=10,width=170,height=35)

		# buttons
		ttk.Button(self.song_frame,text = "Back",bootstyle="secondary",cursor="hand2",
	     			command=self.__back).place(x=734,y=55,width=100,height=35)
		ttk.Button(self.song_frame,text = "Search",bootstyle="secondary",cursor="hand2",
	     			command=self.__search_song).place(x=842,y=55,width=100,height=35)
		ttk.Button(self.song_frame,text = "Add",bootstyle="secondary",cursor="hand2", 
	     			command=self.__add_cart).place(x=950,y=55,width=100,height=35)

		self.__create_song_table()

		# cart frame
		cart_txt = ttk.Label(self.__second_frame,text = "Cart",style="Bold.TLabel",font=(self._font,18))
		self.cart_frame = ttk.LabelFrame(self.__second_frame, relief=RIDGE, borderwidth=1,
				   						labelwidget=cart_txt,bootstyle='primary')
		self.cart_frame.place(x=0, y=355, width=1060, height=245)

		ttk.Button(self.cart_frame,text = "Delete", bootstyle="secondary",cursor="hand2",
	     			command=self.__delete_cart).place(x=825,y=175,width=100,height=33)
		ttk.Button(self.cart_frame,text = "Finish", bootstyle="secondary",cursor="hand2",
	     			command=self.__bill).place(x=940,y=175,width=100,height=33)
		
		self.__create_cart()
		
	def __create_song_table(self):
		col = ["ID", "Name","Singer","Category","Price","Quantity"]
		width = [100, 200, 200, 100, 100, 100]
		song_table = ttk.Treeview(self.song_frame, columns=col, style='info.Treeview', selectmode='browse')
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
		song_table.place(x=10, y=105, width=1040, height=200)
		self.__song_table = song_table

	def __create_cart(self):
		col = ["User's ID", "Song's ID","Date","Price"]
		width = [100, 100, 200, 100]
		cart_table = ttk.Treeview(self.cart_frame, columns=col, style='info.Treeview', selectmode='browse')

		scroll_y = ttk.Scrollbar(cart_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=cart_table.yview)
		# avoid resize column
		cart_table.bind("<Button-1>", lambda event: "break" \
		  				if cart_table.identify_region(event.x, event.y) == "separator" else "")
		
		cart_table.column('#0', width=0, stretch=NO)
		for c, w in zip(col, width):
			cart_table.column(c, width=w, anchor=CENTER)
			cart_table.heading(c, text=c)
		cart_table.place(x=10, y=0, width=1040, height=161)
		self.cart_table = cart_table
		
	def __update_entry(self):
	# variables for users' entries
		self.user_name = ttk.StringVar()
		self.gender = ttk.StringVar()
		self.year = ttk.StringVar()
		self.phone = ttk.StringVar()

		self.txt_user_name.configure(textvariable=self.user_name)
		self.txt_gender.configure(textvariable=self.gender)
		self.txt_year.configure(textvariable=self.year)
		self.txt_phone.configure(textvariable=self.phone)

	# variables for songs' entries
		self.song_name = ttk.StringVar()
		self.singer = ttk.StringVar()
		self.category = ttk.StringVar()
		self.price = ttk.StringVar()

		self.txt_song_name.configure(textvariable=self.song_name)
		self.txt_singer.configure(textvariable=self.singer)
		self.txt_category.configure(textvariable=self.category)
		self.txt_price.configure(textvariable=self.price)

# NO MORE INIT FROM HERE

	def __update_user_table(self, L:list[User]):
		'''Delelte old and create new view base on input list'''
		children = self.__user_table.get_children()
		if children:
			self.__user_table.delete(*children)
		for user in L:
			self.__user_table.insert('', 'end', values=(user.id, user.name, user.gender, user.year, user.phone))
	
	def __update_song_table(self, L:list[Song]):
		'''Delete old and create new view base on input list'''
		children = self.__song_table.get_children()
		if children:
			self.__song_table.delete(*children)
		for song in L:
			self.__song_table.insert('', 'end', song.id, values=(song.id, song.name,song.singer_name, 
																song.category, song.price, song.quantity))
	
	def __next(self):
		i = self.__user_table.focus()
		if not i: 
			Messagebox.show_error("No users have been chosen", "Error")
			return
		selected_row = self.__user_table.item(i, 'values')
		self.__selected_user_id = selected_row[0]

		self.__show_second_frame()

	def __back(self):
		# back restart everything
		self.forget()
		self.show()
		
	def __show_first_frame(self):
		self.__second_frame.place_forget()
		self.__first_frame.place(x=20, y=10, width=1060, height=615)
	
	def __show_second_frame(self):
		self.__first_frame.place_forget()
		self.__second_frame.place(x=20, y=10, width=1060, height=615)
		self.__clear_song_input()

	def __pull_user_info(self):
		''' Pull the input from entries and store in manager temp info'''
		name = self.user_name.get().strip()
		gender = self.gender.get().strip()
		year = self.year.get().strip()
		phone = self.phone.get().strip()

		self.user_manager.get_info(name, gender, year, phone)
		
	def __search_user(self):
		self.__pull_user_info()
		result = self.user_manager.search(*self.user_manager._temp_info)

		if not result: 
			return Messagebox.show_info("No result!","Search query")
		
		self.__clear_user_input()
		self.__update_user_table(result)

	def __clear_user_input(self):
		self.txt_user_name.delete(0, END)
		self.txt_gender.current(0)	
		self.txt_year.delete(0, END)	
		self.txt_phone.delete(0, END)

	def __pull_song_info(self):
		''' Pull the input from entries and store in manager temp info'''
		name = self.song_name.get().strip()
		category = self.category.get().strip()
		singer = self.singer.get().strip()
		price = self.price.get().strip()

		self.song_manager.get_info(name, singer, category, price, '')

	def __search_song(self):
		self.__pull_song_info()
		song_info = self.song_manager._temp_info
		result = self.song_manager.search(*song_info)

		if not result: 
			return Messagebox.show_info("No result!","Search query")
		self.__clear_song_input()
		self.__update_song_table(result)

	def __clear_song_input(self):
		self.txt_song_name.delete(0, END)
		self.txt_category.delete(0,END)	
		self.txt_singer.delete(0, END)	
		self.txt_price.delete(0, END)

	def __add_cart(self):
		user_id = self.__selected_user_id

		i = self.__song_table.focus()
		if not i: return
		selected_row = self.__song_table.item(i,'values')
		song_id = selected_row[0]
		price = selected_row[4]
		date = datetime.now().strftime("%d/%m/%Y")
		
		quantity = selected_row[5]
		if quantity != "0":
			self.cart_table.insert('','end', values=(user_id, song_id, date, price))
		else:
			return Messagebox.show_error("Out of stock", "Error")
		
		# minus quantity of display song table by 1
		row_list = list(selected_row)
		row_list[5] = f"{int(quantity) - 1}"

		self.__song_table.item(i, values=row_list)

	def __delete_cart(self):
		x = self.cart_table.focus()
		if not x: return

		# return quantity to song table
		# possible because song table are insert with iid = song_id
		i = self.cart_table.item(x, 'values')[1]
		selected_row = self.__song_table.item(i, 'values')
		quantity = selected_row[5]

		row_list = list(selected_row)
		row_list[5] = f"{int(quantity) + 1}"
		self.__song_table.item(i, values=row_list)

		self.cart_table.delete(x)

	def __bill(self):
		total = 0.0
		for i in self.cart_table.get_children():
			user_id, song_id, date, price = self.cart_table.item(i, 'values')
			self.sale_mng.add(user_id, song_id, date, float(price))
			total += float(price)
		
		Messagebox.show_info(f"Total Price: {total}","Total")
		self.__delete_cart_all()
		
		self.__show_first_frame()
	
	def __delete_cart_all(self):
		children = self.cart_table.get_children()
		self.cart_table.delete(*children)

	def _reload(self):
		self.__update_user_table(self.user_manager.values)
		self.__update_song_table(self.song_manager.values)
		self.__delete_cart_all()

	def show(self):
		super().show()
		self.__show_first_frame()
	