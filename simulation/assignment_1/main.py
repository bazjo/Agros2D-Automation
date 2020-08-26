import agros2d as a2d

from simulation import setupSimulation

f = open("result.csv", "w")

def simulateCurrent(current):
    problem = a2d.problem(clear = True)
    problem.coordinate_type = "planar"
    problem.mesh_type = "triangle"

    sim = setupSimulation(current)

    a2d.view.zoom_best_fit()
    problem.solve()

    volume = sim.volume_integrals([2]) # Volumenintegral vom Gebiet 2 -> I-Joch
    flux_density = sim.local_values(0.07, -0.0005)

    force = volume["Fty"] * 2 * 0.03
    flux = flux_density["Br"]

    f.write(str(current) + "," + str(force) + "," + str(flux)+ "\n")

f.write("Current [A],Force [N],Flux Density [T]\n")

for current in range(1, 65):
    simulateCurrent(current)

f.close()
