def hash_phone(s:str) -> str:
    hash_list = [str((int(c)+3)%10) for c in s]
    return ''.join(hash_list)


if __name__ == "__main__":
    print(hash_phone('012123231237128371239'))