import Tkinter as tk
from matplotlib import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from utils import *

PLOT_SIZE = [5,5]

class CustomEntry(tk.Frame):
    def __init__(self,parent,label,default=0):
        tk.Frame.__init__(self,parent)
        self.var = tk.StringVar()
        self.var.set(str(default))
        label = label.replace("_"," ").capitalize()
        self.label = tk.Label(self,text=label,justify=tk.LEFT,width=20)
        self.label.pack(side=tk.LEFT,padx=5,anchor="e",fill=tk.BOTH)
        self.entry = tk.Entry(self,textvariable=self.var)
        self.entry.pack(side=tk.RIGHT,expand=1)

    def get(self):
        return self.var.get()

class ParameterController(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text=self.__class__.__name__).pack()
        #self.labels_frame = tk.Frame(self)
        #self.labels_frame.pack(side=tk.LEFT)
        self.params = {}

    def _clear_params(self):
        for name in self.params.keys():
            self.params[name].destroy()
            del self.params[name]
                    
    def set_params(self,params):
        self._clear_params()
        for name,value in params.items():
            self.params[name] = CustomEntry(self,name,value)
            self.params[name].pack(side=tk.TOP,anchor="n")

    def as_dict(self):
        result = {}
        for key,widget in self.params.items():
            result[key] = float(widget.var.get())
        return result

class ViewerWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text=self.__class__.__name__).pack()
        self.figure = figure.Figure(figsize=PLOT_SIZE, dpi=100)
        self.ax = self.figure.add_subplot(111,polar=True)
        self.canvas = FigureCanvasTkAgg(self.figure,self)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(fill=tk.BOTH,expand=1)
        self.ax.tick_params(labelsize="small")
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.canvas.show()
        self.points = None
        
    def plot_sources(self,sources):
        if self.points:
            self.points.remove()
        az,za = np.array([(i.az,np.pi/2-i.alt) for i in sources]).transpose()
        self.points = self.ax.scatter(az,za)
        self.ax.set_rlim(0,np.pi/2)
            
class BestPathWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text=self.__class__.__name__).pack()
        self.path = tk.Listbox(self)
        self.path.pack(fill=tk.BOTH,expand=1)

    def set_path(self,sources):
        self.path.delete(0,tk.END)
        for source in sources:
            self.path.insert(tk.END,source.name)

    
class ControlsWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text=self.__class__.__name__).pack()
    
        self.start = tk.Button(self,text="start",command=self.start)
        self.start.pack(side=tk.LEFT)
        self.stop = tk.Button(self,text="stop",command=self.stop)
        self.stop.pack(side=tk.LEFT)
        
    def start(self):
        print "start"

    def stop(self):
        print "stop"

class MasterWindow(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom")
        self.controls = ControlsWindow(self.bottom_frame)
        self.controls.pack()
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side="top")
        self.viewer = ViewerWindow(self.top_frame)
        self.viewer.pack(side="left",padx=4)
        self.pathlist = BestPathWindow(self.top_frame)
        self.pathlist.pack(side="left",anchor="n",padx=4)
        self.params = ParameterController(self.top_frame)
        self.params.pack(side="right",anchor="n")


def launch():
    root = tk.Tk()
    MasterWindow(root).pack()
    root.mainloop()
    
if __name__ == "__main__":
    launch()
    