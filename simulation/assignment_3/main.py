import agros2d as a2d

from simulation import setupSimulation

f = open("result.csv", "w")

def simulateCurrent(current):
    problem = a2d.problem(clear = True)
    problem.coordinate_type = "planar"
    problem.mesh_type = "triangle"

    sim = setupSimulation(current, 0.003)

    a2d.view.zoom_best_fit()
    problem.solve()

    # geometry variables for result analysis
    i_core_area = 2
    x_airgap = 0.07
    y_airgap = -0.0005

    volume = sim.volume_integrals([i_core_area]) # volume integral of the i-core
    local_values = sim.local_values(x_airgap, y_airgap) # local field values in the airgap

    force = volume["Fty"] * 2 * 0.03 # force on i-core
    flux = local_values["Br"] # flux in the  airgap

    f.write(str(current) + "," + str(force) + "," + str(flux)+ "\n")

f.write("Current [A],Force [N],Flux Density [T]\n")

for current in range(-60, 60 + 1, 5):
    simulateCurrent(current)

f.close()
