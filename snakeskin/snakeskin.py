import interface as _interface
import telescope as _telescope
import sources as _sources
import optimiser as _optimiser
import utils as _utils
import Tkinter as tk
from threading import Event,Thread

class InteractiveSnakeskin(object):
    def __init__(self,root,sources,optimiser,telescope):
        self.root = root
        self.sources = sources
        self.optimiser = optimiser
        self.telescope = telescope()
        self.gui = _interface.MasterWindow(root)
        self.gui.params.set_params(optimiser.model)
        self.gui.pack()
        self.stop_event = Event()
        self.update()
        self.opt_thread = None
        self.gui.controls.add_control("start",self.start)
        self.gui.controls.add_control("stop",self.stop)

    def update(self):
        self.telescope.set_date()
        sources = self.sources.get_visible(self.telescope)
        self.gui.pathlist.set_path(sources)
        self.gui.viewer.plot_sources(sources)
        if self.optimiser.best_path:
            print "BEST PATH",self.optimiser.best_path
            self.gui.viewer.plot_path(self.optimiser.best_path)

    def stop(self):
        print "STOP CALLED"
        self.stop_event.set()
        try:
            self.opt_thread.join()
        except:
            pass
    
    def start(self):
        print "START CALLED"
        if not self.opt_thread or not self.opt_thread.is_alive():
            self.stop_event.clear()
            self.optimise()

    def _optimise(self):
        print "STARTING"
        pos = (0.1,0.1,"north")
        while not self.stop_event.is_set():
            print "iterate"
            self.optimiser.model.update(self.gui.params.get_params())
            print self.optimiser.model
            self.optimiser.optimise(pos)
                        
    def optimise(self):
        print "called"
        self.opt_thread = Thread(target=self._optimise)
        self.opt_thread.start()

        
def main():
    field = _sources.fake_source_field()
    tele = _telescope.telescope_type_from_config("../config/telescopes/MeerKAT.cfg")
    opt = _optimiser.AntColonyOptimiser(field,tele)
    root = tk.Tk()
    InteractiveSnakeskin(root,field,opt,tele)
    root.mainloop()

if __name__ == "__main__":
    main()
