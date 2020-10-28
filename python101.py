print('Hello World')

def square_root(x):
	return x ** .5

print(int(square_root(64)))

def nl():
	print('\n')

#Boolean expressions
print('True and False Now')
nl()
bool1 = True
bool2 = 3*3 == 9
bool3 = False
bool4 = 3*3 != 9

print(bool1, bool2, bool3, bool4)

print(type(bool1))

#Conditianal Statements
print('Conditional Statements')

def soda(money):
	if money >= 2:
		return "You've got yourself a soda !"
	else:
		return "You don't have enough money !"
		
print(soda(10))
print(soda(1))
nl()

#Lists
print('Lists have Brackets:')
movies = ["When Harry Met Sally", "The Hangover", "The Perls of Being a Wallflower", "The Exorcist"]
print(movies[0:4])
print(movies[0:])
print(movies[:3])
print(len(movies))

movies.append("Jaws")
print(movies)

movies.pop()
print(movies)

movies.pop(1)
print(movies)

movies = ["When Harry Met Sally", "The Hangover", "The Perls of Being a Wallflower", "The Exorcist"]
person = ["Heath", "Jake", "Leah", "Jeff"]

print(person)
combinedList = zip(movies, person)
print(list(combinedList))
nl()

#Tuples
print("Tuples hace parentheses and CANNOT change")
grades = ('A', 'B', 'C', 'D', 'F')
print(grades[1])
nl()

#Looping
print('For Loops - start to finish of iterate:')
vegetables = ['cucumber', 'spinach', 'cabbage']

for x in vegetables:
	print(x)

i = 0
while i < 5:
	print(i)
	i += 1


