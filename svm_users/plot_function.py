from numpy import array
import matplotlib.pyplot as plt
from adjustText import adjust_text


class InputPlotObject:
    username = 'NoName :('
    x_coord = 0
    y_coord = 0

    def __init__(self, username, economic, social) -> None:
        super().__init__()
        self.username = username
        self.x_coord = economic
        self.y_coord = social


def compass_plot(data):
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
    font_label = {
        'color': 'black',
        'weight': 'normal',
        'size': 9,
    }

    # todo: adjust according to screen size
    plt.figure(figsize=(10, 10))
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

    x_axis = []
    y_axis = []
    plt_axis = [-1, 1, -1, 1]

    positions = []
    for obj in data:
        x_axis.append(obj.x_coord)
        y_axis.append(obj.y_coord)
        positions.append(plt.text(obj.x_coord, obj.y_coord, obj.username, fontdict=font_label))

    plt.margins(2, 2)
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

# proba plota

# obj1 = InputPlotObject("Korisnik 1", 0.4, -.3)
# obj2 = InputPlotObject("Korisnik 2", -0.9, 0.5)
# obj3 = InputPlotObject("Korisnik 3", 0, -0.85)

# niz = [obj1, obj2, obj3]

# compass_plot(niz)
