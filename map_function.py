import csv
import matplotlib.pyplot as plt
from adjustText import adjust_text 
import numpy as np

def plotCompass(fileName='tweets_with_sentiment.csv'):
	fontTitle = {
					'color':  'black',
					'weight': 'normal',
					'size': 20,
					}

	fontAxis = {
					'color':  'black',
					'weight': 'normal',
					'size': 16,
					}

	fontLabel = {
					'color':  'black',
					'weight': 'normal',
					'size': 6,
					}

	x_axis = []
	y_axis = []
	person_labels = []
	plt_axis = [-1, 1, -1, 1]

	plt.axhline(0, color='black')
	plt.axvline(0, color='black')
	txt = []
	with open(fileName, 'r', newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
					if row['username'] in person_labels:
							continue
					x = float(row['economic_policy'])
					y = float(row['social_policy'])
					x_axis.append(x)
					y_axis.append(y)
					person_labels.append(row['username'])
					txt.append(plt.text(x,y,row['username'], fontdict=fontLabel))
					
	plt.margins(2,2)
	plt.axis(plt_axis)
	plt.scatter(x_axis, y_axis)
	plt.fill_between([0,1], 0, 1, alpha=0.3, color='#1F98D0')   #Blue
	plt.fill_between([-1,0], 0, 1, alpha=0.3, color='#FF7373')  #Red
	plt.fill_between([-1,0], -1, 0, alpha=0.3, color='#8AFF73') #Green
	plt.fill_between([0,1], -1, 0, alpha=0.3, color='#FFEC73')  #Yellow

	if fileName=='tweets_with_sentiment.csv':
		plt.title(label='Political Compass - Training', fontdict=fontTitle)
	else:
		plt.title(label='Political Compass - Test', fontdict=fontTitle)
	plt.xlabel(xlabel='Economic policy', fontdict=fontAxis)
	plt.ylabel(ylabel='Social policy', fontdict=fontAxis)
	plt.grid(True)
	adjust_text(txt, arrowprops=dict(arrowstyle="->", color='r', lw=0.5), precision=0.01) # force_text=(0.3, 0.5) force_points=(0.5, 0.5)
	plt.show()