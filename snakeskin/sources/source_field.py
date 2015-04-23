from snakeskin.sources import Source
import numpy as np

SF_DTYPE = [
    ("idx","int32"),
    ("name","|S256"),
    ("ra","float32"),
    ("dec","float32"),
    ("tobs","float32"),
    ("value","float32"),
    ("src_obj","object")
    ]

class SourceField(np.recarray):
    def __init__(self,*args,**kwargs):
        super(SourceField,self).__init__(*args,**kwargs)

    @classmethod
    def from_source_list(cls,sources):
        obj = cls(len(sources),dtype=SF_DTYPE)
        for idx,src in enumerate(sources):
            obj[idx] = (idx,src.name,src._ra,src._dec,src.tobs,src._value,src)
        return obj
    
    def azalt(self,telescope):
        lmst = telescope.sidereal_time()
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
    
    
