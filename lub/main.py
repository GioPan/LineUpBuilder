import os
from player import Player
from problem import Problem
from model import Model
from generator import Generator
from node import Node
from branching import Branching
import time
import argparse


# =====================
# Command line interpreter
# =====================
parser = argparse.ArgumentParser(description='K-Best LineUps Builder.')
parser.add_argument('-l','--listOfPlayers',dest='playersFile', default = os.path.join("data","players.dat"),
                                        help='the file containing the list of all the players considered (default: data/players.dat)')
parser.add_argument('-p','--paramsFile',dest='paramsFile', default = os.path.join("data","params.dat"),
                                        help='the file containing all the parameters of the problem (default: data/params.dat)')
parser.add_argument('-o','--outputFile',dest='outputFile', default = os.path.join("output.txt"),
                                        help='the file where the solution should be printed (default: output.txt)')

args = parser.parse_args()


p = Generator.generate(args.playersFile,args.paramsFile)
solutions = Branching.solve(p,p.nLineUps,p.nPlayersRequired,p.nDifferences)

# Prints the results to file
f = open(args.outputFile,'w')
i = 1
for node in solutions:
    f.write('##############\n')
    f.write('Solution #{0} \n'.format(i))
    f.write('Objective value : {0}\n'.format(node.objective))
    f.write('##############\n')
    f.write('Team :\n')
    for player in node.solution:
        f.write('{0}\n'.format(player))
    i += 1
f.close()
