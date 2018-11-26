# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 10:26:07 2017

@author: dhamilton
"""
import sys
import numpy as np
from collections import defaultdict

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

LARGE_FONT = ("Verdana", 12)
# dark_background ggplot presentation
style.use("ggplot")

figure = Figure(figsize=(5, 4), dpi=100)
a = figure.add_subplot(111)


class Bamboo:
    def __init__(self, growthRate):
        self.growthRate = int(growthRate)
        self.currentHeight = 0

    def grow(self):
        self.currentHeight = self.currentHeight + self.growthRate

    def cut(self, cut):
        self.currentHeight = self.currentHeight - cut

    def state(self):
        print(self.currentHeight)


def animate(i):
    yData = np.random.randint(20, size=8)
    xData = [1, 2, 3, 4, 5, 6, 7, 8]
    a.clear()
    a.plot(xData, yData)


class BambooApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="appicon.ico")
        tk.Tk.wm_title(self, "Bamboo App")

        # App Container
        container = tk.Frame(self)
        container.grid(sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = AppPage(container, self)

        self.frames[AppPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(AppPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class AppPage(tk.Frame):
    H = 0
    totalVolume = 0
    bambooCollection = {}
    bambooResults = defaultdict(list)
    algorithm = "MH"

    def update_algorithm(self, alg):
        self.algorithm = alg

        for widget in self.algFrame.winfo_children():
            widget.destroy()

        algNotification = ttk.Label(self.algFrame, text=self.algorithm, font=LARGE_FONT, justify='center')
        algNotification.grid(row=0, column=0, sticky="nsew", padx=10)

    def __init__(self, parent, controller):

        CONFIG_X_PADDING = 10
        CONFIG_Y_PADDING = 10

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Bamboo App", font=LARGE_FONT, justify='center')
        label.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10, padx=10)

        algorithmController = ttk.LabelFrame(self, text="Algorithm Configuration")
        algorithmController.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew", padx=CONFIG_X_PADDING,
                                 pady=CONFIG_Y_PADDING)

        bambooGrowthSpeedLabel = ttk.Label(algorithmController, text="Bamboo Growth Rate: ")
        bambooGrowthSpeedLabel.grid(row=1, column=0, sticky="w", padx=CONFIG_X_PADDING)
        self.bambooGrowthRateEntry = ttk.Entry(algorithmController, justify='left')
        self.bambooGrowthRateEntry.grid(row=1, column=1, sticky="we")
        addBambooButton = ttk.Button(algorithmController, text="Add Bamboo", command=lambda: self.addBamboo())
        addBambooButton.grid(row=1, column=2, sticky="w", padx=CONFIG_X_PADDING, pady=CONFIG_Y_PADDING)

        algorithmOptionLabel = ttk.Label(algorithmController, text="Select Algorithm: ")
        algorithmOptionLabel.grid(row=3, column=0, sticky="w", padx=CONFIG_X_PADDING)
        algorithmOption1 = ttk.Radiobutton(algorithmController, text="MH", variable=self.algorithm, value="MH",
                                           command=lambda: self.update_algorithm("MH"))
        algorithmOption1.grid(row=3, column=1, sticky="w", padx=CONFIG_X_PADDING)
        algorithmOption1.invoke()
        algorithmOption2 = ttk.Radiobutton(algorithmController, text="MGR", variable=self.algorithm, value="MGR",
                                           command=lambda: self.update_algorithm("MGR"))
        algorithmOption2.grid(row=3, column=2, sticky="w", padx=CONFIG_X_PADDING)

        self.bambooFrame = ttk.LabelFrame(self, text="Bamboos")
        self.bambooFrame.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=CONFIG_X_PADDING,
                              pady=CONFIG_Y_PADDING)
        bambooNotification = ttk.Label(self.bambooFrame, text="No Bamboos.")
        bambooNotification.grid(row=0, column=0, sticky="nsew", padx=CONFIG_X_PADDING)

        self.hFrame = ttk.LabelFrame(self, text="H")
        self.hFrame.grid(row=4, column=1, sticky="nsew", padx=CONFIG_X_PADDING,
                         pady=CONFIG_Y_PADDING)
        hNotification = ttk.Label(self.hFrame, text="N/A", font=LARGE_FONT, justify='center')
        hNotification.grid(row=0, column=0, sticky="nsew", padx=CONFIG_X_PADDING)


        self.totalVolumeFrame = ttk.LabelFrame(self, text="V")
        self.totalVolumeFrame.grid(row=4, column=2, sticky="nsew", padx=CONFIG_X_PADDING,
                         pady=CONFIG_Y_PADDING)
        tVNotification = ttk.Label(self.totalVolumeFrame, text="N/A", font=LARGE_FONT, justify='center')
        tVNotification.grid(row=0, column=0, sticky="nsew", padx=CONFIG_X_PADDING)



        self.algFrame = ttk.LabelFrame(self, text="Algorithm")
        self.algFrame.grid(row=4, column=3, sticky="nsew", padx=CONFIG_X_PADDING,
                           pady=CONFIG_Y_PADDING)
        algNotification = ttk.Label(self.algFrame, text=self.algorithm, font=LARGE_FONT, justify='center')
        algNotification.grid(row=0, column=0, sticky="nsew", padx=CONFIG_X_PADDING)

        runAlgorithmButton = ttk.Button(self, text="Run", command=lambda: self.execute())
        runAlgorithmButton.grid(row=5, column=0, columnspan=2, sticky="w", padx=CONFIG_X_PADDING,
                                pady=CONFIG_Y_PADDING)

        resetAlgorithmButton = ttk.Button(self, text="Reset", command=lambda: self.reset_algorithm())
        resetAlgorithmButton.grid(row=5, column=2, sticky="w", padx=CONFIG_X_PADDING,
                                  pady=CONFIG_Y_PADDING)

        self.output = tk.Text(self, wrap="word", width=50)
        self.output.grid(row=6, column=0, columnspan=3, sticky="w", padx=CONFIG_X_PADDING, pady=CONFIG_Y_PADDING)

        self.canvasFrame = ttk.LabelFrame(self, text="Results")
        self.canvasFrame.grid(row=6, column=4, sticky="nsew", padx=CONFIG_X_PADDING,
                              pady=CONFIG_Y_PADDING)

        self.canvas = FigureCanvasTkAgg(figure, self.canvasFrame)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=6, column=4, rowspan=3, sticky="w", padx=CONFIG_X_PADDING,
                                         pady=CONFIG_Y_PADDING)

        sys.stdout = TextRedirector(self.output, "stdout")
        # sys.stderr = TextRedirector(self.output, "stderr")

        # self.configure_algorithm(2, "MGR")

    def addBamboo(self):

        updatedH = 0

        if len(self.bambooCollection) > 0:
            self.bambooCollection[len(self.bambooCollection)] = Bamboo(self.bambooGrowthRateEntry.get())
        else:
            self.bambooCollection[0] = Bamboo(self.bambooGrowthRateEntry.get())

        for widget in self.bambooFrame.winfo_children():
            widget.destroy()

        for bamboo in self.bambooCollection:
            updatedH += int(self.bambooCollection[bamboo].growthRate)
            bambooText = "Bamboo " + str(bamboo) + ": Growth Rate " + str(self.bambooCollection[bamboo].growthRate)
            ttk.Label(self.bambooFrame, text=bambooText) \
                .grid(row=bamboo, column=0, sticky="nsew", padx=10)
            # print(str(self.bambooCollection[bamboo].growthRate))

        for widget in self.hFrame.winfo_children():
            widget.destroy()

        hNotification = ttk.Label(self.hFrame, text=updatedH, font=LARGE_FONT, justify='center')
        hNotification.grid(row=0, column=0, sticky="nsew", padx=10)

        for widget in self.totalVolumeFrame.winfo_children():
            widget.destroy()

        self.totalVolume = len(self.bambooCollection) * self.H

        tVNotification = ttk.Label(self.totalVolumeFrame, text=str(self.totalVolume), font=LARGE_FONT, justify='center')
        tVNotification.grid(row=0, column=0, sticky="nsew", padx=10)

        self.H = updatedH

    def reset_algorithm(self):
        CONFIG_X_PADDING = 10
        CONFIG_Y_PADDING = 10

        self.bambooCollection.clear()
        # RESET BAMBOO
        self.bambooFrame = ttk.LabelFrame(self, text="Bamboos")
        self.bambooFrame.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=CONFIG_X_PADDING,
                              pady=CONFIG_Y_PADDING)
        bambooNotification = ttk.Label(self.bambooFrame, text="No Bamboos.")
        bambooNotification.grid(row=0, column=0, sticky="nsew", padx=CONFIG_X_PADDING)

        # RESET H
        self.H = 0

        # RESET V
        self.totalVolume = 0

        for widget in self.hFrame.winfo_children():
            widget.destroy()

        hNotification = ttk.Label(self.hFrame, text=self.H, font=LARGE_FONT, justify='center')
        hNotification.grid(row=0, column=0, sticky="nsew", padx=10)

        a.clear()
        self.canvas.draw()

        self.clean_output()

    def clean_output(self):
        self.output.destroy()
        self.output = tk.Text(self, wrap="word", width=50)
        self.output.grid(row=6, column=0, columnspan=3, sticky="w", padx=10, pady=10)
        sys.stdout = TextRedirector(self.output, "stdout")

        for bamboo in self.bambooCollection:
            self.bambooCollection[bamboo].currentHeight = 0

    def plot_results(self):

        a.clear()
        a.axhline(y=self.H, color='k', linestyle='-')
        xData = np.arange(self.iteration)
        #print(self.bambooResults)
        for key in self.bambooResults:
            yData = self.bambooResults[key]
            a.plot(xData, yData, label="Bamboo " + str(key))

        # Place a legend above this subplot, expanding itself to
        # fully use the given bounding box.
        a.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                 ncol=3, mode="expand", borderaxespad=0.)

        self.canvas.draw()

    def execute(self):
        self.repeat = 0
        self.clean_output()
        self.bambooResults.clear()

        if (len(self.bambooCollection) < 2):
            print("There needs to be 2 or more bamboos.")

        else:
            self.iteration = 0
            terminate = True
            while terminate:
                self.step()
                self.state()

                if self.iteration >= self.H:
                    stateMatch = True
                    #config after pump priming, where all or all but one are below H
                    for bambooIndex in self.bambooResults:
                        if self.bambooResults[bambooIndex][self.iteration] != self.bambooResults[bambooIndex][self.iteration-(self.H)]:
                            stateMatch = False

                    if stateMatch:
                        print("------- Finished Cutting --------")
                        terminate = False

                self.iteration += 1
                #if self.iteration == 20:
                #    terminate = False


        self.plot_results()

    def state(self):
        state = str(self.iteration) + ": "
        for bamboo in self.bambooCollection:
            state += str(self.bambooCollection[bamboo].currentHeight) + " "
        print(state)

    def findBambooToCut(self, exceeded):
        if exceeded and self.algorithm is "MH":
            return max(range(len(self.bambooCollection)),
                       key=lambda index: self.bambooCollection[index].currentHeight)

        elif exceeded and self.algorithm is "MGR":
            return max(range(len(self.bambooCollection)), key=lambda index: self.bambooCollection[index].growthRate)

        else:
            return max(range(len(self.bambooCollection)),
                       key=lambda index: self.bambooCollection[index].currentHeight)

    def step(self):

        cutRequired = False
        hExceeded = 0

        for index, bamboo in self.bambooCollection.items():
            bamboo.grow()
            self.bambooResults[index].append(bamboo.currentHeight)
            if bamboo.currentHeight >= self.H:
                hExceeded += 1
                cutRequired = True

        if cutRequired:
            self.state()
            cutBamboo = self.findBambooToCut(True if hExceeded > 1 else False)
            print("Bamboo " + str(cutBamboo) + " exceeded " + str(self.H))
            self.bambooCollection[cutBamboo].cut(self.H)

    def print_stdout(self):
        '''Illustrate that using 'print' writes to stdout'''
        print("this is stdout")

    def print_stderr(self):
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


app = BambooApp()
# app.geometry("1280x720")
# ani = animation.FuncAnimation(figure, animate, interval=1000)
app.mainloop()