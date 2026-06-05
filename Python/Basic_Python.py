firstmame = "sam"
lastname = "smith"
fullname = firstmame + " " + lastname
print(fullname)

country = "finland"
city = "helsinki"
location = country + " " + city
print(location)

age = 22


#Creating a String

letter = 'P'                # A string could be a single character or a bunch of texts
print(letter)               # P
print(len(letter))          # 1
greeting = 'Hello, World!'  # String could be made using a single or double quote,"Hello, World!"
print(greeting)         

multiline_string = '''I am a teacher and enjoy teaching.
I didn't find anything as rewarding as empowering people.
That is why I created 30 days of python.'''
print(multiline_string)


#String concatenation

first_name = 'Asabeneh'
last_name = 'Yetayeh'
full_name = first_name  +  ' ' + last_name
print(full_name) # Asabeneh Yetayeh


#Tab means 8 spaces (at columns 9, 17, 25, 33, 41, etc.)

print('Day 1\t5\t5')
print('Day 2\t6\t20')
print('Day 3\t5\t23')
print('Day 4\t1\t35')

#Expanding Tabs in Strings
challenge = 'thirty\tdays\tof\tpython'
print(challenge.expandtabs())   # 'thirty  days    of      python'
print(challenge.expandtabs(10)) # 'thirty    days      of        python'

#Accessing Characters in Strings by Index

language = 'Python'
first_letter = language[0]
print(first_letter) # P
last_letter = language[-1]
print(last_letter) # n


#Slicing Python Strings

language = 'Python'
first_three = language[0:3]
print(first_three) # Pyt
last_three = language[-3:]
print(last_three)   # hon

#Skipping Characters in Strings
pto = language[0:6:2] 
print(pto) # Pto


#Reversing a String

greeting = 'Hello, World!'
print(greeting[::-1]) # !dlroW ,olleH



