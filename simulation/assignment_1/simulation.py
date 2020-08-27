import agros2d as a2d

def setupSimulation(coil_current):
    # field
    sim = a2d.field("magnetic")
    sim.analysis_type = "steadystate"
    sim.solver = "linear"
    sim.matrix_solver = "mumps"
    sim.number_of_refinements = 2
    sim.polynomial_order = 2
    sim.adaptivity_type = "disabled"

    # parametric simulation variables
    windings = 50 # windings of the coil

    # materials
    sim.add_material("air", {"magnetic_permeability": 1})
    sim.add_material("iron", {"magnetic_permeability": 3500})
    sim.add_material("I+", {"magnetic_permeability": 1, "magnetic_total_current_prescribed": 1, "magnetic_total_current_real": (windings * coil_current) / 2})
    sim.add_material("I-", {"magnetic_permeability": 1, "magnetic_total_current_prescribed": 1, "magnetic_total_current_real": -1 * (windings * coil_current) / 2})

    # boundaries
    sim.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_real": 0})
    sim.add_boundary("J = 0", "magnetic_surface_current", {"magnetic_surface_current_real": 0})

    geometry = setupGeometry()

    return sim

def setupGeometry():
    geometry = a2d.geometry

    # parametric geometry variables (in metres)
    width = 0.17 # width of the u- and i-core in x-dimension
    height = 0.17 # height of the u-core in y-dimension
    thickness = 0.03 # thickness of the core assembly
    airgap = 0.001 # airgap between cores
    coil_clearance = 0.0001 # clearance between coil and perpendicular side of the core (must not be zero)
    coil_thickness = 0.01 # thickness of the coil
    simulation_radius = 0.3 # radius of the outer boundary
    label_offset = 0.01 # offset of labels fron y-axis

    # calculated geometry variables
    x_core_outer = width / 2
    x_core_inner = x_core_outer - thickness
    x_core_coil = x_core_inner - coil_clearance
    y_u_core_outer = height
    y_u_core_inner = y_u_core_outer - thickness
    y_i_core_inner = 0 - airgap
    y_i_core_outer = y_i_core_inner - thickness
    y_coil_upper = y_u_core_outer + coil_thickness
    y_coil_lower = y_u_core_inner - coil_thickness
    center_offset = (y_coil_upper - y_i_core_outer) / 2

    # u-core
    # geometry.add_edge(startX, startY, endX, endY, angle = 0)
    geometry.add_edge(x_core_inner, 0, x_core_outer, 0, angle = 0)
    geometry.add_edge(x_core_outer, 0, x_core_outer, y_u_core_outer, angle = 0)
    geometry.add_edge(x_core_outer, y_u_core_outer, x_core_coil, y_u_core_outer, angle = 0)
    geometry.add_edge(x_core_coil, y_u_core_outer, 0, y_u_core_outer, angle = 0)
    geometry.add_edge(0, y_u_core_inner, x_core_coil, y_u_core_inner, angle = 0)
    geometry.add_edge(x_core_coil, y_u_core_inner, x_core_inner, y_u_core_inner, angle = 0)
    geometry.add_edge(x_core_inner, y_u_core_inner, x_core_inner, 0, angle = 0)

    # i-core
    geometry.add_edge(0, y_i_core_inner, x_core_outer, y_i_core_inner, angle = 0)
    geometry.add_edge(x_core_outer, y_i_core_inner, x_core_outer, y_i_core_outer, angle = 0)
    geometry.add_edge(x_core_outer, y_i_core_outer, 0, y_i_core_outer, angle = 0)

    #upper coil
    geometry.add_edge(0, y_coil_upper, x_core_coil, y_coil_upper, angle = 0)
    geometry.add_edge(x_core_coil, y_coil_upper, x_core_coil, y_u_core_outer, angle = 0)

    #lower coil
    geometry.add_edge(0, y_coil_lower, x_core_coil, y_coil_lower, angle = 0)
    geometry.add_edge(x_core_coil, y_coil_lower, x_core_coil, y_u_core_inner, angle = 0)

    # boundary
    geometry.add_edge(simulation_radius, center_offset, 0, simulation_radius + center_offset, angle = 90, boundaries = {"magnetic": "A = 0"})
    geometry.add_edge(0, -1 * simulation_radius + center_offset, simulation_radius, center_offset, angle = 90, boundaries = {"magnetic": "A = 0"})

    geometry.add_edge(0, -1 * simulation_radius + center_offset, 0, y_i_core_outer, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_i_core_outer, 0, y_i_core_inner, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_i_core_inner, 0, y_coil_lower, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_coil_lower, 0, y_u_core_inner, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_u_core_inner, 0, y_u_core_outer, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_u_core_outer, 0, y_coil_upper, angle = 0, boundaries = {"magnetic": "J = 0"})
    geometry.add_edge(0, y_coil_upper, 0, simulation_radius + center_offset, angle = 0, boundaries = {"magnetic": "J = 0"})

    # labels
    geometry.add_label(label_offset, simulation_radius + center_offset - 0.01, materials = {"magnetic": "air"})
    geometry.add_label(label_offset, y_u_core_inner + (y_u_core_outer - y_u_core_inner) / 2, materials = {"magnetic": "iron"}) # u-core
    geometry.add_label(label_offset, y_i_core_inner + (y_i_core_outer - y_i_core_inner) / 2, materials = {"magnetic": "iron"}) # i-core
    geometry.add_label(label_offset, y_u_core_outer + (y_coil_upper - y_u_core_outer ) / 2, materials = {"magnetic": "I+"}) # upper coil
    geometry.add_label(label_offset, y_coil_lower + (y_u_core_inner - y_coil_lower ) / 2, materials = {"magnetic": "I-"}) # lower coil

    return geometry
