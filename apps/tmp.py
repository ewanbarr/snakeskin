import sys
sys.path.append("../")

import snakeskin as s

params = {"pheremone_weight":1.0,
          "allure_weight":0.0}

telescope = s.Parkes()
sources = s.source_field_from_file(sys.argv[1])
pheremones = s.BasePheremoneModel()
path_finder = s.BasePathFinder(telescope,sources,pheremones,params)
print path_finder.find_path()


