#!/bin/python3

#Importing
print("Importing is important:")

import sys #system function and parameters

from datetime import datetime
print(datetime.now())

from datetime import datetime as dt #importing with an alias
print(dt.now())

def nl():
	print('\n')

nl()

#Advanced Strings
print('Advanced strings:')
my_name = "Heath"
print(my_name[0]) #first initial

sentence = "This is a sentence."
print(sentence[:4]) # first word
print(sentence[-9:-1])# last word

print(sentence.split()) #split sentence by delimiter (space)

sentence_split = sentence.split()
print(sentence_split)
sentence_join = " ".join(sentence_split)
print(sentence_join)

quoteception = "I said, 'Give me all the money'"
print(quoteception)

quoteception = "I said, \"Give me all the money\""
print(quoteception)

print("A" in "Apple")
letter = "a"
word = 'Apple'
print(letter in word.lower())

nl()

#Dictionaries
print('Dictionaries are keys and values:')
drinks = {"White Russions": 7, "Olf Fashion": 10, "Lemon Drop":8, "Buttery Nipple": 6}
print(drinks)

employees = {'Finance': ['Bob', 'Linda', 'Tina'], "IT" : ['Gene', 'Louise', 'Teddy'], "HR": ['Jimmy', 'Mort']}
print(employees)

employees['Legal'] = ['Mr. Frond']
print(employees)
