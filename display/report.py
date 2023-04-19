from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from sale import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
from page import Page
import matplotlib as plt

class Report(Page):
	def __init__(self, main_frame:ttk.Frame, sale_manager: SaleManager, user_manager: UserManager):
		self.sale_manager = sale_manager
		self.user_manager = user_manager
		super().__init__(main_frame)

	def _init_frame(self):
		self.font_size = 13
		self.__init_searchbar()

		#plot design
		self.color = sns.color_palette('Set2')[1]
		sns.set_style('darkgrid')
		plt.rc('axes', titlesize=18)  
		plt.rc('axes', labelsize=12)
		plt.rc('xtick', labelsize=10)
		plt.rc('ytick', labelsize=10)
		plt.rc('legend', fontsize=12)
		plt.rc('font', size=12)
		plt.rcParams['font.family'] = self._font
		self.__init_plots()

	def __init_searchbar(self):
		graph_list = ["Users genders", "Users ages", "Top users", "Top songs", "Date"]
		self.selection = ttk.Combobox(self._frame, values = graph_list,state = "readonly", 
									justify='center', font=(self._font,self.font_size), background='white')
		self.selection.place(x=230, y=40, width=400, height=40)
		self.selection.current(0)

		ttk.Button(self._frame, text="Plot", bootstyle="success",cursor="hand2",
	     			command=self.__show_plot).place(x=690,y=40,width=180,height=40)
	
	def __init_plots(self):
		self.options = {
			"Users genders": self.__user_genders(),
			"Users ages": self.__user_ages(),
			"Top users": self.__top_users(),
			"Top songs": self.__top_songs(),
			"Date": self.__date(),
		}
		self.current_plot:Canvas = None

	def __show_plot(self):
		selection = self.selection.get()
		selected_plot = self.options[selection]

		if self.current_plot:
			self.current_plot.place_forget()
	
		if selection in ["Users genders", "Users ages"]:
			selected_plot.place(x=90, y=80, width=800, height=600)
		else:
			selected_plot.place(x=110, y=80, width=800, height=500)
		
		self.current_plot = selected_plot
	
	# TODO: change shadow option, change _init_ paramenter
	def __user_genders(self):
		male, female = self.user_manager.count_gender()

		# plot
		fig = Figure()
		ax:plt.Axes = fig.add_subplot()
		ax.set_title("Users genders")
		ax.pie([male, female], labels = ['Male', 'Female'], shadow=False, 
	 			autopct=lambda x: f"{x:.2f}%")

		# draw
		chart = FigureCanvasTkAgg(fig, self._frame)
		chart.draw()
		return chart.get_tk_widget()
			
	def __user_ages(self):
		age1, age2, age3 = self.user_manager.count_age()

		# plot
		fig = Figure()
		ax:plt.Axes = fig.add_subplot()
		ax.pie([age1, age2, age3], labels = ['<18', '18-30', '>30'], shadow=True, 
	 			autopct=lambda x: f"{x:.2f}%")
		ax.set_title('Users ages')

		# draw
		chart = FigureCanvasTkAgg(fig, self._frame)
		chart.draw()
		return chart.get_tk_widget()

	def __top_users(self):
		user_rp = self.sale_manager.group_user()
		length = min(len(user_rp), 10)
		x = (list(user_rp.keys()))[:length]
		y = (list(user_rp.values()))[:length]

		#plot
		fig = Figure()
		ax:plt.Axes = fig.add_subplot()
		ax.bar(range(length), y, tick_label = x, color=self.color)
		ax.set_title('Top users')

		#display chart
		chart = FigureCanvasTkAgg(fig, self._frame)
		chart.draw()
		return chart.get_tk_widget()
	
	def __top_songs(self):
		song_rp = self.sale_manager.group_song()
		length = min(len(song_rp), 10)
		x = (list(song_rp.keys()))[:length]
		y = (list(song_rp.values()))[:length]

		# plot
		fig = Figure()
		ax:plt.Axes = fig.add_subplot()
		ax.bar(range(length), y, tick_label = x, color=self.color)
		ax.set_title('Top songs')

		# display 
		chart = FigureCanvasTkAgg(fig, self._frame)
		chart.draw()
		return chart.get_tk_widget()

	def __date(self):
		time_rp = self.sale_manager.group_time()
		length = min(len(time_rp), 5)
		x = (list(time_rp.keys()))[:length]
		y = (list(time_rp.values()))[:length]

		# plot
		fig = Figure()
		ax:plt.Axes = fig.add_subplot()
		ax.bar(range(length), y, tick_label = x, color=self.color)
		ax.set_title(f'Last {length} days')

		# display
		chart = FigureCanvasTkAgg(fig, self._frame)
		chart.draw()
		return chart.get_tk_widget()
	
	def _reload(self):
		self.__init_plots()