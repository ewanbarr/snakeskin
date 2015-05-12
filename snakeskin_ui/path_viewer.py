import Tkinter as tk
import numpy as np
from snakeskin_ui.custom_widgets import PlotWindow

class AzElvPathViewer(PlotWindow):
    def __init__(self,parent):
        PlotWindow.__init__(self,parent)
                
    def setup_axes(self):
        ax = self.fig.add_subplot(111,polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_ylabel("ZA")
        ax.set_xlabel("Az")
        ax.patch.set_facecolor('0.5')
        return [ax]
    
    def draw_za_boundary(self,za,theta,c):
        ax = self.axes[0]
        ax.fill(theta,za,c)
        self.canvas.draw()

    def draw_zenith_hole(self,min_za):
        theta = np.linspace(0,np.pi*2,100)
        za = np.ones(100)*min_za
        self.draw_za_boundary(za,theta,'0.5')

    def draw_horizon(self,za,theta):
        self.draw_za_boundary(za,theta,'w')
        

if __name__ == "__main__":
    root = tk.Tk()
    viewer = AzElvPathViewer(root)
    viewer.pack()
    
    root.mainloop()
