from pattern import PatternUser, PatternSong
class Entity:
	'''Prototype for things which have a single id'''
	def __init__(self, i:str, name:str):
		self._id = i
		self._name = name
	
	def __str__(self) -> str:
		return f"{self.id:15}{self.name:15}"
	
	@property
	def id(self):
		return self._id
	
	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, name):
		self._name = name

class User(Entity):
	def __init__(self, i, name, gender:str, year:int, phone:str):
		super().__init__(i, name)
		self.__gender = gender
		self.__year = year
		self.__phone = phone
	
	def __str__(self) -> str:
		extra_info = f"{self.gender:10}{self.year:10}{self.phone:15}"
		return super().__str__() + extra_info

	def __eq__(self, pattern: PatternUser) -> bool:
		match_name = self.name == pattern.name or not pattern.name
		match_gender = self.gender == pattern.gender or not pattern.gender
		match_phone = self.phone == pattern.phone or not pattern.phone
		
		match_year = self.year >= pattern.year[0] and self.year <= pattern.year[1]

		return match_name and match_gender and match_year and match_phone

	@property
	def gender(self):
		return self.__gender
	
	@gender.setter
	def gender(self, gender):
		self.__gender = gender

	@property
	def phone(self):
		return self.__phone
	
	@phone.setter
	def phone(self, phone):	
		self.__phone = phone
		
	@property
	def year(self):
		return self.__year
	
	@year.setter
	def year(self, year):
		self.__year = year

class Song(Entity):
	def __init__(self, i, name, singer_name:str, category:str, price:float, quantity:int):
		super().__init__(i, name)
		self.__singer_name = singer_name
		self.__category = category
		self.__price = price
		self.__quantity = quantity
	
	def __str__(self) -> str:
		extra_info = f"{self.__singer_name:15}{self.__category:10}{self.__price:5}"
		return super().__str__() + extra_info

	def __eq__(self, pattern: PatternSong) -> bool:
		match_name = self.name == pattern.name or not pattern.name
		match_singer = self.singer_name == pattern.singer_name or not pattern.singer_name 
		match_category = self.category == pattern.category or not pattern.category

		match_price = self.price >= pattern.price[0] and self.price <= pattern.price[1]
		match_quantity = self.quantity >= pattern.quantity[0] and self.quantity <= pattern.quantity[1]

		return match_name and match_singer and match_category and match_price and match_quantity

	@property
	def singer_name(self):
		return self.__singer_name	
	@singer_name.setter
	def singer_name(self, singer_name):
		self.__singer_name = singer_name
	
	@property
	def category(self):
		return self.__category
	@category.setter
	def category(self, category):
		self.__category = category
	
	@property
	def price(self):
		return self.__price
	@price.setter
	def price(self, price:float):
		self.__price = price

	@property
	def quantity(self):
		return self.__quantity
	@quantity.setter
	def quantity(self, n:int):
		self.__quantity = n
