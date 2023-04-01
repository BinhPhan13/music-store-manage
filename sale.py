from entity_manager import *
from entity import *
from datetime import datetime

class Sale:
	def __init__(self, user_id:User, song_id:Song, time, price):
		self.__user = user_id
		self.__song = song_id
		self.__time = time
		self.__price = price

	def __str__(self) -> str:
		return f"{self.user_id:15}{self.song_id:15}{self.time:10}{self.__price:10}"

	def __eq__(self, other: 'Sale'):
		match_user = self.user_id == other.user_id or not other.user_id
		match_song = self.song_id == other.song_id or not other.song_id
		match_time = self.time == other.time or not other.time
		match_price = self.price == other.price or not other.price
		return match_user and match_song and match_time and match_price
	
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
		self.__data = []

	@property
	def user_ref(self):
		return self.__user_ref
	@property
	def song_ref(self):
		return self.__song_ref
	def search(self, user_id, song_id, time, price):
		pattern_sale = Sale(user_id, song_id, time, price)
		return [sale for sale in self.__data if sale == pattern_sale]
	
	def add(self, user_id, song_id):
		if not (user_id or song_id): 
			print("Must include both user and song!")
			return
		user = self.__user_ref.find(user_id)
		song_stock = self.__song_ref.find(song_id)
		if not user:
			print("User not exist!")
			return
		if not song_stock:
			print("Song not exist!")
			return
		if not song_stock.n:
			print(f"Out of stock for {song_stock.song.id}!")
			return
		
		new_sale = Sale(user_id, song_id, datetime.now().strftime("%c"), song_stock.song.price)
		song_stock.n -= 1
		self.__data.append(new_sale)
		return 1
	
	def show(self, L:list[Sale]):
		print(f"There are {len(L)} sales:")
		for sale in L: print(sale)
	
	def show_all(self):
		self.show(self.__data)

	# calculate total spend from users
	# def user_money(self):
	# 	user_sale = defaultdict(list)
	# 	for sale in self.__data:
	# 		user_sale[sale.user_id].append(sale)
	# 	user_sale_1 = {}

	# 	for user_id, sales in user_sale.items():
	# 		user_sale_1[user_id] = sum(list(map(lambda sale: sum(list(map(lambda sa: sa[1], sale.times))), sales)))
	# 	return user_sale_1

if __name__ == "__main__":
	user_mng = UserManager()
	song_mng = SongManager()
	sale_mng = SaleManager(user_mng, song_mng)

	for i in range(3):
		song_mng.add()
	song_mng.show_all()
	user_mng.add()
	user_mng.show_all()
	sale_mng.add('user0', 'song0')
	sale_mng.add('user0', 'song4')
	sale_mng.add('user0', 'song1')
	sale_mng.add('user0', 'song0')

	
	sale_mng.show_all()
	song_mng.show_all()
	sale_mng.show(sale_mng.search('', 'song0', '', ''))
	