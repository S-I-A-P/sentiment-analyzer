from numpy import array
import matplotlib.pyplot as plt
from adjustText import adjust_text
import csv

class InputResultPlotObject:
    username = 'NoName :('
    x_coord = 0
    y_coord = 0
    hit = False

    def __init__(self, username, economic, social, hit) -> None:
        super().__init__()
        self.username = username
        self.x_coord = economic
        self.y_coord = social
        self.hit = hit

    def toString(self):
        print({'username': self.username, 'x_coord': self.x_coord, 'y_coord': self.y_coord, 'hit': self.hit})


def compass_result_plot(data):
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
    font_label_correct = {
        'color': 'green',
        'weight': 'normal',
        'size': 10,
    }
    font_label_incorrect = {
        'color': 'red',
        'weight': 'normal',
        'size': 8,
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
        print(obj.hit == 'True')
        if obj.hit == 'True':
            hit_font = font_label_correct
        else:
            hit_font = font_label_incorrect
        positions.append(plt.text(obj.x_coord, obj.y_coord, obj.username, fontdict=hit_font))
    plt_axis = [-1, 1, -1, 1]

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
	with open('results2.csv', newline='', encoding='utf-8') as csvfile:
		obj_array = []
		reader = csv.DictReader(csvfile)
		for row in reader:
			obj = InputResultPlotObject(row['username'], float(row['result_x']), float(row['result_y']), row['hit'])
			print({ 'username': obj.username, 'economic_policy': obj.x_coord, 'social_policy': obj.y_coord, 'hit': obj.hit})
			obj_array.append(obj)

		print(len(obj_array))
		compass_result_plot(obj_array)
			
	
if __name__=="__main__":
    main()

