from entity import *

class PatternUser:
    def __init__(self, name:str, gender:str, year:tuple[int, int], phone:str):
        self.name = name
        self.gender =gender
        self.year = year
        self.phone = phone
    
class PatternSong:
    def __init__(self, name:str, singer_name:str, category:str, 
                        price:tuple[float, float], quantity:tuple[int, int]):
        self.name = name
        self.singer_name = singer_name
        self.category = category
        self.price = price
        self.quantity = quantity

class PatternSale:
    def __init__(self, user_id:str, song_id:str, time:tuple[str, str]):
        self.user_id = user_id
        self.song_id = song_id
        self.time = time

        