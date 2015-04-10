import interface as _interface
import telescope as _telescope
import sources as _sources
import optimiser as _optimiser
import utils as _utils
import evaluators as _evaluators
import Tkinter as tk
from threading import Event,Thread
import logging
logging.basicConfig(level=logging.INFO)

class InteractiveSnakeskin(object):
    def __init__(self,root,sources,optimiser,telescope_config):
        self.root = root
        self.sources = sources
        self.optimiser = optimiser
        self.telescope = _telescope.create_telescope(telescope_config)
        self.gui = _interface.MasterWindow(root)
        self.gui.params.set_params(optimiser.model)
        self.gui.pack()
        self.stop_event = Event()
        self.update()
        self.opt_thread = None
        self.gui.controls.add_control("start",self.start)
        self.gui.controls.add_control("stop",self.stop)
        self.gui.controls.add_control("update",self.update)
        self.gui.controls.add_control("reset",self.reset)

    def reset(self):
        self.optimiser.pheremones = _optimiser.Pheremones()
        self.optimiser.best_score = 0
        self.optimiser.best_tour = []
        
    def update(self):
        self.telescope.set_date()
        sources = self.sources.get_visible(self.telescope)
        if self.optimiser.best_tour:
            print "BEST PATH",self.optimiser.best_tour
            self.gui.pathlist.set_tour(self.optimiser.best_tour)
            self.gui.viewer.plot_tour(self.optimiser.best_tour)

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
        pos = (0.1,0.1,"north")
        while not self.stop_event.is_set():
            self.optimiser.update(self.gui.params.get_params())
            self.optimiser.optimise(pos)
                        
    def optimise(self):
        self.opt_thread = Thread(target=self._optimise)
        self.opt_thread.start()


def test():
    field = _sources.fake_source_field()
    evaluator = _evaluators.Evaluator(field)
    telescope_config = _utils.read_config("../config/telescopes/MeerKAT.cfg")
    opt = _optimiser.AntColonyOptimiser(field,evaluator,telescope_config)
    return opt
        
def main(root):
    field = _sources.fake_source_field()
    evaluator = _evaluators.Evaluator(field)
    telescope_config = _utils.read_config("../config/telescopes/MeerKAT.cfg")
    opt = _optimiser.AntColonyOptimiser(field,evaluator,telescope_config)
    return InteractiveSnakeskin(root,field,opt,telescope_config)

if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()
