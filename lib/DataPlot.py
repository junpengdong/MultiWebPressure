import matplotlib.pyplot as plt
import operator
import os
import json

__all__ = 'PerformanceDataPlot',


class PerformanceDataPlot:

    def __init__(self, s, c, f):
        self.__function = f
        self.__sequence_key = 'sequence'
        self.__sequence_json = 'sequence.json'
        self.__plot_name = '%s_%s.png'
        self.__base_dir = '../image/%s/%s/%s/' % (s, c, f)
        plt.figure(figsize=(16, 8))
        plt.title('%s WebPressure Data' % f, fontsize=20)
        plt.ylabel('Response Time(ms)', fontsize=18)
        plt.xlabel('Request Times', fontsize=18)
        plt.tick_params(labelsize=16)

    def data_plot(self, y):
        x = [i for i in range(1, len(y) + 1)]
        min_index, min_value = min(enumerate(y), key=operator.itemgetter(1))
        max_index, max_value = max(enumerate(y), key=operator.itemgetter(1))
        self.__point_line(x, y)
        plt.annotate(str(min_value), xy=(min_index + 1, min_value))
        plt.annotate(str(max_value), xy=(max_index + 1, max_value))
        self.save_image()
        plt.show()

    @staticmethod
    def __point_line(x, y, color='red', label=None):
        plt.plot(x, y, '.-', color=color, label=label)

    @staticmethod
    def __line(x, y, color='red', line_width=2, line_style='--'):
        plt.plot(x, y, color=color, linewidth=line_width, linestyle=line_style)

    def save_image(self):
        sequence = 1
        if not os.path.exists(self.__base_dir):
            os.makedirs(self.__base_dir)
            with open(self.__base_dir + self.__sequence_json, 'w') as json_file:
                json.dump({self.__sequence_key: sequence}, json_file, indent=4)
        else:
            with open(self.__base_dir + self.__sequence_json, 'r') as json_str:
                sequence = json.load(json_str).get(self.__sequence_key) + 1
            with open(self.__base_dir + self.__sequence_json, 'w') as json_file:
                json.dump({self.__sequence_key: sequence}, json_file, indent=4)
        plt.savefig(self.__base_dir + (self.__plot_name % (self.__function, sequence)))
