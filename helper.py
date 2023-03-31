''' TODO:Add state to hashes function'''
import re
import random


def verify_name(s: str):
    pattern = r'^[a-z A-Z]*$'
    if re.match(pattern, s): return True
    return False

def verify_phone(s: str):
    pattern = r'^(03|05|07|08|09)[0-9]{8}$'
    if re.match(pattern, s) or not s: return True
    return False

def verify_year(s: str):
    if (s.isdigit() and (int(s) > 1800 and int(s) <= 2023)) or s == '': return True
    else: return False

def verify_price(s: str):
	try:
		if s == '': return True
		s = float(s)
		if s > 0: return True
		return False
	except ValueError:
		return False

def verify_number(s: str):
	return s == '' or (s.isdigit() and int(s) > 0)


if __name__ == "__main__":
	print(verify_number(2.33))