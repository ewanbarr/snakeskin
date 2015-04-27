import ephem as eph
import numpy as np

SEC_TO_SIDRAD = 7.292170441953352e-05

class Source(eph.FixedBody):
    def __init__(self,ra,dec,tobs=1800.0,name="none",value=1.,obs_config=None):
        super(Source,self).__init__()
        self.name = name
        coords = eph.Equatorial(ra,dec)
        self._ra = coords.ra
        self._dec = coords.dec
        self.tobs = tobs
        self.value = value
        self.obs_config = obs_config

    def azalt(self,telescope,dt=0.0):
        telescope.progress_time(dt)
        self.compute(telescope)
        telescope.reverse_time(dt)
        return self.az,self.alt
    
    def trail(self,telescope,duration=600.0):
        start_lmst = telescope.sidereal_time()
        end_lmst = start_lmst+SEC_TO_SIDRAD*duration
        lmst = np.linspace(start_lmst,end_lmst,100)%(np.pi*2)
        lat = telescope.lat
        ha = lmst-self.ra
        cosha = np.cos(ha)
        coslat = np.cos(lat)
        sinlat = np.sin(lat)
        alt = np.arcsin(sinlat*np.sin(self.dec)
                        +coslat*np.cos(self.dec)*cosha)
        az = np.arctan2(np.sin(ha),
                        (cosha*sinlat
                         - np.tan(self.dec)*coslat))+np.pi
        return az,alt
