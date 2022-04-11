from numpy import array
import matplotlib.pyplot as plt
from adjustText import adjust_text
import csv

SR_LANGUAGE = 'sr'
EN_LANGUAGE = 'en'

class InputLanguagePlotObject:
    username = 'NoName :('
    x_coord = 0
    y_coord = 0
    tweet_language = 'Undefined :('

    def __init__(self, username, economic, social, tweet_language) -> None:
        super().__init__()
        self.username = username
        self.x_coord = economic
        self.y_coord = social
        self.tweet_language = tweet_language


def compass_language_plot(data):
    font_title = {
        'color': 'black',
        'weight': 'normal',
        'size': 20,
    }
    font_axis = {
        'color': 'black',
        'weight': 'normal',
        'size': 16,
    }
    font_label_cyr = {
        'color': 'red',
        'weight': 'normal',
        'size': 7,
    }
    font_label_lat = {
        'color': 'blue',
        'weight': 'normal',
        'size': 9,
    }
    font_label_eng = {
        'color': 'black',
        'weight': 'normal',
        'size': 11,
    }

    # todo: adjust according to screen size
    plt.figure(figsize=(10, 10))
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

    x_axis = []
    y_axis = []
    positions = []
    for obj in data:
        x_axis.append(obj.x_coord)
        y_axis.append(obj.y_coord)
        lan_font = font_label_cyr if obj.tweet_language == SR_LANGUAGE else (font_label_eng if obj.tweet_language == EN_LANGUAGE else font_label_lat)
        positions.append(plt.text(obj.x_coord, obj.y_coord, obj.username, fontdict=lan_font))
    plt_axis = [-1, 1, -1, 1]

    plt.legend(loc="upper left")

    plt.margins(1, 1)
    plt.axis(plt_axis)
    plt.scatter(x_axis, y_axis)
    plt.fill_between([0, 1], 0, 1, alpha=0.3, color='#1F98D0')  # Blue
    plt.fill_between([-1, 0], 0, 1, alpha=0.3, color='#FF7373')  # Red
    plt.fill_between([-1, 0], -1, 0, alpha=0.3, color='#8AFF73')  # Green
    plt.fill_between([0, 1], -1, 0, alpha=0.3, color='#FFEC73')  # Yellow

    plt.title(label='Political Compass', fontdict=font_title)
    plt.xlabel(xlabel='Economic policy', fontdict=font_axis)
    plt.ylabel(ylabel='Social policy', fontdict=font_axis)

    plt.grid(True)
	

    adjust_text(positions, arrowprops=dict(arrowstyle="->", color='r', lw=0.5),
                precision=0.01)  # force_text=(0.3, 0.5) force_points=(0.5, 0.5)

    plt.show()

# Defining main function
def main():
	with open('tweets_with_sentiment_2.csv', newline='', encoding='utf-8') as csvfile:
		distinct_dict = dict()
		user_dict = dict()
		obj_array = []
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['username'] not in distinct_dict:
				user_dict[row['username']] = (float(row['economic_policy']), float(row['social_policy']))
				distinct_dict[row['username']] = {}
			if row['language'] not in distinct_dict[row['username']]:
				distinct_dict[row['username']][row['language']] = 1
			else:
				distinct_dict[row['username']][row['language']] += 1
		

		# Odabrati najcesce koriscen jezik kao glavni za mapiranje
		for username in distinct_dict:
			print(username)
			max = 0
			lan = ''
			for language in distinct_dict[username]:
				print({language: distinct_dict[username][language]})
				if max < distinct_dict[username][language]:
					max = distinct_dict[username][language]
					lan = language
			obj = InputLanguagePlotObject(username, user_dict[username][0], user_dict[username][1], lan)
			print({ 'username': obj.username, 'economic_policy': obj.x_coord, 'social_policy': obj.y_coord, 'language': obj.tweet_language})
			obj_array.append(obj)

		print(len(obj_array))
		compass_language_plot(obj_array)
			
	

  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()

# proba plota

# obj1 = InputPlotObject("Korisnik 1", 0.4, -.3)
# obj2 = InputPlotObject("Korisnik 2", -0.9, 0.5)
# obj3 = InputPlotObject("Korisnik 3", 0, -0.85)

# niz = [obj1, obj2, obj3]

# compass_plot(niz)
