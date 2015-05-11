#!/usr/bin/env python
import argparse
from numpy import loadtxt, genfromtxt, corrcoef, sum, log, arange
from numpy.random import rand
from scipy.spatial.distance import cdist
from pylab import pcolor, show, colorbar, xticks, yticks, savefig
from tsp_solver.greedy import solve_tsp

parser = argparse.ArgumentParser(
	description='Plot tsne output.')
parser.add_argument('-i', '--input', default='data')
args = parser.parse_args()

data = loadtxt('{0}/vectors'.format(args.input))

labels = []
with open('{}/words'.format(args.input)) as f:
	for line in f:
		labels.append(line.strip())

distanceMatrix = cdist(data, data, 'euclidean')
path = solve_tsp(distanceMatrix)
pcolor(data[path], cmap='binary')
savefig('{}/correlation.png'.format(args.input), figsize=(4,4), dpi=600)

for i in path:
	print(labels[i])
