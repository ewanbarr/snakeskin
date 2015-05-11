import Tkinter as tk
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Viewer(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.fig,self.ax = self.__generate_axes()
        self.canvas = FigureCanvasTkAgg(self.fig,self.parent)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.show()

    def __generate_axes(self):
        fig = mpl.figure.Figure()
        ax = fig.add_subplot(111,polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_ylabel("ZA")
        ax.set_xlabel("Az")
        ax.patch.set_facecolor('0.5')
        return fig,ax
    
    def draw_za_boundary(self,za,theta,c):
        self.ax.fill(theta,za,c)
        self.canvas.draw()

    def draw_zenith_hole(self,min_za):
        theta = np.linspace(0,np.pi*2,100)
        za = np.ones(100)*min_za
        self.draw_za_boundary(za,theta,'0.5')

    def draw_horizon(self,za,theta):
        self.draw_za_boundary(za,theta,'w')
        

if __name__ == "__main__":
    root = tk.Tk()
    viewer = Viewer(root)
    viewer.pack()
    root.mainloop()
