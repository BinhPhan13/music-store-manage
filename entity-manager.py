from entity import *
from helper import hash_phone

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
	


if __name__ == "__main__":
	umng = UserManager()
	for i in range(5):
		umng.add()

	umng.show(umng._data.values())
	umng.update('u46017')
	umng.show(umng._data.values())
	umng.delete('u46017')
	umng.show(umng._data.values())
