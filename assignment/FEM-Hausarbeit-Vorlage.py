import agros2d as a2d
import math

# problem
problem = a2d.problem(clear = True)
problem.coordinate_type = "planar"
problem.mesh_type = "triangle"
    
# fields
# magnetic
magnetic = a2d.field("magnetic")
magnetic.analysis_type = "steadystate"
magnetic.solver = "linear"
magnetic.matrix_solver = "mumps"
magnetic.number_of_refinements = 2
magnetic.polynomial_order = 2
magnetic.adaptivity_type = "disabled"

# materials
magnetic.add_material("air", {"magnetic_permeability" : 1})
magnetic.add_material("iron", {"magnetic_permeability" : 3500})
magnetic.add_material("I+", {"magnetic_permeability" : 1, "magnetic_total_current_prescribed" : 1, "magnetic_total_current_real" :  800})
magnetic.add_material("I-", {"magnetic_permeability" : 1, "magnetic_total_current_prescribed" : 1, "magnetic_total_current_real" : -800})

# boundaries
magnetic.add_boundary("A = 0", "magnetic_potential", {"magnetic_potential_real" : 0})

# geometry
geometry = a2d.geometry
# U-Joch
geometry.add_edge( 0.055 ,  0    ,  0.085 ,  0    , angle = 0)
geometry.add_edge( 0.085 ,  0    ,  0.085 ,  0.14 , angle = 0)
geometry.add_edge( 0.085 ,  0.14 ,  0.045 ,  0.14 , angle = 0)
geometry.add_edge( 0.045 ,  0.14 , -0.045 ,  0.14 , angle = 0)
geometry.add_edge(-0.045 ,  0.14 , -0.085 ,  0.14 , angle = 0)
geometry.add_edge(-0.085 ,  0.14 , -0.085 ,  0    , angle = 0)
geometry.add_edge(-0.085 ,  0    , -0.055 ,  0    , angle = 0)
geometry.add_edge(-0.055 ,  0    , -0.055 ,  0.11 , angle = 0)
geometry.add_edge(-0.055 ,  0.11 , -0.045 ,  0.11 , angle = 0)
geometry.add_edge(-0.045 ,  0.11 ,  0.045 ,  0.11 , angle = 0)
geometry.add_edge( 0.045 ,  0.11 ,  0.055 ,  0.11 , angle = 0)
geometry.add_edge( 0.055 ,  0.11 ,  0.055 ,  0    , angle = 0)
# Spule
geometry.add_edge( 0.045 ,  0.14 ,  0.045 ,  0.15 , angle = 0)
geometry.add_edge( 0.045 ,  0.15 , -0.045 ,  0.15 , angle = 0)
geometry.add_edge(-0.045 ,  0.15 , -0.045 ,  0.14 , angle = 0)
geometry.add_edge( 0.045 ,  0.11 ,  0.045 ,  0.10 , angle = 0)
geometry.add_edge( 0.045 ,  0.10 , -0.045 ,  0.10 , angle = 0)
geometry.add_edge(-0.045 ,  0.10 , -0.045 ,  0.11 , angle = 0)
# I-Joch
geometry.add_edge( 0.085 , -0.031,  0.085 , -0.001, angle = 0)
geometry.add_edge( 0.085 , -0.001, -0.085 , -0.001, angle = 0)
geometry.add_edge(-0.085 , -0.001, -0.085 , -0.031, angle = 0)
geometry.add_edge(-0.085 , -0.031,  0.085 , -0.031, angle = 0)
# Modellgrenze
geometry.add_edge( 0    , -0.11 ,  0.15 ,  0.04 , angle = 90, boundaries = {"magnetic" : "A = 0"})
geometry.add_edge( 0.15 ,  0.04 ,  0    ,  0.19 , angle = 90, boundaries = {"magnetic" : "A = 0"})
geometry.add_edge( 0    ,  0.19 , -0.15 ,  0.04 , angle = 90, boundaries = {"magnetic" : "A = 0"})
geometry.add_edge(-0.15 ,  0.04 ,  0    , -0.11 , angle = 90, boundaries = {"magnetic" : "A = 0"})
# Label    
geometry.add_label( 0   ,  0.05 , materials = {"magnetic" : "air"}) # Umgebungsluft
geometry.add_label( 0   ,  0.125, materials = {"magnetic" : "iron"})# U-Joch
geometry.add_label( 0   , -0.016, materials = {"magnetic" : "iron"})# I-Joch
geometry.add_label( 0   ,  0.145, materials = {"magnetic" : "I+"})  # oberer Teil der Spule
geometry.add_label( 0   ,  0.105, materials = {"magnetic" : "I-"})  # unterer Teil der Spule
    
a2d.view.zoom_best_fit()
problem.solve()
    
volume = magnetic.volume_integrals([2]) # Volumenintegral vom Gebiet 2 -> I-Joch
kraft = 0.03 * volume["Fty"]
print("Zugkraft: " + str(kraft) + " N")
    
