import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ttkbootstrap import font
from project_code.entity_manager import UserManager
from project_code.entity import User
from page import Page
from tkinter import *

class UserDisplay(Page):
	def __init__(self, main_frame:ttk.Frame, user_manager:UserManager):
		super().__init__(main_frame)

		self.__update_entry()
		self.user_manager = user_manager

	def _init_frame(self):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=14)

		ttk.Label(self._frame, text = "User's Details", font=(self._font, 16),
	    		bootstyle = "secondary inverse", anchor="center").place(x=35,y=30, width=1035, height=50)

		# name entry
		ttk.Label(self._frame, text="Name", font=default_font).place(x=63, y=100, height=35)
		self.txt_name = ttk.Entry(self._frame, font=default_font)
		self.txt_name.place(x=153,y=100,width=180,height=35)

		# gender entry
		ttk.Label(self._frame, text="Gender", font=default_font).place(x=363, y=100, height=35)
		gender_options = ["","Female", "Male"]
		self.txt_gender = ttk.Combobox(self._frame, values = gender_options,
									state='readonly',justify='center', font=default_font)
		self.txt_gender.current(0)
		self.txt_gender.place(x=453,y=100,width=180,height=35)

		# phone entry	
		ttk.Label(self._frame, text="Phone", font=default_font).place(x=63,y=180,height=35)
		self.txt_phone = ttk.Entry(self._frame, font=default_font)
		self.txt_phone.place(x=153,y=180,width=180,height=35)

		# year entry
		ttk.Label(self._frame, text="Year", font=default_font).place(x=363,y=180,height=35)
		self.txt_year = ttk.Entry(self._frame, font=default_font)
		self.txt_year.place(x=453,y=180,width=180,height=35)

		# first button row
		ttk.Button(self._frame, text="Add", bootstyle="success",cursor="hand2",
	    		command=self.__add_user).place(x=673,y=100,width=100,height=35)
		ttk.Button(self._frame, text="Update", bootstyle="success",cursor="hand2",
	     		command=self.__update_user).place(x=803, y=100, width=100, height=35)
		ttk.Button(self._frame, text="Search", bootstyle="success",cursor="hand2",
	     		command=self.__search_user).place(x=933,y=100,width=100,height=35)
		
		# second button row
		self.hide_show = ttk.Button(self._frame, text="Show", bootstyle="success",cursor="hand2",
			      					command=self.__show_table)
		self.hide_show.place(x=673, y=180, width=360, height=35)

		self.__create_table()

	def __create_table(self):
		col = ['ID', 'Name', 'Gender', 'Year', 'Phone']
		width = [100, 230, 100, 100, 200]
		user_table = ttk.Treeview(self._frame, columns=col, style='info.Treeview', selectmode='browse')

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
		self.__user_table = user_table

	def __update_entry(self):
		'''Add variables to entry'''
		self.name = ttk.StringVar()
		self.gender = ttk.StringVar()
		self.year = ttk.StringVar()
		self.phone = ttk.StringVar()

		self.txt_name.configure(textvariable=self.name)
		self.txt_gender.configure(textvariable=self.gender)
		self.txt_year.configure(textvariable=self.year)
		self.txt_phone.configure(textvariable=self.phone)

	def __hide_table(self):
		self.__user_table.place_forget()
		self.hide_show.configure(text="Show", command=self.__show_table)
	def __show_table(self):
		self.__user_table.place(x=35,y=250,width=1035,height=360)
		self.hide_show.configure(text="Hide", command=self.__hide_table)

	def __clear_input(self):
		self.txt_name.delete(0, END)
		self.txt_gender.current(0)	
		self.txt_year.delete(0, END)	
		self.txt_phone.delete(0, END)

	def __update_table(self, L:list[User]):
		'''Delete old and create new view base on input list'''
		children = self.__user_table.get_children()
		if children:
			self.__user_table.delete(*children)
		for u in L:
			self.__user_table.insert('', 'end', values=(u.id, u.name, u.gender, u.year, u.phone))

	def __visible_table(self):
		try:
			self.__user_table.info()
			return True
		except Exception:
			return False
	
	def __pull_info(self):
		''' Pull the input from entries and store in manager temp info'''
		name = self.name.get().strip()
		gender = self.gender.get().strip()
		year = self.year.get().strip()
		phone = self.phone.get().strip()

		self.user_manager.get_info(name, gender, year, phone)

	def __search_user(self):
		self.__pull_info()
		result = self.user_manager.search(*self.user_manager._temp_info)
		if not result: 
			return Messagebox.show_info("No result!", "Search query")
		
		self.__clear_input()
		self.__update_table(result)
		if not self.__visible_table():
			self.__show_table()		

	def __add_user(self):
		self.__pull_info()
		add_error = self.user_manager.add()
		if add_error:
			return Messagebox.show_error(add_error, "Error")
		
		self.__clear_input()
		self._reload()
		return 1

	def __update_user(self):
		i = self.__user_table.focus()
		if not i: 
			return Messagebox.show_error("Error", "No user selected!")
		
		self.__pull_info()
		
		selected_row = self.__user_table.item(i, 'values')
		user_id = selected_row[0]
		update_error = self.user_manager.update(user_id)

		if update_error:
			return Messagebox.show_error("Error", update_error)
		
		self.__clear_input()
		self._reload()
		return 1
	
	def _reload(self):
		self.__update_table(self.user_manager.values)