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


#Lists

fruits = ['banana', 'orange', 'mango', 'lemon']                     # list of fruits
vegetables = ['Tomato', 'Potato', 'Cabbage','Onion', 'Carrot']      # list of vegetables
animal_products = ['milk', 'meat', 'butter', 'yoghurt']             # list of animal products
web_techs = ['HTML', 'CSS', 'JS', 'React','Redux', 'Node', 'MongDB'] # list of web technologies
countries = ['Finland', 'Estonia', 'Denmark', 'Sweden', 'Norway'] 

# Print the lists and its length
print('Fruits:', fruits)
print('Number of fruits:', len(fruits))


#accessing list items by index
fruits = ['banana', 'orange', 'mango', 'lemon']
first_fruit = fruits[0] 
last_fruit = fruits[-1]
print(first_fruit)      # banana
print(last_fruit)       # lemon


#slicing lists
fruits = ['banana', 'orange', 'mango', 'lemon']
all_fruits = fruits[0:4] # banana, orange, mango, lemon
fr = fruits[1:4] # orange, mango, lemon
all_fruits = fruits[0:] # banana, orange, mango, lemon
orange_and_mango = fruits[1:3] # orange, mango
orange_mango_lemon = fruits[1:] # orange, mango, lemon
orange_and_lemon = fruits[::2] # banana, mango


#modifying list items
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits[0] = 'avocado'
print(fruits)       #  ['avocado', 'orange', 'mango', 'lemon']
fruits[1] = 'apple'
print(fruits)       #  ['avocado', 'apple', 'mango', 'lemon']
last_index = len(fruits) - 1
fruits[last_index] = 'lime'
fruits[-1] = 'lime' # also works
print(fruits)        #  ['avocado', 'apple', 'mango', 'lime']


#append items to a list
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.append('apple')
print(fruits)           # ['banana', 'orange', 'mango', 'lemon', 'apple']


#insert items to a list
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.insert(2, 'apple') # insert apple between orange and mango
print(fruits)           # ['banana', 'orange', 'apple', 'mango', 'lemon']
fruits.insert(3, 'lime')   # ['banana', 'orange', 'apple', 'lime', 'mango', 'lemon']
print(fruits)

#remove items from a list
fruits = ['banana', 'orange', 'mango', 'lemon', 'banana']
fruits.remove('banana')
print(fruits)  # ['orange', 'mango', 'lemon', 'banana']

#removing using pop
fruits = ['banana', 'orange', 'mango', 'lemon']
fruits.pop()
print(fruits)       # ['banana', 'orange', 'mango']
fruits.pop(0)
print(fruits)       # ['orange', 'mango']

