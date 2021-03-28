import cplex
from os import listdir

path = "Problem-Set/"



def valueBuffer(filename):
    with open(filename) as file:
        for line in file:
            for word in line.split():
                yield int(word)
         
            

def readValues(filename):
    values = valueBuffer(filename)
    
    costs = []
    sets = []
    set_number = values.__next__()
    element_number = values.__next__()
    
    # Leer datos
    for _ in range(element_number):
        costs.append( values.__next__() )
    
    for _ in range(set_number):
        num_elements_in_set = values.__next__()
        elements_in_set = []
        for _ in range(num_elements_in_set):
            elements_in_set.append( values.__next__() )
        sets.append( elements_in_set )
        
    return sets, costs



def fixFormat(sets, costs):
    objective = [ sum( [ costs[e-1] for e in s ] ) for s in sets ]
    elements = [ [] for _ in range(len(costs)) ]
    constraints = []
    
    for i in range(len(sets)):
        for e in sets[i]:
            elements[e-1].append(i)
    
    for e in elements:
        cval = [[ s for s in e ], [1] * len(e)]
        constraints.append(cval)
        
    return objective, constraints



# Inicio del problema
def solveProblem(filename):
    
    # Leer Datos
    sets, costs = readValues(filename)
    objective, constraints = fixFormat(sets, costs)
    
    ns = len(sets)
    ne = len(costs)
    
    # Definir el problema
    problem = cplex.Cplex()
    problem.objective.set_sense(problem.objective.sense.minimize)
    
    # Variables
    names = [f"set {i+1}" for i in range(ns)]
    problem.variables.add(
        obj = objective,
        names = names,
        types = ["B"] * ns
        )
    
    # Restricciones
    cnames = [f"element{i+1}" for i in range(ne)]
    rhs = [1] * ne
    problem.linear_constraints.add(
        names = cnames,
        lin_expr = constraints,
        rhs = rhs,
        senses = ["G"] * ne
        )
    
    
    # Resolver el problema
    problem.set_results_stream(None)
    problem.solve()
    
    print()
    try:
        print("Soluciones:", problem.solution.get_values())
        print("Valor Objetivo:", problem.solution.get_objective_value())
    except:
        print("No hay soluciones reales")



# Read File Loop

for file in listdir( path ):
    solveProblem( path + file )