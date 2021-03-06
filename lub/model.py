from __future__ import division
from pyomo.checker import plugins
from pyomo.pysp import plugins
from pyomo.gdp import plugins
from pyomo.mpec import plugins
from pyomo.neos import plugins
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.core import Var, plugins
from problem import Problem
from pyomo.opt import SolverStatus, TerminationCondition, plugins
from branchingConstraint import BranchingConstraint

class Model:
      "Instances of this class represent mathematical models for the Line Up problem"

      def __init__(self,problem,node,differences):
            self.problem = problem
            self.node = node
            # Creates the Pyomo model
            self.model = ConcreteModel()
            self.results = None

            # Creates the Sets
            self.model.Players = Set(initialize = self.playersNames(problem))
            self.model.Teams = Set(initialize = problem.teams)
            self.model.Roles = Set(initialize = problem.roles)
            self.model.Duplicates = Set(dimen=2, initialize = self.duplicates(problem))
            
            
            # Creates the variables                  
            self.model.x = Var(self.model.Players, domain=Binary)
            self.model.z = Var(self.model.Teams, domain=Binary)
            self.model.y = Var(self.model.Roles, domain=NonNegativeReals)

            # ============================================
            # Creates the objective
            # ============================================
            
            expression = 0
            for p in problem.players:
                  expression = (expression + p.projection * self.model.x[p.name])
            self.model.obj = Objective(expr = expression,sense=maximize)

            # ===========================
            # Creates the constraints
            # ===========================

            # Budget Constraints
            def maker_one(model):                      
                  lhs = 0
                  for p in problem.players:
                        lhs = lhs + (p.salary * model.x[p.name])
                  return lhs <= problem.budget
            
            self.model.constraints_one = Constraint(rule = maker_one)

            # Players Required
            def maker_two(model):                      
                  lhs = 0
                  for p in problem.players:
                        lhs = lhs + model.x[p.name]
                  return lhs == problem.nPlayersRequired
            
            self.model.constraints_two = Constraint(rule = maker_two)

            # Players per Role
            def maker_three(model,role):
                  lhs = 0
                  for p in problem.players:
                        if p.role == role:
                              lhs = lhs + model.x[p.name]
                  if role == 'GK':
                        return lhs == problem.nPlayersPerRole[role]
                  else:
                        return lhs == problem.nPlayersPerRole[role] + model.y[role]
            
            self.model.constraints_three = Constraint(self.model.Roles,rule = maker_three)

            
            def maker_four(model):
                  lhs = 0
                  for r in problem.roles:                              
                        lhs = lhs + model.y[r]
                  return lhs <= problem.extraPlayers
            
            self.model.constraints_four = Constraint(rule = maker_four)

            
            def maker_five(model,team):
                  lhs = 0
                  for p in problem.players:
                        if p.team == team:
                              lhs = lhs + model.x[p.name]
                  return lhs <= problem.getTeamSize(team) * model.z[team]
            
            self.model.constraints_five = Constraint(self.model.Teams, rule = maker_five) 

            def maker_six(model):
                  lhs = 0
                  for t in problem.teams:
                        lhs = lhs + model.z[t]
                  return lhs >= problem.minTeamsRepresented
            
            self.model.constraints_six = Constraint(rule = maker_six)

            def maker_seven(model,team):
                  lhs = 0
                  for p in problem.players:
                        if p.team == team:
                              lhs = lhs + model.x[p.name]
                  return lhs <= problem.maxNPlayersOfATeam
            
            self.model.constraints_seven = Constraint(self.model.Teams, rule = maker_seven)

            def maker_eight(model,player1,player2):
                  return model.x[player1] + model.x[player2] <= 1
            self.model.constraints_eight = Constraint(self.model.Duplicates, rule = maker_eight)

            ### Branching constraints
            
            branchingConstraints = []
            if(self.node.parent != None):
                  ### Inherits the branching constraints of the parent node
                  if self.node.parent.branchingConstraints != None:
                        for c in self.node.parent.branchingConstraints:                        
                              branchingConstraints.append(c)
                        
                  ### New branching constraints for the current nodes
                  ones = []
                  others = []
                  playerZero = None
                  for p in self.node.parent.solution:
                        if self.node.parent.solution.index(p) < self.node.childrenNumber - 1:
                              ones.append(p)
                        if self.node.parent.solution.index(p) > self.node.childrenNumber - 1:
                              others.append(p)
                        if self.node.parent.solution.index(p) == self.node.childrenNumber - 1:
                              playerZero = p

                  ### For each player which must be 1 it adds, as lhs, a list made only of the player
                  for p in ones:
                        branchingConstraints.append(BranchingConstraint([p],'eq',1))

                  ### For the player which myst be 0 it adds, as lhs, a list made only of the player
                  branchingConstraints.append(BranchingConstraint([playerZero],'eq',0))

                  ### For the remaining players it adds, as lhs, the list of the playes which then must be summed
                  lhs = []
                  for p in others:
                        lhs.append(p)
                  branchingConstraints.append(BranchingConstraint(lhs,'leq',len(self.node.parent.solution) - differences - (self.node.childrenNumber -1 )))

                  ### Saves the constraints in the node
                  self.node.branchingConstraints = branchingConstraints

                  ### Adds the constraints to the model
                  def makerBranching(model,constraint):
                        ### Creates the lhs as the sum of the players in constraints.lhs
                        lhs = 0
                        for p in constraint.lhs:
                              lhs = lhs + model.x[p]
                              
                        if constraint.verse == 'eq':
                              return lhs == constraint.rhs
                        elif constraint.verse == 'leq':
                              return lhs <= constraint.rhs
                        else:
                              return lhs >= constraint.rhs
                                              
                  self.model.branching = Constraint(branchingConstraints, rule = makerBranching)
                        
                  
                  
            

      def printModel(self):
            self.model.pprint()
         
      def solve(self,timeLimit):
            solver = SolverFactory('glpk')
           # solver.options['timeLimit'] = timeLimit
            self.results = solver.solve(self.model)

            if self.results.solver.termination_condition == TerminationCondition.infeasible:
                  self.node.objective = float('-inf')
                  self.node.solution = None
            else:
                  # Saves the necessary information in the node
                  self.node.objective = self.model.obj()
                  lineup = []
                  for p in self.problem.players:
                        if self.model.x[p.name].value != 0:
                              lineup.append(p.name)
                  self.node.solution = lineup

      def getStatus(self):
            print 'Printing status'
            self.model.load(self.results) # Loading solution into results object
            print 'Status ', self.results.solver.status, " ",  self.results.solver.termination_condition

      def getObjective(self):
            return self.model.obj()
      
      def printReport(self):
            for p in self.problem.players:
                  if self.model.x[p.name].value != 0:
                        print p.name,' ',p.role,' ',p.salary,' ',p.team                       
            print "Optimal objective %.2f" % self.model.obj()


      def printSolution(self):
            print("Solution")
            for v in self.model.component_data_objects(Var):
                  if v.value != 0:
                        print str(v), v.value

      
      def getNVariables(self):
            return self.model.nvariables()

      def getLowerBound(self):
            return self.results.Problem.Lower_bound
      
      def getUpperBound(self):
            return self.results.Problem.Upper_bound

      def getStatus(self):
            return self.results.Solver.Termination_condition

      def getNConstraints(self):
            return self.model.nconstraints()

      def duplicates(self,problem):
            pairs = []
            for p1 in problem.players:
                  for p2 in problem.players:
                        if((p1.duplicateCode != 0) &(p2.duplicateCode !=0) & (p1.duplicateCode == p2.duplicateCode) & (p1.name != p2.name)):
                              pairs.append((p1.name,p2.name))
            return pairs

      def playersNames(self,problem):
            names = []
            for p in problem.players:
                  names.append(p.name)
            return names            

      def teamPairs(self,problem):
            team_pairs = []
            for t1 in problem.teams:
                  for t2 in problem.teams:
                        if(t1.name != t2.name):
                              team_pairs.append((t1.name,t2.name))
            return team_pairs



            
