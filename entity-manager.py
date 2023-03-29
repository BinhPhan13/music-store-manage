from entity import *
from helper import *

'''TODO: ADD INFO VERIFICATION'''

class EntityManager:
	'''Prototype for manager of entities'''
	def __init__(self):		
		self._mng_type = 'entity'
		self._data = {}
		self._queue = []
		self._counter = 0 #for id
		self._temp_info = None
		self._temp_id = None 

	@property
	def mng_type(self):
		return self._mng_type
	
	def _create_id(self):
		if self._queue:
			i = self._queue.pop()
		else:
			i = self._counter
			self._counter += 1
		return f'{self._mng_type}{i:06}'

	def _get_info(self):
		name = input(f"- Name of the {self.mng_type}: ")
		self._temp_info = name, 
	
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
		self._get_info()
		# check for empty field -> abort
		for i in self._temp_info:
			if not i: 
				print("Contain empty fields !")
				return
		# Polymorphism here
		return 1
		
	def update(self, id):
		self._get_info()
		self._temp_id = id
	
	def delete(self, id):
		del self._data[id]

class UserManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'user'

	def _get_info(self):
		super()._get_info()
		# get gender, year, phone
		gender = input(f"- Gender of the {self.mng_type}: ")
		year = input(f"- Year of the {self.mng_type}: ")
		phone = input(f"- Phone of the {self.mng_type}: ")
			# if not verify_phone(phone): return
		# if not verify_year(year): return
		self._temp_info = (*self._temp_info, gender, year, phone)

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
		
	def update(self, id):
		super().update(id)
		updated_user = self._data[self._temp_id]
		new_name, new_gender, new_year, new_phone = self._temp_info
		if new_phone:
			result = self.search(None, None, None, new_phone)
			if result:
				print('Phone exists!')
			else:
				updated_user.phone = new_phone
				
		if new_name:
			updated_user.name = new_name
		if new_gender:
			updated_user.gender = new_gender
		if new_year:
			updated_user.year = new_year

class SingerManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'singer'
	
	def search(self, name):
		pattern_singer = Singer(None, name)
		result = [singer for singer in self._data.values() if singer == pattern_singer]
		return result

class CategoryManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'category'

	def search(self, name):
		pattern_category = Category(None, name)
		result = [category for category in self._data.values() if category == pattern_category]
		return result

class SongManager(EntityManager):
	def __init__(self, singer_manager:SingerManager, category_manager:CategoryManager):
		super().__init__()
		self._mng_type = 'song'
		self.__singer_ref = singer_manager
		self.__category_ref = category_manager
	
	def _get_info(self):
		super()._get_info()	
		singer_name = input(f"- Singer name of the {self.mng_type}: ")
		category_name = input(f"- Category of the {self.mng_type}: ")
		price = input(f"- Price of the {self.mng_type}: ")
		# verify price then convert to float
		try:
			price = round(float(price), 2)
		except ValueError:
			price = 0.0
		
		self._temp_info = (*self._temp_info, singer_name, category_name, price)
		print(self._temp_info)
		
	
	def search(self, name, singer_name, category_name, price):
		temp_singer, temp_category = Singer(None, ''), Category(None, '')
		if singer_name:
			temp_singer = Singer(None, singer_name)
		if category_name:
			temp_category = Category(None, category_name)
		
		pattern_song = Song(None, name, temp_singer, temp_category, price, None)
		result = [song for song in self._data.values() if song == pattern_song]
		return result
		

	def add(self):
		if not super().add(): return
		name, singer_name, category_name, price = self._temp_info
		n = input(f"- Number of {self.mng_type} to add: ")
		# verify no then conver to int
		n = int(n)

		# if song exist -> add to no
		# if new song:
		#	check if new category, new singer
		# 	auto add new category, singer
		#	add song
		result = self.search(name, singer_name, category_name, price)
		if result:
			self._data[result[0].id].no += n
			return 1
		
		singer = self.__singer_ref.search(singer_name)

		# if new singer -> create singer -> SingerManager add
		if not singer:
			hash_singer = self.__singer_ref._create_id()
			singer = Singer(hash_singer, singer_name)
			# auto-add
			self.__singer_ref._data[hash_singer] = singer
		else:
			singer[0].no += 1
		
		category = self.__category_ref.search(category_name)
		if not category:
			hash_category = self.__category_ref._create_id()
			category = Singer(hash_category, category_name)
			# auto-add
			self.__category_ref._data[hash_category] = category
		else:
			category[0].no += 1

		s = self._create_id()
		new_song = Song(s, name, singer, category, price, n)
		self._data[s] = new_song
	
		return 1
	
	def update(self, i):
		super().update(i)
		updated_song = self._data[self._temp_id]
		new_name, new_singer_name, new_category_name, new_price = self._temp_info
		singer_change, category_change = True, True
		if not new_name:
			new_name = updated_song.name
		if not new_singer_name:
			new_singer_name = updated_song.singer.name
			singer_change = False
		if not new_category_name:
			new_category_name = updated_song.category.name
			category_change = False
		if not new_price:
			new_price = updated_song.price
		result = self.search(new_name, new_singer_name, new_category_name, new_price)
		if result:
			print('This song already exists')
			result[0].no += updated_song.no
			self.delete(i)
			return 1
		
		singer = self.__singer_ref.search(new_singer_name)
		if not singer:
			hash_singer = self.__singer_ref._create_id()
			singer = Singer(hash_singer, new_singer_name)
			# auto-add
			self.__singer_ref._data[hash_singer] = singer
			updated_song.singer.no -= 1
		elif singer_change:
			singer = singer[0]
			singer.no += 1
			updated_song.singer.no -= 1


		category = self.__category_ref.search(new_category_name)
		if not category:
			hash_category = self.__category_ref._create_id()
			category = Category(hash_category, new_category_name)
			# auto-add
			self.__category_ref._data[hash_category] = category
			updated_song.category.no -= 1

		elif category_change:
			category = category[0]
			category.no += 1
			updated_song.category.no -= 1


		updated_song.name = new_name
		updated_song.singer = singer
		updated_song.category = category
		updated_song.price = new_price
		


	def delete(self, id):
		category = self._data[id].category
		category.no -= 1
		singer = self._data[id].singer
		singer.no -= 1
		if category.no == 0:
			self.__category_ref.delete(category.id)
		if singer.no == 0:
			self.__singer_ref.delete(singer.id)
		self._queue.append(id)
		super().delete(id)


if __name__ == "__main__":
	sgmng = SingerManager()
	ctmng = CategoryManager()
	smng = SongManager(sgmng, ctmng)
	for i in range(3):
		smng.add()
	
	sgmng.show_all()
	ctmng.show_all()
	smng.show_all()
	smng.update('song000001')
	sgmng.show_all()
	ctmng.show_all()
	smng.show_all()
	smng.delete('song000001')
	sgmng.show_all()
	ctmng.show_all()
	smng.show_all()
	# umng = UserManager()
	# for i in range(3):
	# 	umng.add()

	# umng.show(umng._data.values())
	# umng.update('user000001')
	# umng.show(umng._data.values())
	# umng.show(umng._data.values())
