import sys
sys.path.append("../")
import numpy as np
import snakeskin as s

params = {"pheremone_weight":1.0,
          "allure_weight":0.0}

telescope = s.Parkes()
eval_telescope = s.Parkes()
sources = s.source_field_from_file(sys.argv[1])
pheremones = s.BasePheremoneModel()
path_finder = s.BasePathFinder(telescope,sources,pheremones,params)
path,cost = path_finder.find_path()

telescope = s.Parkes()
evaluator = s.BaseEvaluator(eval_telescope,path)
evaluator.evaluate()

import matplotlib.pyplot as plt

ax = plt.subplot(111,polar=True)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

print evaluator.value,evaluator.drive_time,evaluator.idle_time

for drive in evaluator.drive_paths:
    az,alt = drive
    za = np.pi/2 - alt
    ax.plot(az,za,c='b',lw=1)

for obs in evaluator.tracks:
    az,alt = obs
    za = np.pi/2 - alt
    ax.plot(az,za,c='r',lw=2)

plt.show()


