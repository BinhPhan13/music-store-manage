import re
from collections import defaultdict
import numpy as np

# Entity and subclasses
class Entity:
	# Prototype for things which have a single id
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
	
	@name.setter
	def name(self, name):
		self._name = name

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
		regex = '[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)'
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


class Song(Entity):
	def __init__(self, id, name, category, singer, price, stock):
		super().__init__(id, name)
		self.__category = category
		self.__singer = singer
		self.__price = price
		self.__stock = stock

	@property
	def category(self):
		return self.__category
	
	@property
	def singer(self):
		return self.__singer
	
	@property
	def price(self):
		return self.__price
	
	@price.setter
	def price(self, price):
		if price >= 0:
			self.__price = price
		else:
			print('Invalid price')	

	@property
	def stock(self):
		return self.__stock
	
	@stock.setter
	def stock(self, stock):
		if stock >= 0:
			self.__stock = stock
		else:
			print('Invalid number of stocks')

	
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



class SongManager(EntityManager):
	def __init__(self):
		super().__init__()
		self._mng_type = 'song'

	def update(self):
		song = self.find(input('Enter the song ID you want to update: '))
		if song:
			while True:
				req = input('You want to update: ')
				if req == 'price':
					song.price = input('Enter gender: ')
				elif req == 'stock':
					song.stock = input('Enter email: ')
				else: break
		else: print('The song does not exist')

	def add(self):
		info = self.get_info()
		if info is None: return

		song_id, song_name = info
		self._data[song_id] = Song(song_id, song_name,
			     					input('- Song category: '),
								    input('- Song singer: '),
			     					float(input('- Song price: ')),
									int(input('- Song stocks: ')))

	def delete(self):
		id = input('Enter the song ID you want to delete: ')
		song = self.find(id)
		if song:
			del self._data[id]
		else: 
			print('The user does not exist')
		
# Connector and subclasses
class Connector:
	def __init__(self, e1:Entity, e2:Entity):
		self.e1 = e1
		self.e2 = e2
		self.data = None

class Purchase(Connector):
	def __init__(self, user: User, song: Song):
		super().__init__(user, song)
	
	def __str__(self) -> str:
		return f"User {self.e2.name}" + \
			f" have bought {self.e1.name} for {(self.data)} disks."
	
class ConnectorManager:
	def __init__(self, e_mng1:EntityManager, e_mng2:EntityManager):
		# reference managers
		self.ref1 = e_mng1
		self.ref2 = e_mng2

		self.data : list[Connector] = []

	def get_info(self):
		i1 = input(f"- ID of the {self.ref1.mng_type}: ")
		e1 = self.ref1.find(i1)
		if not e1:
			print(f"That {self.ref1.mng_type} not exists!")
			return None

		i2 = input(f"- ID of the {self.ref2.mng_type}: ")
		e2 = self.ref2.find(i2)
		if not e2:
			print(f"That {self.ref2.mng_type} not exists!")
			return None

		return e1, e2

	def find(self, e1_id, e2_id):
		result = None
		for connector in self.data:
			if connector.e1.id == e1_id and \
				connector.e2.id == e2_id:

				result = connector
				break
		return result
	
	def show(self):
		print(f'There are in total {len(self.data)} purchases')
		for purchase in self.data:
			print(f'- {purchase}')

	def add(self):
		pass

class PurchaseManager(ConnectorManager):
	def add(self):
		info = self.get_info()
		if not info: return

		user, song = info
		new_purchase = Purchase(user, song)
		new_purchase.data = int(input('- Number of disks: '))
		song.stock -= new_purchase.data
		if(song.stock < 0):
			print('Invalid purchase')
		else:
			self.data.append(new_purchase)
			return new_purchase
	
	def bills(self):
		new_purchase = self.add()
		price = new_purchase.e2.price * new_purchase.data
		print(f'The total price is: {price}')

	def report_user(self, user_id):
		#total money from 1 user
		user_purchase = defaultdict(list)
		for purchase in self.data:
			user_purchase[purchase.e1.id].append(purchase)
		user_id = input('Enter the user ID you want to check: ')
		if user_id in user_purchase.keys():
			return sum(list(map(lambda purchase: purchase.e2.price*purchase.data, user_purchase[user_id])))

if __name__ == '__main__':
	user_manager = UserManager()
	user_manager.add()
	user_manager.add()

	song_manager = SongManager()
	song_manager.add()
	song_manager.add()

	purchase_manager = PurchaseManager(user_manager, song_manager)
	purchase_manager.add()
	purchase_manager.show()
	purchase_manager.bills()
	print(purchase_manager.report_user(3))
