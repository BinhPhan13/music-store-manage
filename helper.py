''' TODO:Add state to hashes function'''

def hash_phone(s:str) -> str:
    hash_list = [str((int(c)+3)%10) for c in s]
    return ''.join(hash_list)

def hash_character(c):
    return chr(ord('a') + (ord(c) + 13)%26)

def hash_name(s: str) -> str:
    hash_list = [hash_character(c) for c in s if c != ' ']
    return ''.join(hash_list)

if __name__ == "__main__":
    print(hash_phone('012123231237128371239'))
    print(hash_name('phan thanh binh'))