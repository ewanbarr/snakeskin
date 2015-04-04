import interface as _interface
import telescope as _telescope
import sources as _sources
import optimiser as _optimiser
import utils as _utils
import Tkinter as tk
from threading import Event,Thread

class InteractiveSnakeskin(object):
    def __init__(self,root,sources,optimiser,telescope):
        self.sources = sources
        self.optimiser = optimiser
        self.telescope = telescope()
        self.gui = _interface.MasterWindow(root)
        self.gui.params.set_params(optimiser.model)
        self.gui.pack()
        self.stop_event = Event()
        self.update()
        self.optimise()

    def update(self):
        self.telescope.set_date()
        sources = self.sources.get_visible(self.telescope)
        self.gui.pathlist.set_path(sources)
        self.gui.viewer.plot_sources(sources)
        
    def stop(self):
        print "STOP CALLED"
        self.stop_event.set()
        self.opt_thread.join()

    def _optimise(self):
        print "STARTING"
        pos = (0.1,0.1,"north")
        while not self.stop_event.is_set():
            print "iterate"
            self.optimiser.model.update(self.gui.params.as_dict())
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
