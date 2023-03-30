from entity import *
from helper import hash_phone, hash_name

'''TODO: ADD INFO VERIFICATION'''

class EntityManager:
	'''Prototype for manager of entities'''
	def __init__(self):		
		self._mng_type = 'entity'
		self._data = {}
		self._temp_info = None
		self._temp_id = None 

	@property
	def mng_type(self):
		return self._mng_type

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

		self._temp_info = (*self._temp_info, gender, year, phone)

	# use this if no id is provided
	def search(self):
		self._get_info()
		name, gender, year, phone = self._temp_info
		
		if phone: result = [self.find('u' + hash_phone(phone))]
		else:
			pattern_user = User(None, name, gender, year, None)
			result = [user for user in self._data.values() if user == pattern_user]

		if not result:
			print("No result!")
		else:		
			self.show(result)

	def add(self):
		if not super().add(): return
		name, gender, year, phone = self._temp_info
		s = 'u' + hash_phone(phone)
		if self.find(s):
			print(s)
			print("User exists!")
			return 
		
		new_user = User(s, name, gender, year, phone)
		self._data[s] = new_user
		return 1
		
	def update(self, id):
		super().update(id)
		updated_user = self._data[self._temp_id]
		new_name, new_gender, new_year, _ = self._temp_info
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

class CategoryManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'category'

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
		
	
	def search(self):
		self._get_info()
		name, singer_name, category_name, price = self._temp_info
		# if full attributes -> convert to id
		if name and singer_name and category_name and price:
			hash_singer = hash_name(singer_name)
			hash_category = hash_name(category_name)
			s = hash_name(name) + hash_singer + hash_category + str(price)
			result = [self.find(s)]
		else:
			temp_singer, temp_category = Singer(None, ''), Category(None, '')
			if singer_name:
				temp_singer = Singer(None, singer_name)
			if category_name:
				temp_category = Category(None, category_name)
			
			pattern_song = Song(None, name, temp_singer, temp_category, price, None)
			result = [song for song in self._data.values() if song == pattern_song]

		if not result:
			print("No result!")
		else: 
			self.show(result)
		

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
		hash_singer = hash_name(singer_name)
		hash_category = hash_name(category_name)
		s = hash_name(name) + hash_singer + hash_category + str(price)
		if self.find(s):
			self._data[s].no += n
			return 1
		
		singer = self.__singer_ref.find(hash_singer)
		# if new singer -> create singer -> SingerManager add
		if not singer:
			singer = Singer(hash_singer, singer_name)
			# auto-add
			self.__singer_ref._data[hash_singer] = singer
		

		category = self.__category_ref.find(hash_category)
		# if new category -> create category -> CategoryManager add
		if not self.__category_ref.find(hash_category):
			category = Category(hash_category, category_name)
			# auto-add
			self.__category_ref._data[hash_category] = category


		new_song = Song(s, name, singer, category, price, n)
		self._data[s] = new_song
	
		return 1



if __name__ == "__main__":
	sgmng = SingerManager()
	ctmng = CategoryManager()
	smng = SongManager(sgmng, ctmng)
	for i in range(4):
		smng.add()
	
	sgmng.show_all()
	ctmng.show_all()
	smng.show_all()

	smng.search()
	# umng = UserManager()
	# for i in range(5):
	# 	umng.add()

	# umng.show(umng._data.values())
	# umng.update('u46017')
	# umng.show(umng._data.values())
	# umng.delete('u46017')
	# umng.show(umng._data.values())
