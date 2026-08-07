#%%
import pybamm
import numpy as np
# import os
import matplotlib.pyplot as plt
import pybamm.mz_develop.output_module as outmod

#%%
model = pybamm.lithium_ion.SPM({"PE degradation": "yes"})
#%
param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.ORegan2021_pe_deg_v2)
#%%
experiment = pybamm.Experiment(
    [
        (
            "Charge at 0.5 C until 4.2 V",
            "Hold at 4.2 V until C/50",
            "Rest for 60 minutes",
            "Discharge at 0.5 C until 2.8 V",
            "Hold at 2.8 V until C/50",
            "Rest for 60 minutes",
        )
    ] * 20,
    # need for case I
    period="0.5 minute",
)

sim = pybamm.Simulation(
    model, experiment=experiment,
    parameter_values=param,
    solver=pybamm.CasadiSolver(mode="safe", dt_max=600),
)


#%%
try:
    solution = sim.solve(calc_esoh=False)
except pybamm.SolverError as e:
    print("Solve stopped early:", e)
    solution = sim.solution


    #%%
output_variables = outmod.output_variables_spm
sim.plot(output_variables)


