import agros2d as a2d

from simulation import setupSimulation

f = open("result.csv", "w")

def simulateMagnet(magnet_height):
    problem = a2d.problem(clear = True)
    problem.coordinate_type = "planar"
    problem.mesh_type = "triangle"

    sim = setupSimulation(0, magnet_height)

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

    f.write(str(magnet_height) + "," + str(force) + "," + str(flux)+ "\n")

f.write("Magnet Thickness [m],Force [N],Flux Density [T]\n")

for magnet_height in range(1, 12):
    simulateMagnet(magnet_height * 0.001)

f.close()
