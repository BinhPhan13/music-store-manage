from tkinter import * 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from project_code.entity_manager import UserManager,SongManager
from project_code.sale import SaleManager

from display.resize_img import resize_picture
from display.page import Page
from display.home import Home
from display.users import UserDisplay
from display.songs import SongDisplay
from display.category import Categories
from display.singer import Singers
from display.bill import Bill
from display.sale import SaleDisplay
from display.report import Report

import os,sys,pickle

class IMS:    
	def __init__(self, root:ttk.Window):
		self.root = root

		self.menu_frame = ttk.Frame(self.root, bootstyle='light')
		self.menu_frame.place(x=0,y=0,width=250,height=700)

		self.main_frame = ttk.Frame(root)
		self.main_frame.place(x=251,y=69,width=(1350-250), height=(700-68))

		self.font = "bookman old style"

		self.__load_image()
		self.__init_title()
		self.__init_menu()

		separator = ttk.Separator(orient='vertical', bootstyle='primary')
		separator.place(x=250,y=0,relheight=1)

		self.path = "./_sale.mng"
		# load/create user, song, sale managers
		if os.path.exists(self.path):
			try:
				with open(self.path, "rb") as file:
					self.sale_mng:SaleManager = pickle.load(file)
					self.user_mng = self.sale_mng.user_ref
					self.song_mng = self.sale_mng.song_ref
			except Exception as e:
				print(e)
				sys.exit()
		else:
			self.user_mng = UserManager()
			self.song_mng = SongManager()
			self.sale_mng = SaleManager(self.user_mng, self.song_mng)
		
		self.home_page = Home(self.main_frame, self.user_mng, self.song_mng)
		self.user_page = UserDisplay(self.main_frame, self.user_mng)
		self.song_page = SongDisplay(self.main_frame, self.song_mng)
		self.category_page = Categories(self.main_frame, self.song_mng)
		self.singer_page = Singers(self.main_frame, self.song_mng)
		self.bill_page = Bill(self.main_frame, self.user_mng, self.song_mng, self.sale_mng)
		self.sale_page = SaleDisplay(self.main_frame, self.sale_mng)
		self.report_page = Report(self.main_frame, self.sale_mng,self.user_mng)

		self.__current_page:Page = None
		self.show_home_page()
		
	def __load_image(self):
		img_path = 'images/main/'
		self.__home_img = resize_picture(img_path + 'home.png',25,25)
		self.__user_img = resize_picture(img_path + 'user.png',25,25)
		self.__song_img = resize_picture(img_path + 'song.png',25,25)
		self.__singer_img = resize_picture(img_path + 'singer.png',25,25)
		self.__category_img = resize_picture(img_path + 'category.png',25,25)
		self.__bill_img = resize_picture(img_path + 'bill.png',25,25)
		self.__sale_img = resize_picture(img_path + 'sale.png',25,25)
		self.__report_img = resize_picture(img_path + 'report.png',25,25)
		self.__logout_img = resize_picture(img_path + 'logout.png',25,25)
		self.__admin_img = resize_picture(img_path + 'admin.png',50,50)

	def __init_menu(self):
		# Label
		ttk.Label(self.menu_frame, text='Group 3 - DS', font=(self.font,13,'bold'),
					anchor=CENTER,bootstyle='primary inverse').pack(fill=X, ipady=22)
		
		# Buttons
		## change style of button
		button_style = 'primary.Link.TButton'
		ttk.Style().configure(button_style, font=(self.font,12,'bold'))

		## create buttons		
		ttk.Button(self.menu_frame, text='Homepage', image=self.__home_img, compound=LEFT,
					style=button_style, cursor='hand2',
					command=self.show_home_page).pack(fill=X, ipady=15)

		ttk.Button(self.menu_frame, text='Users', image=self.__user_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_user_page).pack(fill=X, ipady=15)
		
		ttk.Button(self.menu_frame, text='Songs', image=self.__song_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_song_page).pack(fill=X, ipady=15)
	
		ttk.Button(self.menu_frame, text='Categories', image=self.__category_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_category_page).pack(fill=X, ipady=15)
		
		ttk.Button(self.menu_frame, text='Singers', image=self.__singer_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_singer_page).pack(fill=X, ipady=15)
	
		ttk.Button(self.menu_frame, text='Bill', image=self.__bill_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_bill_page).pack(fill=X, ipady=15)
		
		ttk.Button(self.menu_frame, text='Sales', image=self.__sale_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_sale_page).pack(fill=X, ipady=15)
		
		ttk.Button(self.menu_frame, text='Report', image=self.__report_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.show_report_page).pack(fill=X, ipady=15)

		ttk.Button(self.menu_frame, text='Logout', image=self.__logout_img, compound=LEFT,
					style=button_style, cursor='hand2', 
					command=self.logout).pack(fill=X, ipady=15)

	def __init_title(self):
		# TITLE FRAME
		title_frame = ttk.Frame(self.root, bootstyle='primary')
		title_frame.place(x=250,y=0,width=1100, height=68)
		
		## title label 
		ttk.Label(title_frame, text='Music Store Managment System', font=(self.font,20,'bold'),
				bootstyle='primary inverse').pack(side=LEFT, padx=20)

		## button admin 
		ttk.Button(title_frame, text=' Admin', image= self.__admin_img,compound=LEFT, 
				bootstyle='primary', command=self.hello_admin).pack(side=RIGHT, padx=50)

	def hello_admin(self):
		Messagebox.show_info('Hello Admin')

	def logout(self):
		question = Messagebox.show_question('Are you sure you want to quit?')
		if question == 'Yes':
			self.main_frame.quit()
	
	def show_home_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.home_page.show()
		self.__current_page = self.home_page

	def show_user_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.user_page.show()
		self.__current_page = self.user_page

	def show_song_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.song_page.show()
		self.__current_page = self.song_page

	def show_category_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.category_page.show()
		self.__current_page = self.category_page

	def show_singer_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.singer_page.show()
		self.__current_page = self.singer_page
		
	def show_bill_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.bill_page.show()
		self.__current_page = self.bill_page

	def show_sale_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.sale_page.show()
		self.__current_page = self.sale_page

	def show_report_page(self):
		if self.__current_page:
			self.__current_page.forget()
		
		self.report_page.show()
		self.__current_page = self.report_page

	def save(self):
		can_dump = False
		while not can_dump:
			try:
				with open(self.path, "wb") as file:
					pickle.dump(self.sale_mng, file)
				can_dump = True
			except Exception as e:
				print(e)


if __name__ == "__main__":
	root = ttk.Window(themename='minty')
	obj = IMS(root)
	root.geometry('1350x700+0+0')
	root.title('Group 3 - DS - Advance Python Project')
	root.resizable(width = False, height = False)
	print("hello before")
	root.mainloop()
	print("hello after")
	obj.save()
	print("hello after save")