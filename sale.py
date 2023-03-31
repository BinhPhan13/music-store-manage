from entity_manager import *
from collections import defaultdict
class Sale:
	def __init__(self, user_id, song_id):
		self.__user_id = user_id
		self.__song_id = song_id
		self.__times = []

	def __str__(self) -> str:
		return f"{self.user_id:15}{self.song_id:15}{str(self.times):10}"
	def __eq__(self, other: 'Sale'):
		match_user = self.user_id == other.user_id or not other.user_id
		match_song = self.song_id == other.song_id or not other.song_id
		return match_user and match_song
	@property
	def user_id(self):
		return self.__user_id
	@user_id.setter
	def user_id(self, i):
		self.__user_id = i	
	@property
	def song_id(self):
		return self.__song_id
	@song_id.setter
	def song_id(self, i):
		self.__song_id = i
	@property
	def times(self):
		return self.__times


class SaleManager:
	def __init__(self, user_manager:UserManager, song_manager:SongManager):
		self.__user_ref = user_manager
		self.__song_ref = song_manager
		self.__data = []

	def search(self, user_id, song_id):
		pattern_sale = Sale(user_id, song_id)
		return [sale for sale in self.__data if sale == pattern_sale]
	
	def add(self, user_id, song_id, buy_time):
		result = self.search(user_id, song_id)
		if result: 
			result[0].times.append(buy_time)
			return 1
		
		new_sale = Sale(user_id, song_id)
		price = self.__song_ref.find(song_id).price
		new_sale.times.append((buy_time, price))
		self.__data.append(new_sale)
		return 1
	
	def refresh(self):
		for data in self.__data:
			if data[0] not in self.__user_ref._data.keys():
				data[0] = None
			if data[1] not in self.__song_ref._data.keys():
				data[1] = None
	
	def show(self, L:list[Sale]):
		print(f"There are {len(L)} sales:")
		for sale in L: print(sale)
	
	def show_all(self):
		self.show(self.__data)

	# calculate total spend from users
	def user_money(self):
		user_sale = defaultdict(list)
		for sale in self.__data:
			user_sale[sale.user_id].append(sale)
		for user_id, sales in user_sale.items():
			user_sale[user_id] = sum(list(map(lambda sale: sale.times[1], sales)))

if __name__ == "__main__":
	user_mng = UserManager()
	song_mng = SongManager()
	sale_mng = SaleManager(user_mng, song_mng)

	for i in range(3):
		song_mng.add()
	song_mng.show_all()
	user_mng.add()
	for song_id in song_mng._data.keys():
		sale_mng.add(list(user_mng._data.keys())[0], song_id, f't{song_id}')
	
	sale_mng.show_all()
	song_mng.update('song000000')
	print(song_mng._queue)
	song_mng.show_all() 
	sale_mng.show_all()
	sale_mng.refresh()
	sale_mng.show_all()