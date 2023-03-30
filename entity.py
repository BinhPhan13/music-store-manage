class Entity:
	'''Prototype for things which have a single id'''
	def __init__(self, i, name):
		self._id = i
		self._name = name
	
	def __str__(self) -> str:
		return f"{self._name:15}"
	
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
	def __init__(self, i, name, gender, year, phone):
		super().__init__(i, name)
		self.__gender = gender
		self.__year = year
		self.__phone = phone
	
	def __str__(self) -> str:
		extra_info = f"{self.gender:3}{self.year:6}{self.phone:15}"
		return super().__str__() + extra_info

	def __eq__(self, other: 'User') -> bool:
		match_name = self.name == other.name or not other.name
		match_gender = self.gender == other.gender or not other.gender
		match_year = self.year == other.year or not other.year
		match_phone = self.phone == other.phone or not other.phone

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

class Category(Entity):
	def __eq__(self, other:'Category'):
		return self.name == other.name or not other.name

class Singer(Entity):
	def __eq__(self, other:'Singer'):
		return self.name == other.name or not other.name

class Song(Entity):
	def __init__(self, i, name, singer:Singer, category:Category, price:float, no:int):
		super().__init__(i, name)
		self.__singer = singer
		self.__category = category
		self.__price = price
		self.__no = no
	
	def __str__(self) -> str:
		extra_info = f"{self.__singer.name:15}{str(self.__category.name):10}{self.__price:5}{self.__no:5}"
		return super().__str__() + extra_info

	def __eq__(self, other: 'Song') -> bool:
		match_name = self.name == other.name or not other.name
		match_singer = self.singer == other.singer 
		match_category = self.category == other.category
		match_price = self.price == other.price or not other.price

		return match_name and match_singer and match_category and match_price

	@property
	def singer(self):
		return self.__singer	
	@singer.setter
	def singer(self, singer:Singer):
		self.__singer = singer
	
	@property
	def category(self):
		return self.__category
	@category.setter
	def category(self, category: Category):
		self.__category = category
	
	@property
	def price(self):
		return self.__price
	@price.setter
	def price(self, price:float):
		self.__price = price
	
	@property
	def no(self):
		return self.__no
	@no.setter
	def no(self, no):
		self.__no = no

if __name__ == '__main__':
	pass