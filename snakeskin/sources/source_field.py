from snakeskin.sources import Source
import numpy as np
import ephem as eph

SF_DTYPE = [
    ("idx","int32"),
    ("name","|S256"),
    ("ra","float32"),
    ("dec","float32"),
    ("tobs","float32"),
    ("value","float32"),
    ("src_obj","object")
    ]

SEC_TO_SIDRAD = 7.292170441953352e-05

class SourceField(np.recarray):
    def __init__(self,*args,**kwargs):
        super(SourceField,self).__init__(*args,**kwargs)

    @classmethod
    def from_source_list(cls,sources):
        obj = cls(len(sources),dtype=SF_DTYPE)
        dummy_observer = eph.Observer() #for coord precession
        for idx,src in enumerate(sources):
            src.compute(dummy_observer)
            obj[idx] = (idx,src.name,src.ra,src.dec,src.tobs,src.value,src)
        return obj
    
    def __test(self,telescope,dt):
        date = telescope.date
        az_ = []
        alt_ = []
        if not hasattr(dt,"__iter__"):
            dt = np.ones(self.size)*dt
            
        for dt_,row in zip(dt,self):
            telescope.date = date
            telescope.progress_time(dt_)
            az,alt = row.src_obj.azalt(telescope)
            az_.append(az)
            alt_.append(alt)
        telescope.date = date
        return np.array(az_),np.array(alt_)

    def azalt(self,telescope,dt=0.0):
        dlmst = dt*SEC_TO_SIDRAD
        lmst = (telescope.sidereal_time() + dlmst) % (np.pi*2)
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
    
    
