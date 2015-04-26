import warnings
SEC_TO_DAYS = 1/86400.

class BaseEvaluator(object):
    def __init__(self,telescope,tour):
        self.telescope = telescope
        self.tour = tour
        self.__wait = 600.0
        self.value = 0
        self.idle_time = 0
        self.drive_time = 0
        self.drive_paths = []
        self.tracks = []
        
    def __spin_until_observable(self,source):
        idle_time = 0
        while not self.telescope.observable(source):
            warnings.warn("%s not observable at %s"%(
                    source.name,self.telescope.date))
            self.telescope.progress_time(self.__wait)
            idle_time += self.__wait
        return idle_time
                    
    def evaluate(self):
        for source in self.tour:
            start = self.telescope.date
            self.idle_time += self.__spin_until_observable(source)
            az,alt = source.azalt(self.telescope)
            self.drive_paths.append(self.telescope.path_to(az,alt))
            response = self.telescope.sky_response(az,alt)
            self.value += response * source.value
            self.drive_time += self.telescope.drive_time(az,alt)
            self.telescope.drive_to(source)
            self.tracks.append(source.trail(self.telescope,duration=source.tobs))
            self.telescope.observe(source)
