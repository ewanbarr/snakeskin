import numpy as np
import ephem as eph
from utils import *

class SourceField(list):
    def __init__(self,sources=None):
        super(SourceField,self).__init__([])
        if sources:
            self.extend(sources)
        
    def get_visible(self,telescope,exclude=None):
        if exclude is None:
            exclude = []
        return SourceField([source for source in self if source.visible(telescope) if source not in exclude])

    
class Source(eph.FixedBody):
    def __init__(self,ra,dec,name="none"):
        super(Source,self).__init__()
        self.name = name
        coords = eph.Equatorial(ra,dec)
        self._ra = coords.ra
        self._dec = coords.dec
        self.value = lambda: 1
        
    def visible(self,telescope):
        self.compute(telescope)
        return self.alt > telescope.horizon
            
    def estimated_tobs(self):
        return 600.0


def fake_source_field():
    fname = "../test_data/pulsars.txt"
    f = open(fname)
    lines = f.readlines()
    f.close()
    field = SourceField()
    for line in lines:
        name,ra,dec = line.split()
        source = Source(ra,dec,name)
        field.append(source)
    return field
