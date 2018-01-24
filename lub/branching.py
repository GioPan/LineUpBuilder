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
        nNodes = teamSize-differences+1
        for i in range(1,nNodes+1):
            n = Node(root,i)
            m = Model(problem,n,differences)
            m.solve(60)
            if n.objective > float('-inf'):
                Branching.addSolution(solutions,n,nSolutions)
                nodes.append(n)
                
        nodes = Branching.fathomNodes(nodes,solutions)
        while len(nodes) > 0:
            node = Branching.getBestNode(nodes)
            print 'Exploring node ', node.id
            nodes.remove(node)
            for i in range(1,nNodes+1):
                n = Node(node,i)
                m = Model(problem,n,differences)
                m.solve(60)
                if n.objective > float('-inf'):
                    Branching.addSolution(solutions,n,nSolutions)
                    nodes.append(n)
            nodes = Branching.fathomNodes(nodes,solutions)
            
        return solutions
    
        
    @staticmethod
    def addSolution(solutions,solution,length):

        if len(solutions) < length:
            solutions.append(solution)
        else:
            if solution.objective > Branching.getSmallestValue(solutions):
                Branching.removeSmallest(solutions)
                solutions.append(solution)
                print 'New solution in the K-best'
                

    @staticmethod
    def getSmallestValue(solutions):
        smallest = float("inf")
        for node in solutions:
            if node.objective < smallest:
                smallest = node.objective
        return smallest

    @staticmethod
    def removeSmallest(solutions):
        smallestSolution = None
        smallestObjective = float("inf")
        for node in solutions:
            if node.objective < smallestObjective:
                smallestObjective = node.objective
                smallestSolution = node
        solutions.remove(smallestSolution)

    @staticmethod
    def getBestNode(nodes):
        bestNode = None
        bestObjective = float('-inf')
        for n in nodes:
            if n.objective > bestObjective:
                bestNode = n
                bestObjective = n.objective
        return bestNode
        
    @staticmethod
    def fathomNodes(nodes,solutions):
        nodesToExplore = []
        cutoff = Branching.getSmallestValue(solutions)
        for node in nodes:
            if node.objective <= cutoff:
                print node.id,' fathomed'                 
            else:
                nodesToExplore.append(node)
        return nodesToExplore
