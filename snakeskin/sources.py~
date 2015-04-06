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
        self.minimum_tobs = 300.0
        self.maximum_tobs = 900.0

    def visible(self,telescope):
        self.compute(telescope)
        up = self.alt > telescope.horizon
        setting = telescope.next_setting(self)
        remaining = (setting - telescope.date) / SEC_TO_DAYS
        self.compute(telescope)
        return up and remaining > self.minimum_tobs

    def value(self,telescope):
        return 1
        


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
