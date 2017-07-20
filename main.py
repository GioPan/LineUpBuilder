import os
from player import Player
from problem import Problem
from model import Model
from generator import Generator
from node import Node
from branching import Branching
import time
import argparse


p = Generator.generate("data.dat","params.dat")
solutions = Branching.solve(p,3,8,2)
for node in solutions:
    print 'Solution node ', node.id
    print 'Children n ', node.childrenNumber
    print 'Objective ', node.objective
    print 'Team ', node.solution

