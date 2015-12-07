from snakeskin.sources import source_loaders
from snakeskin.telescopes import parkes
from snakeskin.sources import source_loaders
from snakeskin.path_finders import base_path_finder as bpf
from snakeskin.pheremones.base_pheremones import BasePheremoneModel
pher = BasePheremoneModel()
pks = parkes.Parkes()
x = bpf.BasePathFinder(pks,p,pher)
p = source_loaders.source_field_from_file("test_data/p789_with_values.txt",parkes.Parkes())
pks = parkes.Parkes()
x = bpf.BasePathFinder(pks,p,pher)

x.find_path()