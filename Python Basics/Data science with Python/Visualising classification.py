## General imports
#%matplotlib inline
import matplotlib.pyplot as plt 
#import seaborn; seaborn.set()
import numpy as np 
import time
time.sleep(5)
import os
#if not os.path.exists('fig'):
#	os.makedirs('fig')

## Common plot formatting
def format_plot(ax,title):
	ax.xaxis.set_major_formatter(plt.NullFormatter())
	ax.yaxis.set_major_formatter(plt.NullFormatter())
	ax.set_xlabel('feature 1',color='gray')
	ax.set_ylabel('feature 2',color='gray')
	ax.set_title(title, color='gray')

## Classification imports
from sklearn.datasets.samples_generator import make_blobs
from sklearn.svm import SVC

#create 50 separable points
X,y = make_blobs(n_samples=50, centres=2, 
				random_state=0, cluster_std=0.60)

#Fit the support vector classifier model
clf = SVC(kernel='linear')
clf.fit(X,y)

#create new points to predict
X2, _ = make_blobs(n_samples=80, centers=2,random_state=0, cluster_std=0.80)
X2 = X2[50:]

#Predict the labels
y2 = clf.predict(X2)
time.sleep(5)

#Plot the data
fig, ax = plt.subplots(figsize=(8, 6))
point_style = dict(cmap='Paired', s=50)
ax.scatter(X[:,0], X[:, 1], c=y, **point_style)

#Format plot
format_plot(ax, 'Input Data')
ax.axis([-1,4,-2,7])
fig.savefig('fig/07.01-classification-1.png')
plt.close(fig)