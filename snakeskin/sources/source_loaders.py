from snakeskin.sources import Source,SourceField
import numpy as np

FILE_DTYPE = [
    ("name","|S256"),
    ("ra","|S256"),
    ("dec","|S256"),
    ("tobs","float32"),
    ("value","float32"),
    ]

def source_field_from_file(fname,telescope):
    vals = np.genfromtxt(fname,dtype=FILE_DTYPE)
    sources = []
    for val in vals:
        source = Source(val['ra'],val['dec'],tobs=val['tobs'],
                        name=val['name'],value=val['value'])
        sources.append(source)
    field = SourceField(telescope,sources)
    return field
    
