#%%
import pybamm
import numpy as np
import os
import matplotlib.pyplot as plt
import pybamm.mz_develop.output_module as outmod

#%%
model = pybamm.lithium_ion.SPM({"PE degradation": "yes"})
#%
param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Zhuo2021)
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
)


#%%
solution = sim.solve(calc_esoh=False)


    #%%
output_variables = outmod.output_variables_spm
sim.plot(output_variables)

total_cycles = len(solution.cycles)
cycle_numbers= np.arange(1, total_cycles+1)
Q_dis_cycles = []

for i in range (total_cycles):

    Q_dis_cyc = solution.cycles[i].steps[3]["Discharge capacity [A.h]"].entries
    Q_dis_cycles.append(Q_dis_cyc[-1] - Q_dis_cyc[0])


os.makedirs("pybamm/mz_develop/output", exist_ok=True)
np.save("Q_dis_cycles_Chen.npy", Q_dis_cycles)

plt.figure(figsize=(8,6))
plt.plot(cycle_numbers, Q_dis_cycles, '-o', mfc='none', label="Zhuo2021")
plt.xlabel("Cycle number"); plt.ylabel("Discharge capacity [A.h]")
plt.legend(); plt.show()