# Basics patterns and syntax of Python functions

# Basic function structure
def fibonacci(N):
	L = []
	a, b = 0, 1
	while len(L) < N:
		a, b = b, a + b
		L.append(a)
	return L
print('Basic Fibonacci:')
print(fibonacci(10))
print(fibonacci(100))


# Function with default args
def fibonacci(N, a=0, b=1):
	L = []
	while len(L) < N:
		a, b = b, a + b
		L.append(a)
	return L

print('\n\n')
print('Fibonacci with default args:')
print(fibonacci(10, 8, 13))


# Args passed from the command line
def catch_all(*args, **kwargs):
	print("args = ", args)
	print("kwargs = ", kwargs)
print('catch_all(1, 2, 3, a=4, b=5)')
catch_all(1, 2, 3, a=4, b=5)