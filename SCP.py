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

def defineProblem(ns, ne, objective, constraints):

    problem = cplex.Cplex()
    # vv Hacer que no corra por más de 10 minutos vv
    problem.parameters.timelimit.set(600)   
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
    
    return problem
    

# Inicio del problema
def solveProblem(filename):
    
    # Leer Datos
    sets, costs = readValues(filename)
    objective, constraints = fixFormat(sets, costs)
    ns, ne = len(sets), len(costs)
    
    # Definir el problema
    problem = defineProblem(ns, ne, objective, constraints)

    # Resolver el problema
    problem.set_results_stream(None) # Silencio!
    try:
        problem.solve()
    except:
        print("Error")
    
    
    
    print("")
    status = problem.solution.get_status()
    print(f"[{status}] ", end="")
    if status in [101, 102, 107]:
        if status == 101:
            print("La solución es óptima")
        if status == 102:
            print("La solución es óptima (dentro de los límites)")
        elif status == 107:
            print("Se agotó el tiempo de espera")
            print("A continuación se muestra la mejor solución encontrada")
        print("Soluciones:", problem.solution.get_values())
        print("Valor Objetivo:", problem.solution.get_objective_value())
    elif status == 103:
        print("La solución es infactible")
    elif status == 0:
        print("El estado final es desconocido")
    



def main():
    # Read File Loop
    for file in listdir( path ):
        print("\nProblema:", file)
        solveProblem( path + file )
    

if __name__ == "__main__":
    main()


