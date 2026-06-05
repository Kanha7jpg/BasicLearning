fruits = ['banana', 'orange', 'mango', 'lemon']
fruits[0] = 'avocado'
print(fruits)       #  ['avocado', 'orange', 'mango', 'lemon']
fruits[1] = 'apple'
print(fruits)       #  ['avocado', 'apple', 'mango', 'lemon']
#last_index = len(fruits) - 1
fruits[-1] = 'lime'
print(fruits)        #  ['avocado', 'apple', 'mango', 'lime']

print(fruits[-1])

print('banana' in fruits) 