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

l, r = map(int, input().split())
count = 0

i = 1
while i * i <= r:
    sq = i * i
    if l <= sq <= r:
        count += 1
    i += 1

print(count)