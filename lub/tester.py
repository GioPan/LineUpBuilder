from problem import Problem
from model import Model
from modelRoot import ModelRoot
from subproblem import Subproblem
from scenario_tree import ScenarioTree
import time
import gc

class Tester:

    @staticmethod
    def solveFullProblem(problem,timeLimit):
        model = Model(problem)

        start_time = time.time()
        model.solve(timeLimit)
        elapsed_time_mip = time.time() - start_time
        
        ub_mip = model.getUpperBound()
        gap_mip = float("inf")
        objective_mip = float("inf")
        
        if (ub_mip < float("inf")):
            objective_mip = model.getObjective()
            gap_mip = (
                (model.getUpperBound()
                 -model.getObjective()
                )/(1e-15+model.getObjective())
            )

        print "%8s %8s %8s %8s" % ("Method","Time","Objective","Gap")
        if(ub_mip < float("inf")):
            print ("%8s %8.2f %8.2f %8.2f"
                   % ("MIP",elapsed_time_mip,objective_mip,gap_mip)
            )
        else:
            print ("%8s %8.2f %8.2f %8.2f"
                   % ("MIP",elapsed_time_mip,
                      float("inf"),float("inf"))
            )
    gc.collect()

    
    @staticmethod
    def solveWithAlgorithm(problem,timeLimit):
        print "Using algorithm ..."
        start_time = time.time()

        # Sets the initial value of the thetas at the last stage
        
        Theta = {}
        for node in problem.scenario_tree.nodes[problem.stages]:
            Theta[node.id] = {}
            for team in problem.teams:
                Theta[node.id][team.name] = 1/(1 + pow(problem.discountRate,node.stage+1)) * team.getValue(node)

        print "Last stage thetas calculated ..."


        # Calculates the intermediate thetas by solving the subproblems

        t = problem.stages - 1
        while t >= 1:
            for node in problem.scenario_tree.nodes[t]:
                Theta[node.id] = {}
                for team in problem.teams:
                    sp = Subproblem(node,team,problem,Theta)
                    print "Model built"
                    sp.solve(timeLimit)
                    Theta[node.id][team.name] = sp.getObjective()
                    print "Theta %d - %s calculated. " % (node.id,team.name)
                    gc.collect()
            t = t -1

        # Solves the final model for the root node

        mr = ModelRoot(problem,Theta)
        mr.solve(timeLimit)
        elapsed_time_alg = time.time() - start_time

        print "%8s %8s %8s" % ("Method","Time","Objective")
        print "%8s %8.2f %8.2f" % ("ALG",elapsed_time_alg,mr.getObjective())


