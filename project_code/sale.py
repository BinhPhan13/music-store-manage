from entity_manager import *
from entity import *
from helper import process_time, reverse_date
from collections import defaultdict
from pattern import PatternSale

class Sale:
	def __init__(self, user_id:str, song_id:str, time:str, price:float):
		self.__user = user_id
		self.__song = song_id
		self.__time = time
		self.__price = price

	def __str__(self) -> str:
		return f"{self.user_id:15}{self.song_id:15}{self.time:10}{self.__price:10}"

	def __eq__(self, pattern: PatternSale):
		match_user = self.user_id == pattern.user_id or not pattern.user_id
		match_song = self.song_id == pattern.song_id or not pattern.song_id

		match_time = reverse_date(self.time) >= reverse_date(pattern.time[0]) and \
					reverse_date(self.time) <= reverse_date(pattern.time[1])
		
		return match_user and match_song and match_time
	
	@property
	def user_id(self):
		return self.__user
	@property
	def song_id(self):
		return self.__song
	@property
	def time(self):
		return self.__time
	@property
	def price(self):
		return self.__price

class SaleManager:
	def __init__(self, user_manager:UserManager, song_manager:SongManager):
		self.__user_ref = user_manager
		self.__song_ref = song_manager
		self.__data:list[Sale] = []

	@property
	def user_ref(self):
		return self.__user_ref
	@property
	def song_ref(self):
		return self.__song_ref
	
	@property
	def data(self):
		return self.__data
	
	def search(self, user_id, song_id, time) -> list[Sale]:
		time = process_time(time)
		pattern_sale = PatternSale(user_id, song_id, time)
		return [sale for sale in self.__data if sale == pattern_sale]

	def add(self, user_id:str, song_id:str, date:str, price:float):
		song:Song = self.__song_ref.find(song_id)
		
		new_sale = Sale(user_id, song_id, date, price)
		song.quantity -= 1
		self.__data.append(new_sale)
	
	def show(self, L:list[Sale]):
		print(f"There are {len(L)} sales:")
		for sale in L: print(sale)
	
	def show_all(self):
		self.show(self.__data)

	def group_user(self):
		user_sale = defaultdict(list)
		for sale in self.__data:
			user_sale[sale.user_id].append(sale)
		user_sale_1 = {}

		for user_id, sales in user_sale.items():
			user_sale_1[user_id] = sum(list(map(lambda sale: sale.price, sales)))
		user_rp = dict(sorted(user_sale_1.items(), key=lambda x:x[1], reverse=True))
		
		return user_rp
	
	def group_song(self):
		song_sale = defaultdict(list)
		for sale in self.__data:
			song_sale[sale.song_id].append(sale)
		song_sale_1 = {}

		for song_id, sales in song_sale.items():
			song_sale_1[song_id] = sum(list(map(lambda sale: sale.price, sales)))
		song_rp = dict(sorted(song_sale_1.items(), key=lambda x:x[1], reverse=True))
		return song_rp
	
	def group_time(self):
		time_sale = defaultdict(list)
		for sale in self.__data:
			time_sale[sale.time].append(sale)
		time_sale_1 = {}

		for time, sales in time_sale.items():
			time_sale_1[time] = sum(list(map(lambda sale: sale.price, sales)))
		time_rp = dict(reversed(list(time_sale_1.items())))
		return time_rp
