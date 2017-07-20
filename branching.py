from problem import Problem
from model import Model
from node import Node


class Branching:
    
    @staticmethod
    def solve(problem,nSolutions,teamSize,differences):
        
        nodes = []
        solutions = []
        
        root = Node()
        m = Model(problem,root,differences)
        m.solve(60)
        Branching.addSolution(solutions,root,nSolutions)
        print root.solution
        nNodes = teamSize-differences+1
        print nNodes
        for i in range(1,nNodes+1):
            n = Node(root,i)
            m = Model(problem,n,differences)
            m.solve(60)
            Branching.addSolution(solutions,n,nSolutions)
            nodes.append(n)
            #print 'Solved node ',i
            #print n.solution

        return solutions
        
    @staticmethod
    def addSolution(solutions,solution,length):

        if len(solutions) < length:
            solutions.append(solution)
        else:
            if solution.objective > Branching.getSmallestValue(solutions):
                Branching.removeSmallest(solutions)
                solutions.append(solution)
            else:
                print 'Solution ', solution.id,' not better than the other available'
                

    @staticmethod
    def getSmallestValue(solutions):
        smallest = float("inf")
        for node in solutions:
            if node.objective < smallest:
                smallest = node.objective
        return smallest

    @staticmethod
    def removeSmallest(solutions):
        print 'Removing Smallest'
        smallestSolution = None
        smallestObjective = float("inf")
        for node in solutions:
            if node.objective < smallestObjective:
                print node.id,' ',node.objective
                smallestObjective = node.objective
                smallestSolution = node
        print 'Removing ', smallestSolution.id
        solutions.remove(smallestSolution)
        print solutions
        
