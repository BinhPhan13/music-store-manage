from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import font
from project_code.sale import *
from project_code.entity_manager import *
from ttkbootstrap.dialogs import Messagebox
from display.page import Page

class SaleDisplay(Page):
	def __init__(self,main_frame:ttk.Frame,sale_manager:SaleManager):
		super().__init__(main_frame)
		self.__update_search_entry()

		self.sale_mng = sale_manager
	
	def _init_frame(self):
		self.__create_search_frame()
		self.__create_sale_table()

	def __create_search_frame(self):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=13)

		# search frame
		ttk.Style().configure("Bold.TLabel",font=default_font)

		search_txt = ttk.Label(text = "Search",style="Bold.TLabel")
		search_frame = ttk.LabelFrame(self._frame,labelwidget=search_txt,border=2,relief=RIDGE, borderwidth=100)
		search_frame.place(x=300,y=20,width=500,height=70)
		search_frame.config(bootstyle='primary')

		self.search_entry = ttk.Entry(self._frame,font=default_font,background= "white")
		self.search_entry.place(x=504,y=45,width=174,height=35)

		self.search_options = ["Search by", "User's ID", "Song's ID", "Time"]
		self.box_search = ttk.Combobox(self._frame, values = self.search_options, 
									state='readonly',justify='center',font=default_font)
		self.box_search.current(0)
		self.box_search.place(x=313,y=45,width=180,height=35)

		# button
		ttk.Button(self._frame,text="Search", bootstyle="success",cursor="hand2",command=self.__search).place(x=690,y=45,width=100,height=35)

	# Sale frame
	def __create_sale_table(self):
		sale_label = ttk.Label(self._frame,text = "Sale",font=(self._font,15),background="#f3969a",anchor="center",foreground="#ffffff")
		sale_label.place(x=30,y=110,width=1040,height=30)

		#Tree view
		scroll_y = ttk.Scrollbar(self._frame,orient=VERTICAL)

		sale_column = ["User_ID","User's Name","Song_ID","Song's Name","Date","Price"]
		width = [90, 230, 100, 230, 100, 50]
		sale_table = ttk.Treeview(self._frame,columns=sale_column,style="info.Treeview",selectmode='browse',
			    				show="headings",yscrollcommand=scroll_y.set)
		scroll_y = ttk.Scrollbar(sale_table,orient=VERTICAL)
		scroll_y.pack(side=RIGHT,fill=Y)
		scroll_y.config(command=sale_table.yview)

		sale_table.bind("<Button-1>", lambda event: "break" if sale_table.identify_region(event.x, event.y) == "separator" else "")
		sale_table.bind("<ButtonRelease-1>",self.show_detail)
		sale_table.column('#0', width=0, stretch=NO)

		for c, w in zip(sale_column, width):
			sale_table.column(c, width=w, anchor=CENTER)
			sale_table.heading(c, text=c)
		sale_table.place(x=30,y=160,width=1040,height=450)
		self.__sale_table = sale_table
	
	def __update_search_entry(self):
		# Search Variable
		self.text_search = ttk.StringVar()
		self.search_box = ttk.StringVar()

		self.search_entry.configure(textvariable=self.text_search)
		self.box_search.configure(textvariable=self.search_box)
	
	# search function
	def __search(self):
		search_choice = self.box_search.get()
		if search_choice == "User's ID":
			self.__user_search()
		elif search_choice == "Song's ID":
			self.__song_search()
		elif search_choice == "Time":
			self.__time_search()
		else:
			Messagebox.show_error("Please choose", "Error")

	# search by user id
	def __user_search(self):
		user_id = self.search_entry.get().strip()
		result = self.sale_mng.search(user_id, '', '')

		if result:
			self.__update_sale_table(result)
		else:
			Messagebox.show_info("No users!", "Search query")
	
	# search by song id
	def __song_search(self):
		song_id = self.search_entry.get().strip()
		result = self.sale_mng.search('', song_id, '')
		
		if result:
			self.__update_sale_table(result)
		else:
			Messagebox.show_info("No songs!", "Search query")
	
	#search by time
	def __time_search(self):
		time = self.search_entry.get().strip()
		result = self.sale_mng.search('', '', time)
		
		if result:
			self.__update_sale_table(result)
		else:
			Messagebox.show_info("No date!", "Search query")
	
	def __update_sale_table(self, L:list[Sale]):
		children = self.__sale_table.get_children()
		if children:
			self.__sale_table.delete(*children)
		for sale in L:
			user_id = sale.user_id
			song_id = sale.song_id
			user = self.sale_mng.user_ref.find(user_id)
			song = self.sale_mng.song_ref.find(song_id)

			user_name = user.name if user else ''
			song_name = song.name if song else 'Deleted'

			self.__sale_table.insert('', 'end', values=(user_id, user_name, song_id, song_name, sale.time, sale.price))
		
	# add _ for button release
	def show_detail(self, _):
		win = ttk.Toplevel(self._frame)
		win.title('Detail')
		win.geometry('700x410+400+200')
		win.resizable(False, False)
		self.__create_user_frame(win)
		self.__create_song_frame(win)
		self.__fill_data()

	# User frame 
	def __create_user_frame(self, root:ttk.Toplevel):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=13)
		
		user_frame = ttk.Frame(root, width=320, height=380, relief=RIDGE)
		user_frame.place(x=15, y=15)

	# labels
		ttk.Label(user_frame,text="User's Details", bootstyle="secondary", font=(self._font,18,'bold')).place(x=10,y=10)

		ttk.Label(user_frame, text="Name", font=default_font).place(x=10, y=60, height=33)
		ttk.Label(user_frame, text="Phone", font=default_font).place(x=10, y=140, height=33)

	# entries
		self.txt_user = ttk.Entry(user_frame, font=default_font,background= "white")
		self.txt_user.place(x=90,y=60,width=220,height=35)

		self.txt_phone = ttk.Entry(user_frame, font=default_font,background= "white")
		self.txt_phone.place(x=90,y=140,width=220,height=35)

		ttk.Label(user_frame, text="Gender", font=default_font).place(x=10,y=300,height=33)
		ttk.Label(user_frame, text="Year", font=default_font).place(x=10,y=220,height=33)

		self.txt_gender = ttk.Entry(user_frame,font=default_font, background= "white")
		self.txt_gender.place(x=90,y=300,width=220,height=35)

		self.txt_year = ttk.Entry(user_frame,font=default_font, background= "white")
		self.txt_year.place(x=90,y=220,width=220,height=35)

	# Song frame 
	def __create_song_frame(self, root:ttk.Toplevel):
		default_font = font.nametofont("TkDefaultFont")
		default_font.configure(family=self._font, size=13)
		song_frame = ttk.Frame(root, width=330, height=380, relief=RIDGE)
		song_frame.place(x=350, y=15)

	# labels
		ttk.Label(song_frame,text="Song's Details", bootstyle="secondary", font=(self._font,18,'bold')).place(x=10,y=10)

		ttk.Label(song_frame, text="Name", font=default_font).place(x=10, y=60, height=33)
		ttk.Label(song_frame, text="Category", font=default_font).place(x=10, y=140, height=33)
		ttk.Label(song_frame, text="Price", font=default_font).place(x=10,y=300,height=33)
		ttk.Label(song_frame, text="Singer", font=default_font).place(x=10,y=220,height=33)

	# entries
		self.txt_song = ttk.Entry(song_frame,font=default_font,background= "white")
		self.txt_song.place(x=95,y=60,width=220,height=35)

		self.txt_category = ttk.Entry(song_frame,font=default_font,background= "white")
		self.txt_category.place(x=95,y=140,width=220,height=35)

		self.txt_singer = ttk.Entry(song_frame,font=default_font,background= "white")
		self.txt_singer.place(x=95,y=220,width=220,height=35)

		self.txt_price = ttk.Entry(song_frame,font=default_font,background= "white")
		self.txt_price.place(x=95,y=300,width=220,height=35)
	
	def __fill_data(self):
		#get_data from table
		selection = self.__sale_table.focus()
		content = (self.__sale_table.item(selection))['values']

		user_id = content[0]
		song_id = content[2]

		# find user, song data
		user:User = self.sale_mng.user_ref.find(user_id)
		song:Song = self.sale_mng.song_ref.find(song_id)
		
		# user entry
		user_name, user_gender, user_phone, user_year = \
		(user.name, user.gender, user.phone, user.year) if user else ('', '', '', '')

		self.txt_user.insert(END,user_name)
		self.txt_gender.insert(END,user_gender)
		self.txt_phone.insert(END,user_phone)
		self.txt_year.insert(END,user_year)

		#disable user input for entry
		self.txt_user.configure(state=READONLY)
		self.txt_gender.configure(state=READONLY)
		self.txt_phone.configure(state=READONLY)
		self.txt_year.configure(state=READONLY)

		# song entry
		song_name, song_category, song_singer_name, song_price = \
		(song.name, song.category, song.singer_name, song.price) if song else ('Deleted', '', '', '')

		self.txt_song.insert(END,song_name)
		self.txt_category.insert(END,song_category)
		self.txt_singer.insert(END, song_singer_name)
		self.txt_price.insert(END,song_price)

		#disabled song input for entry
		self.txt_song.configure(state=READONLY)
		self.txt_category.configure(state=READONLY)
		self.txt_singer.configure(state=READONLY)
		self.txt_price.configure(state=READONLY)
	
	def _reload(self):
		self.search_entry.delete(0,END)
		self.box_search.current(0)
		self.__update_sale_table(self.sale_mng.data)
