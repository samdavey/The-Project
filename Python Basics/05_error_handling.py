# Basic error handling

# try .. except
try:
	print('the bit in the "try" statement gets executed first.')
except:
	print('the bit in the "else" statement gets executed on an error.')

# try .. except with specific error handling
try:
	print('Stand back, I\'m about to divide by zero!')
	x = 1 / 0
except ZeroDivisionError as err:
	print('You divided by zero, fool!')
	print('Error class is: ', type(err))
	print('Error message is: ', err)
else:
	print('Pinted only if it magically succeeds.')
finally:
	print('the bit in the finally statement is printed no matter what.')