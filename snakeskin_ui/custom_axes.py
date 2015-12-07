import matplotlib.pyplot as plt
import numpy as np

class AzElvPlot(object):
    def __init__(self,*figargs,**figkwargs):
        self.fig = plt.figure(*figargs,**figkwargs)
        self.ax = self.fig.add_subplot(111,polar=True)
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_ylabel("ZA")
        self.ax.set_xlabel("Az")

    def draw_za_boundary(self,za,theta,c):
        self.ax.fill(theta,za,c)
        plt.draw()

    def draw_zenith_hole(self,min_za):
        theta = np.linspace(0,np.pi*2,100)
        za = np.ones(100)*min_za
        self.draw_za_boundary(za,theta,'0.5')

    def draw_horizon(self,za,theta):
        self.draw_za_boundary(za,theta,'w')
        
    def plot(self,az,alt,**kwargs):
        self.ax.plot(az,np.pi/2-alt,**kwargs)
        
    def scatter(self,az,alt,**kwargs):
        self.ax.scatter(az,np.pi/2-alt,**kwargs)
