import numpy as np
import ephem as eph
from snakeskin.sources import Source
from snakeskin.constants import SEC_TO_SIDRAD

SF_DTYPE = [
    ("idx","int32"),
    ("name","|S256"),
    ("ra","float32"),
    ("dec","float32"),
    ("tobs","float32"),
    ("value","float32"),
    ("observed","bool"),
    ("src_obj","object")
    ]


class SourceField(object):
    def __init__(self,telescope,sources):
        self.telescope = telescope
        self.__parse_source_list(sources)
        self.build_cache()
        self.__orig_data = np.copy

    def __parse_source_list(self,sources):
        self.data = np.recarray(len(sources),dtype=SF_DTYPE)
        for idx,src in enumerate(sources):
            src.compute(self.telescope)
            self.data[idx] = (idx,src.name,src.ra,src.dec,src.tobs,src.value,False,src)
        self.data = np.sort(self.data,order="ra")

    def build_cache(self,max_drift=0.01):
        self._lmsts = np.arange(0,np.pi*2+max_drift,max_drift)
        npts = self._lmsts.size
        dtype =[("idx","int32"),("az","float32",npts),("alt","float32",npts),("valid","bool",npts)]
        self._cache = np.recarray(self.data.size,dtype=dtype)
        for ii,src in enumerate(self.data):
            az,alt = src.src_obj.path(self.telescope,self._lmsts)
            self._cache.az[ii] = az
            self._cache.alt[ii] = alt
        self._cache.valid[:] = self.telescope.visible(self._cache.az,self._cache.alt)
        #self.data[self._cache.valid.sum(axis=1)==0].observed[:] = True
            
    def observable(self,lmst):
        idx = self._lmsts.searchsorted(lmst)
        valid = self._cache.valid[:,idx] & ~self.data.observed
        valid_data = self.data[valid]
        valid_cache =self._cache[valid]
        end_idx = self._lmsts.searchsorted(lmst+valid_data.tobs*SEC_TO_SIDRAD)
        mask = np.array([all(valid_cache.valid[ii][idx:eidx]) for ii,eidx in enumerate(end_idx)])
        if any(mask):
            return valid_data[mask],valid_cache.az[mask][:,idx],valid_cache.alt[mask][:,idx]
        else:
            return None,None,None

    def mark_as_observed(self,idx):
        self.data.observed[np.where(self.data.idx==idx)[0]] = True
        
    def reset_observed_status(self):
        self.data.observed[:] = False
    
            
        
        
        
        
        
    


