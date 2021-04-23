import cplex
from os import listdir
import time

path = "Problem-Set/"
sol_path = "Solutions/"


def valueBuffer(filename):
    with open(filename) as file:
        for line in file:
            for word in line.split():
                yield int(word)

def readValues(filename):
    values = valueBuffer(filename)
    
    costs = []
    elements = []
    set_number = values.__next__()      # No. of sets
    element_number = values.__next__()  # No. of elements
    
    # Leer datos
    for _ in range(element_number):
        costs.append( values.__next__() )
    
    for _ in range(set_number):
        num_sets_per_element = values.__next__()
        sets_per_element = []
        for _ in range(num_sets_per_element):
            sets_per_element.append( values.__next__() )
        elements.append( sets_per_element )
        
    return elements, costs


def fixFormat(elements, costs):
    objective = costs
    constraints = []
    
    for e in elements:
        cval = [[ s-1 for s in e ], [1] * len(e)]
        constraints.append(cval)
        
    return objective, constraints


def defineProblem(ns, ne, objective, constraints):

    problem = cplex.Cplex()
    
    # vv Hacer que no corra por más de 10 minutos vv #
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
    elements, costs = readValues(filename)
    objective, constraints = fixFormat(elements, costs)
    ne, ns = len(elements), len(costs)
    
    # Definir el problema
    problem = defineProblem(ns, ne, objective, constraints)

    # Resolver el problema
    problem.set_results_stream(None) # Silencio!
    start_time = time.time()
    try:
        problem.solve()
    except:
        print("---", end="")
    total_time = time.time() - start_time
    
    status = problem.solution.get_status()
    if status in [101, 102, 107]:
        obj_value = problem.solution.get_objective_value()
        sol = problem.solution.get_values()
    elif status in [0, 103]:
        obj_value = 0
        sol = None
    return total_time, obj_value, sol



def main():
    # Read File Loop
    with open("outfile.txt", "w") as outfile:
        for file in listdir( path ):
            time, obj_value, sol =  solveProblem( path + file )
            str_sol = file.replace(".txt", "") + "\t\t" + "{0:.06f}".format(time) + "\t\t"  + str(obj_value) + "\n"
            outfile.write( str_sol )
            with open( sol_path + file.replace(".txt", ".sol"), "w" ) as sol_file:
                sol_file.write( str( sol ) )
            print(str_sol)
    

if __name__ == "__main__":
    main()


