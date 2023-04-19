from entity import *
from pattern import PatternUser, PatternSong
from helper import *

class EntityManager:
	'''Prototype for manager of entities'''
	def __init__(self):		
		self._mng_type = 'entity'
		self._data = {}
		self._counter = 0 # to generate ids
		self._temp_info:tuple[str, ...] = None # store result of _get_info()
		self._temp_entity = None  # store selection of update()

	@property
	def values(self):
		return self._data.values()
	
	def _create_id(self):
		'''Auto create id'''
		i = f"{self._mng_type}{self._counter}"
		self._counter += 1		
		return i

	def get_info(self, *args):
		self._temp_info = args
	
	def find(self, i):
		return self._data.get(i)

	def show(self, L: list[Entity]):
		print(f"There are {len(L)} {self._mng_type}s: ")
		for e in L: print(e)

	def show_all(self):
		self.show(self.values)

	def search(self):
		pass

	def add(self):
		# check for empty field -> abort
		if '' in self._temp_info:
			return "Contain empty fields!"
		return
		
	def update(self, i):
		self._temp_entity = self.find(i)
		
		
	def delete(self, i):
		del self._data[i]	

class UserManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'user'

	def search(self, name, gender, year, phone) -> list[User]:
		# if all fields are empty -> return all values
		name = capitalize_name(name)
		gender = capitalize_name(gender)
		if not (name or gender or year or phone):
			return self.values
		
		year = process_int(year)

		pattern_user = PatternUser(name, gender, year, phone)
		result = [user for user in self.values if user == pattern_user]

		return result

	def add(self):
		message = super().add()
		if message: return message

	# PULL FROM TEMP INFO AND VERIFY ALL FIELDS
		name, gender, year, phone = self._temp_info

		if not verify_name(name):
			return "Invalid name!"
		if not verify_year(year):
			return "Invalid year!"
		if not verify_phone(phone):
			return "Invalid phone!"

		result = self.search('', '', '', phone)
		if result:
			return 'User exists!'
		
		name = capitalize_name(name)
		year = int(year)
		s = self._create_id()
		new_user = User(s, name, gender, year, phone)
		self._data[s] = new_user
		return 
		
	def update(self, i):
		super().update(i)
		new_name, new_gender, new_year, new_phone = self._temp_info

		self._temp_entity:User = self._temp_entity # type hints purpose

	# IF THERE ARE NON-EMPTY FIELDS -> VERIFY AND UPDATE
		if new_phone:
			if not verify_phone(new_phone):
				return "Invalid phone!"

			result = self.search('', '', '', new_phone)
			if result: return 'Phone exists!'
			self._temp_entity.phone = new_phone
		
		if new_name:
			if not verify_name(new_name):
				return "Invalid name!"
			new_name = capitalize_name(new_name)
			self._temp_entity.name = new_name

		if new_gender:
			self._temp_entity.gender = new_gender

		if new_year:
			if not verify_year(new_year):
				return "Invalid year!"
			new_year = int(new_year)
			self._temp_entity.year = new_year
		return

	def count_gender(self):
		male_counter = 0
		for user in self.values:
			male_counter+=1 if user.gender == "Male" else 0
			print(male_counter)
		return male_counter, len(self._data) - male_counter
	
	def count_age(self):
		age1_counter = 0 # <18
		age2_counter = 0 # 18-30
		age3_counter = 0 # >30
		for user in self.values:
			if 2023 - user.year < 18:
				age1_counter+=1
			elif 2023 - user.year > 30:
				age3_counter+=1
			else:
				age2_counter+=1
		
		return age1_counter, age2_counter, age3_counter
		
class SongManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'song'


	def search(self, name, singer_name, category, price, quantity) -> list[Song]:
		name  = capitalize_name(name)
		singer_name = capitalize_name(singer_name)
		category = capitalize_name(category)
		
		if not (name or singer_name or category or price or quantity):
			return self.values
	
		price = process_float(price)
		quantity = process_int(quantity)
	
		pattern_song = PatternSong(name, singer_name, category, price, quantity)
		result = [song for song in self.values if song == pattern_song]

		return result
	
	def add(self):
		message = super().add()
		if message: return message

	# PULL FROM TEMP INFO AND VERIFY ALL FIELDS
		name, singer_name, category, price, quantity = self._temp_info

		if not verify_name(name):
			return "Invalid name!"
		if not verify_name(singer_name):
			return "Invalid singer name!"
		if not verify_name(category):
			return "Invalid category!"
		if not verify_price(price):
			return "Invalid price!"
		if not verify_quantity(quantity):
			return "Invalid quantity"
		
	# IF SONG ALREADY EXIST -> ONLY ADD QUANTITY
		name = capitalize_name(name)
		singer_name = capitalize_name(singer_name)
		category = capitalize_name(category)

		result = self.search(name, singer_name, category, price, '')
		if result:
			result[0].quantity += int(quantity)
			return
		
		s = self._create_id()
		
		name = capitalize_name(name)
		singer_name = capitalize_name(singer_name)
		category = capitalize_name(category)
		price = float(price)
		quantity = int(quantity)

		new_song = Song(s, name, singer_name, category, price, quantity)
		self._data[s] = new_song
		return
	
	def update(self, i):
		super().update(i)
		new_name, new_singer_name, new_category,  \
		new_price, new_quantity = self._temp_info

		self._temp_entity:Song = self._temp_entity # type hints purpose

		if new_name:
			if not verify_name(new_name):
				return "Invalid name!"
			new_name = capitalize_name(new_name)
			self._temp_entity.name = new_name
		if new_singer_name:
			if not verify_name(new_singer_name):
				return "Invalid singer name!"
			new_singer_name = capitalize_name(new_singer_name)
			self._temp_entity.singer_name = new_singer_name
		if new_category:
			if not verify_name(new_category):
				return "Invalid category!"
			new_category = capitalize_name(new_category)
			self._temp_entity.category = new_category
		if new_price:
			if not verify_price(new_price):
				return "Invalid price!"
			new_price = float(new_price)
			self._temp_entity.price = new_price
		if new_quantity:
			if not verify_quantity(new_quantity):
				return "Invalid quantity!"
			new_quantity = int(new_quantity)
			self._temp_entity.quantity = new_quantity

	# CHECK IF AFTER UPDATED SONG ALREADY IN DATA
		result = self.search(self._temp_entity.name, self._temp_entity.singer_name, 
		       				self._temp_entity.category, str(self._temp_entity.price), '')
		
	# result size can only be 1(found the same song), 2(same song in data)
		if len(result) == 2:
			result[0].quantity += result[1].quantity
			del self._data[result[1].id]
	
	def group(self):
		singer_group: dict[str, list[Song]] = {}
		category_group: dict[str, list[Song]] = {}

		for song in self.values:
			singer = song.singer_name
			category = song.category
			singer_group[singer] = singer_group.get(singer, [])
			singer_group[singer].append(song)			
			category_group[category] = category_group.get(category, [])
			category_group[category].append(song)

		return singer_group, category_group
			