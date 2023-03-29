import re
# Entity and subclasses
class Entity:
	'''Prototype for things which have a single id'''
	def __init__(self, i, name):
		self._id = i
		self._name = name
	
	def __str__(self) -> str:
		return f"{self._id:15}{self._name:25}"
	
	@property
	def id(self):
		return self._id
	
	@property
	def name(self):
		return self._name

class Admin(Entity):
	def	__init__(self, id, name, pw):
		super().__init__(id, name)
		self.__pw = pw
	
	@property
	def pw(self):
		return self.__pw
	
class User(Entity):
	def __init__(self, id, name, gender = None, email = None, year = None):
		super().__init__(id, name)
		self.__gender = gender
		self.__email = email
		self.__year = year

	@property
	def gender(self):
		return self.__gender
	
	@gender.setter
	def gender(self, gender):
		self.__gender = gender

	@property
	def email(self):
		return self.__email
	
	@email.setter
	def email(self, email):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
		if not re.match(regex, email):
			print('Invalid email!')

		else:
			self.__email = email
		
	@property
	def year(self):
		return self.__year
	
	@year.setter
	def year(self, year):
		if year < 0 or year > 2024 : print('Invalid year')
		else: self.__year = year

class Category(Entity):
	pass

class Singer(Entity):
	def __init__(self, id, name, gender = None):
		super().__init__(id, name)
		self.__gender = gender

	@property
	def gender(self):
		return self.__gender
	
	@gender.setter
	def gender(self, gender):
		self.__gender = gender


# EntityManager and subclasses
class EntityManager:
	'''Prototype for manager of entities'''
	def __init__(self):		
		self._data = {}
		self._mng_type = 'entity'

	@property
	def mng_type(self):
		return self._mng_type
	
	def add(self):
		pass

	def get_info(self):
		e_id = input(f"- ID of the {self._mng_type} to add: ")
		result = self.find(e_id)
		if result:
			print(f"That {self._mng_type} already exists so cannot add!")
			return None		
		
		e_name = input(f"- Name of the {self._mng_type} to add: ")
		return e_id, e_name

	def update(self):
		pass

	def delete(self):
		pass

	def find(self, e_id:str) -> (Entity | None):
		if e_id in self._data.keys():
			return self._data[e_id]
		else:
			return None
	
	def show(self):
		print(f"There are {len(self._data)} {self._mng_type}s:")
		for e in self._data.values():
			print(e)

class AdminManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'admin'

	def add(self):
		info = self.get_info()
		if info is None: return

		admin_id, admin_name = info
		admin_pw = input('- Password: ')
		new_admin = Admin(admin_id, admin_name, admin_pw)
		self._data[admin_id] = new_admin

	def login(self):
		result = self.find(input('Enter ID: '))
		pw = input('Enter password: ')
		if result:
			if result.pw == pw: print('Login successfully')
			else: print('Wrong password')
		else:
			print('The ID does not exist')

	def logout(self):
		pass

class UserManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'user'

	def add(self):
		info = self.get_info()
		if info is None: return

		user_id, user_name = info
		new_user = User(user_id, user_name)
		self._data[user_id] = new_user

	def update(self):
		user = self.find(input('Enter the user ID you want to update: '))
		if user:
			while True:
				req = input('You want to update: ')
				if req == 'gender':
					user.gender = input('Enter gender: ')
				elif req == 'email':
					user.email = input('Enter email: ')
				elif req == 'year':
					user.year = int(input('Enter year: '))
				else: break
		else: print('The user does not exist')

	def delete(self):
		id = input('Enter the user ID you want to delete: ')
		user = self.find(id)
		if user:
			del self._data[id]
		else: 
			print('The user does not exist')

class CategoryManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'category'

	def add(self):
		info = self.get_info()
		if info is None: return

		category_id, category_name = info
		category = Category(category_id, category_name)
		self._data[category_id] = category

	def delete(self):
		id = input('Enter the category ID you want to delete: ')
		category = self.find(id)
		if category:
			del self._data[id]
		else: 
			print('The category does not exist')

class SingerManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'singer'
	def add(self):
		info = self.get_info()
		if info is None: return

		singer_id, singer_name = info
		singer = Singer(singer_id, singer_name)
		self._data[singer_id] = singer

	def update(self):
		singer = self.find(input('Enter the singer ID you want to update: '))
		if singer:
			singer.gender = input('Enter the gender')
		else: 
			print('The singer does not exist')

	def delete(self):
		id = input('Enter the singer ID you want to delete: ')
		singer = self.find(id)
		if singer:
			del self._data[id]
		else: 
			print('The singer does not exist')


if __name__ == '__main__':
	# admin = AdminManager()
	# admin.add()
	# admin.add()
	# admin.login()

	user = UserManager()
	user.add()
	user.add()
	user.show()
	user.update()
	user.show()
	user.delete()
	user.show()