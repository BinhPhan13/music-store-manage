from entity import *
from helper import *

class EntityManager:
	'''Prototype for manager of entities'''
	def __init__(self):		
		self._mng_type = 'entity'
		self._data = {}
		self._counter = 0 # to generate ids
		self._temp_info = None # store result of _get_info()
		self._temp_id = None  # store selection of update()

	@property
	def mng_type(self):
		return self._mng_type
	
	def _create_id(self):
		'''Auto create id'''
		i = f"{self._mng_type}{self._counter}"
		self._counter += 1		
		return i

	def _get_info(self):
		name = input(f"- Name of the {self.mng_type}: ").strip()
		if not verify_name(name): 
			print("Invalid name!")
			return 
		self._temp_info = name, 
		return 1
	
	def find(self, i):
		return self._data.get(i)

	def show(self, L: list[Entity]):
		print(f"There are {len(L)} {self.mng_type}s: ")
		for e in L: print(e)

	def show_all(self):
		self.show(self._data.values())

	def search(self):
		pass

	def add(self):
		'''Return 1 if suceed else None'''
		if not self._get_info(): return
		# check for empty field -> abort
		for i in self._temp_info:
			if not i: 
				print("Contain empty fields!")
				return
		# Polymorphism here
		return 1
		
	def update(self, i):
		self._temp_id = i
		if not self._get_info(): return
		return 1
	
	def delete(self, i):
		del self._data[i]	
		return 1

class UserManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'user'

	def _get_info(self):
		if not super()._get_info(): return
		# get gender, year, phone
		gender = input(f"- Gender of the {self.mng_type}: ").strip()

		year = input(f"- Year of the {self.mng_type}: ").strip()
		if not verify_year(year):
			print("Invalid year!")
			return
		
		phone = input(f"- Phone of the {self.mng_type}: ").strip()
		if not verify_phone(phone):
			print("Invalid phone!")
			return
	
		self._temp_info = (*self._temp_info, gender, year, phone)
		return 1

	# use this if no id is provided
	def search(self, name, gender, year, phone):
		
		pattern_user = User(None, name, gender, year, phone)
		result = [user for user in self._data.values() if user == pattern_user]

		return result
	
	def add(self):
		if not super().add(): return
		name, gender, year, phone = self._temp_info
		result = self.search(None, None, None, phone)
		if result:
			print('User exists!')
			return
		s = self._create_id()
		new_user = User(s, name, gender, year, phone)
		self._data[s] = new_user
		return 1
		
	def update(self, i):
		if not super().update(i): return
		updated_user = self._data[self._temp_id]
		new_name, new_gender, new_year, new_phone = self._temp_info
		if new_phone:
			result = self.search(None, None, None, new_phone)
			if result:
				print('Phone exists!')
				return
			updated_user.phone = new_phone
		
		if new_name:
			updated_user.name = new_name
		if new_gender:
			updated_user.gender = new_gender
		if new_year:
			updated_user.year = new_year
		return 1


class SongManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'song'
	
	def _get_info(self):
		if not super()._get_info(): return
		singer_name = input(f"- Singer name of the {self.mng_type}: ").strip()
		if not verify_name(singer_name):
			print("Invalid singer name!")
			return

		category = input(f"- Category of the {self.mng_type}: ").strip()
		if not verify_name(category):
			print("Invalid category!")
			return
		
		price = input(f"- Price of the {self.mng_type}: ").strip()
		if not verify_price(price):
			print("Invalid price!")
			return
		price = round(float(price), 2) if price else 0.0
				
		self._temp_info = (*self._temp_info, singer_name, category, price)
		return 1
			
	def search(self, name, singer_name, category, price):
		pattern_song = Song(None, name, singer_name, category, price)
		result = [stock for stock in self._data.values() if stock.song == pattern_song]
		return result
	
	def add(self):
		if not super().add(): return
		name, singer_name, category, price = self._temp_info

		n = input(f"- Number of {self.mng_type} to add: ").strip()
		if not verify_number(n):
			print("Invalid number!")
			return
		n = int(n)

		result = self.search(name, singer_name, category, price)
		if result:
			result[0].n += n
			return 1
		
		s = self._create_id()
		new_song = Song(s, name, singer_name, category, price)
		new_stock = SongStock(new_song, n)
		self._data[s] = new_stock
		return 1
	
	def update(self, i):
		if not super().update(i): return
		updated_stock = self._data[i]
		name, singer_name, category, price = self._temp_info

		if not name: name = updated_stock.song.name
		if not singer_name: singer_name = updated_stock.song.singer_name
		if not category: category = updated_stock.song.category
		if not price: price = updated_stock.song.price

		result = self.search(name, singer_name, category, price)
		if result:
			result[0].n += updated_stock.n
			del self._data[i]
		else:
			updated_stock.song.name = name
			updated_stock.song.singer_name = singer_name
			updated_stock.song.category = category
			updated_stock.song.price = price
		
		return 1
	
	def show(self, L: list[tuple[Song, int]]):
		print(f"There are {len(L)} {self.mng_type}s: ")
		for stock in L: print(f"{str(stock.song)}{stock.n:10}")


		
		
if __name__ == "__main__":
	smng = SongManager()
	for i in range(4):
		smng.add()
	
	smng.show_all()
	smng.update('song1')
	smng.show_all()
	smng.update('song0')
	smng.show_all()
	# umng = UserManager()
	# for i in range(5):
		# umng.add()

	# umng.show(umng._data.values())
	# umng.update('user000000')
	# umng.show_all()
	# umng.delete('user000001')
	# umng.show_all()
	# umng.add()
	# umng.show_all()