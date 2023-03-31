''' TODO:Add state to hashes function'''
import re
import random

def hash_phone(s:str) -> str:
    state = random.randint(0,10)
    hash_list = [str((int(c)+3)%10) for c in s]
    return ''.join(hash_list)

def hash_character(c):
    state = random.randint(0,10)
    return chr(ord('a') + (ord(c) + 13)%26)

def hash_name(s: str) -> str:
    hash_list = [hash_character(c) for c in s if c != ' ']
    return ''.join(hash_list)


def verify_phone(s: str):
    pattern = r'^09[0-9]{8}$'
    if re.match(pattern, s): return True
    else: return False

def verify_year(s: str):
    if s.isdigit() and (int(s) > 0 or int(s) <= 2023): return True
    else: return False

if __name__ == "__main__":
    print(hash_phone('012123231237128371239'))
    print(hash_name('phan thanh binh'))