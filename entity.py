class Entity:
	'''Prototype for things which have a single id'''
	def __init__(self, i, name):
		self._id = i
		self._name = name
	
	def __str__(self) -> str:
		return f"{self._id:15}{self._name:10}"
	
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
	pass

class Singer(Entity):
	def __init__(self, id, name, gender):
		super().__init__(id, name)
		self.__gender = gender

	@property
	def gender(self):
		return self.__gender
	
	@gender.setter
	def gender(self, gender):
		self.__gender = gender

if __name__ == '__main__':
	pass