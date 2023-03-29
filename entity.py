import re
from abstract import Entity, EntityManager

class Admin(Entity):
	def	__init__(self, i, name, pw):
		super().__init__(i, name)
		self.__pw = pw
	
	@property
	def pw(self):
		return self.__pw
	
class User(Entity):
	def __init__(self, i, name, gender = None, email = None, year = None):
		super().__init__(i, name)
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