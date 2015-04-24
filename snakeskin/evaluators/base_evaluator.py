

class BaseEvaluator(object):
    def __init__(self,tour,telescope):
        self.tour = tour
        self.telescope = telescope
        
    def evaluate(self):
        for source in tour:
            az,alt = source.azalt(self.telescope)
            self.telescope.drive_to()
            
