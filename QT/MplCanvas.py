from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import numpy as np


class MplCanvas:
    def __init__(self, qwidget, x_date, y_value):
        self.fig = Figure()
        self.x = x_date
        self.y = y_value

        self.axes = self.fig.add_subplot(111)
        self.axes.plot(self.x, self.y)
        self.axes.set_xlim(self.x[0], self.x[-1])

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        self.fig.autofmt_xdate()

        self.axes.set_title('Results of saimulation')
        self.axes.set_xlabel('Dates')
        self.axes.set_ylabel('Values ($)')

        self.canvas = FigureCanvas(self.fig)
        qwidget.addWidget(self.canvas)
        self.canvas.draw()

    def update_plot(self, date, value):
        np.append(self.x, date)
        np.append(self.y, value)

        self.axes.cla()
        self.axes.plot(self.x, self.y)
        self.canvas.draw()
