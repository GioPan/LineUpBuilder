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
parser.add_argument('-pl','--playersFile',dest='playersFile', default = os.path.join("data","data/players.dat"),
                                        help='the file containing all the players of the problem (default: data/players.dat)')
parser.add_argument('-par','--paramsFile',dest='paramsFile', default = os.path.join("data","data/params.dat"),
                                        help='the file containing all the parameters of the problem (default: data/params.dat)')
args = parser.parse_args()


p = Generator.generate(args.playersFile,args.paramsFile)
solutions = Branching.solve(p,p.nLineUps,p.nPlayersRequired,p.nDifferences)
for node in solutions:
    print 'Solution node ', node.id
    print 'Objective ', node.objective
    print 'Team ', node.solution

