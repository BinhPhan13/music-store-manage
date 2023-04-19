import re

# only consider from MIN_INT + 1 to MAX_INT
MIN_INT = -1
MAX_INT = 10_000_000


def capitalize_name(name:str):
	'''Capitalize input name'''
	names = name.split(' ')
	names = list(map(str.capitalize, names))
	names = [a for a in names if a]
	return ' '.join(names)


def process_int(s:str):	
	y = s.split('_')
	if len(y) == 1: y += y

	if not y[0]: y[0] =	str(MIN_INT)
	if not y[1]: y[1] = str(MAX_INT)

	if is_int(y[0]) and is_int(y[1]):
		return (int(y[0]), int(y[1]))
	
	return (MIN_INT, MIN_INT)


def process_float(price:str):
	p = price.split('_')
	if len(p) == 1: p += p

	if not p[0]: p[0] = str(MIN_INT)
	if not p[1]: p[1] = str(MAX_INT)

	if is_float(p[0]) and is_float(p[1]):
		return (float(p[0]), float(p[1]))
	return (float(MIN_INT), float(MIN_INT))

def is_int(s:str):
	try:
		x = int(s)
		return str(x) == s # float can be convert to int
	except ValueError:
		return False

def is_float(s:str):
	try:
		s = float(s)
		return True
	except ValueError:
		return False

def verify_name(s: str):
    pattern = r'^[a-z A-Z]*$'
    if re.match(pattern, s): return True
    return False

def verify_phone(s: str):
    pattern = r'^(03|05|07|08|09)[0-9]{8}$'
    if re.match(pattern, s): return True
    return False

def verify_year(s: str):
    return (is_int(s) and (int(s) > 1800 and int(s) <= 2023))

def verify_price(s: str):
	return is_float(s) and (float(s) > 0  and float(s) <= MAX_INT)

def verify_quantity(s: str):
	return is_int(s) and (int(s) > 0 and int(s) <= MAX_INT)


# only consider from MIN_DATE + 1 to MAX_DATE
MIN_DATE = '31/12/2009'
MAX_DATE = '01/01/5000'

def process_time(time:str):
	t = time.split('_')
	if len(t) == 1: t += t
	
	if not t[0]: t[0] = MIN_DATE
	if not t[1]: t[1] = MAX_DATE

	if is_date(t[0]) and is_date(t[1]):
		return (t[0], t[1])
	
	return (MIN_DATE, MIN_DATE)

def reverse_date(date:str):
	if not is_date(date): return

	day, month, year = date.split('/')
	
	return '/'.join([year, month, day])


def is_date(date:str):
	from datetime import datetime
	try:
		datetime.strptime(date, "%d/%m/%Y")
		return True
	except ValueError:
		return False



if __name__ == "__main__":
	pass
	