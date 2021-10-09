import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

from matplotlib import pyplot as plt
import numpy as np

y_of_slice = [0.2, 0.44, 0.65, 0.8, 0.9, 0.95, 0.99]


class Data:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


datafile = "C:/Users/iesm0/Documents/CFD/second/onera_forces_bin.plt"
dataset = tp.data.load_tecplot(datafile)


def get_slice(i):
    frame = tp.active_frame()
    frame.plot_type = tp.constant.PlotType.Cartesian3D
    frame.plot().show_contour = True
    extracted_slice = tp.data.extract.extract_slice(
        origin=(0, 0.0, i),
        normal=(0, 0, 1),
        source=tp.constant.SliceSource.SurfaceZones,
        dataset=dataset)
    extracted_slice.name = 'z-slice-1'
    x = extracted_slice.values('x').as_numpy_array()
    fnorm = extracted_slice.values('fnorm').as_numpy_array()
    tmp = min(x)
    x = list(map(lambda t: t - tmp, x))
    tmp = max(x)
    x = list(map(lambda t: t / tmp, x))
    return x, fnorm


def experiment(i, m, M):
    name = 'cp' + str(i) + 'l.txt'
    x1, y1 = get_theory(name)
    name = 'cp' + str(i) + 'u.txt'
    x2, y2 = get_theory(name)
    y1 = list(map(lambda t: -t, y1))
    y2 = list(map(lambda t: -t, y2))
    m_ = min(min(y1), min(y2))
    M_ = max(max(y1), max(y2))
    k = (M - m) / (M_ - m_)
    y1 = list(map(lambda t: t * k, y1))
    y2 = list(map(lambda t: t * k, y2))
    m_ = min(min(y1), min(y2))
    tmp = m - m_
    y1 = list(map(lambda t: t + tmp, y1))
    y2 = list(map(lambda t: t + tmp, y2))
    return Data(x1, y1, x2, y2)


def get_theory(name):
    f = open('./exp/' + name, 'r')
    x = []
    y = []
    for line in f:
        tmp = list(map(float, line.split()))[:2]
        if len(tmp) == 0:
            break
        x.append(tmp[0])
        y.append(tmp[1])
    return x, y


for i in range(7):
    print(i)
    x, y = get_slice(y_of_slice[i])
    plt.scatter(x, y, c='b', marker='s',
                label='numeric_' + str(i + 1))
    exp_data = experiment(i + 1, min(y), max(y))
    plt.scatter(exp_data.x1, exp_data.y1, c='r', marker='o',
                label='exp_low_' + str(i + 1))
    plt.scatter(exp_data.x2, exp_data.y2, c='g', marker='o',
                label='exp_upper_' + str(i + 1))
    plt.xlabel("x")
    plt.ylabel("fnorm")
    plt.legend()
    plt.grid(True)
    txt: str = 'Position(y/b): ' + str(y_of_slice[i])
    plt.text(0.5, 0.9 * max(y), txt, horizontalalignment='center', fontsize=15)
    plt.savefig('./rez/' + str(i + 1) + '.png', dpi=150, bbox_inches='tight')
    plt.close()
    # plt.show()
