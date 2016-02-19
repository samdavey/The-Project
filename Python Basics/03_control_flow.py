print('basic control flow patterns\n\n')

print('if, elif, else')
x = 0
if x == 0:
	print('x == 0')
elif x == 1:
	print('x == 1')
else:
	print('x <> 0 and x <> 1')
print('done\n\n')

print(' for loops')
for n in [2, 3, 5, 7]:
	print(n, end=' ')
print('\ndone\n\n')

print(' for loop based on default range')
for n in range(15):
	print(n, end=' ')
print('\ndone\n\n')

print(' for loop beased on specifed range 5-15')
for n in range(5, 15):
	print(n, end=' ')
print('\ndone\n\n')

print(' for loop beased on range 0-15 with step of 3')
for n in range(0, 15, 3):
	print(n, end=' ')
print('\ndone\n\n')

print(' while loops')
i = 0
while i < 20:
	print(i, end=', ')
	i += 1
print('\ndone\n\n')

print(' for loop using continue to skip evens')
for i in range(20):
	# check if i is even
	if i % 2 == 0:
		continue
	print(i, end=', ')
print('\ndone\n\n')

print('While loop using break to make fibonacci sequence to 100')
a, b = 0, 1
amax = 100
L = []

while True:
	(a, b) = (b, a + b)
	if a > amax:
		break
	L.append(a)
print(L)

print('Loop using else, triggered iff loop ends naturally')
L = []
nmax = 30

for n in range(2, nmax):
	for factor in L:
		if n % factor == 0:
			break
	else: # no break
		L.append(n)
print(L)
