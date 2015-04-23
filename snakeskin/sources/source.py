import ephem as eph

class Source(eph.FixedBody):
    def __init__(self,ra,dec,tobs=1800.0,name="none",value=1.,obs_config=None):
        super(Source,self).__init__()
        self.name = name
        coords = eph.Equatorial(ra,dec)
        self._ra = coords.ra
        self._dec = coords.dec
        self.tobs = tobs
        self._value = value
        self.obs_config = obs_config

    def azalt(self,telescope):
        self.compute(telescope)
        return self.az,self.alt
    
    def value(self):
        return self._value
    
