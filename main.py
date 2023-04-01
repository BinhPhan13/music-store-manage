from entity_manager import *
from sale import *
import pickle
import os
import sys

if __name__ == "__main__":
	path = "./_sale.mng"
	if os.path.exists(path):
		try:
			with open(path, "rb") as file:
				sale_mng = pickle.load(file)
				user_mng = sale_mng.user_ref
				song_mng = sale_mng.song_ref
		except Exception as e:
			print(e)
			sys.exit()
	else:
		user_mng = UserManager()
		song_mng = SongManager()
		sale_mng = SaleManager(user_mng, song_mng)

	user_mng.show_all()
	song_mng.show_all()
	sale_mng.show_all()

	for i in range(3):
		song_mng.add()
	song_mng.show_all()
	user_mng.add()
	user_mng.show_all()
	sale_mng.add('user0', 'song0')
	sale_mng.add('user0', 'song4')
	sale_mng.add('user0', 'song1')
	sale_mng.add('user0', 'song0')

	
	sale_mng.show_all()
	song_mng.show_all()

	can_dump = False
	while not can_dump:
		try:
			with open(path, "wb") as file:
				pickle.dump(sale_mng, file)
			can_dump = True
		except Exception as e:
			print(e)

	
    