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

	def find(self, e_id:str):
		if e_id in self._data.keys():
			return self._data[e_id]
		else:
			return None
	
	def show(self):
		print(f"There are {len(self._data)} {self._mng_type}s:")
		for e in self._data.values():
			print(e)
