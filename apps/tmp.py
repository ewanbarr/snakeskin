import sys
import numpy as np
from snakeskin.telescopes import Parkes
from snakeskin.sources import source_loaders
from snakeskin.path_finders import base_path_finder as bpf
from snakeskin.pheremones.base_pheremones import BasePheremoneModel


pher = BasePheremoneModel()
pks = Parkes()
p = source_loaders.source_field_from_file("../test_data/p789_with_values.txt",pks)
path_finder = bpf.BasePathFinder(pks,p,pher)

paths = []
costs = []
nants = 20
its = 20

for jj in range(its):
    for ii in range(nants):
        p.reset_observed_status()
        path_finder.telescope.reset()
        path,cost = path_finder.find_path()
        paths.append(path)
        costs.append(cost)
    for path,cost in zip(paths,costs):
        print cost
        pher.deposit(path,cost)
    pher.evaporate()
    paths = []
    costs = []


