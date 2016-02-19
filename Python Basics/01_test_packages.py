print('Begin testing package availability. Will say "Done" when complete.')


print('Testing availability of NumPy')
try:
	import numpy as np
	print('NumPy installed.\n')
except:
	print('!!! NumPy is NOT installed.\nUse "pip install numpy" on the commandline to install.')


print('Testing availability of MatPlotLib')
try:
	import matplotlib as pl
	print('MatPlotLib installed.\n')
except:
	print('!!! MatPlotLib is NOT installed.\nUse "pip install matplotlib" on the commandline to install.')


print('Testing availability of Pandas')
try:
	import pandas as pd
	print('Pandas installed.\n')
except:
	print('!!! Pandas is NOT installed.\nUse "pip install pandas" on the commandline to install.')

print('Testing availability of SciKit-Learn')
try:
	import sklearn as sk
	print('SciKit-Learn installed.\n\n')
except:
	print('!!! SciKit-Learn is NOT installed.\nUse "pip install sklearn" on the commandline to install.')

print('Done.')
