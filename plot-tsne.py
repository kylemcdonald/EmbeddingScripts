#!/usr/bin/env python
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.spatial import Voronoi, voronoi_plot_2d

parser = argparse.ArgumentParser(
	description='Plot tsne output.')
parser.add_argument('-i', '--input', default='data')
parser.add_argument('-p', '--perplexity', default=1)
args = parser.parse_args()

labels = []
with open('{}/words'.format(args.input)) as f:
	for line in f:
		labels.append(line.strip())

data2d = np.loadtxt('{0}/{1}.2d.tsne'.format(args.input, args.perplexity))
data3d = np.loadtxt('{0}/{1}.3d.tsne'.format(args.input, args.perplexity))

plt.figure(figsize=(10, 10), dpi=100)

vor = Voronoi(data2d)
for i in range(len(data2d)):
    if vor.point_region[i] != -1:
    	region = vor.regions[vor.point_region[i]]
    	if not -1 in region:
	        polygon = [vor.vertices[j] for j in region]
	        plt.fill(*zip(*polygon), color=data3d[i])

for label, x, y in zip(labels, data2d[:, 0], data2d[:, 1]):
    plt.annotate(label, xy = (x, y), size = 2, va = 'center', ha = 'center')

plt.axis('off')
plt.xlim([0,1])
plt.ylim([0,1])

pp = PdfPages('{0}/{1}-plot.pdf'.format(args.input, args.perplexity))
plt.savefig(pp, format='pdf', bbox_inches='tight', pad_inches=0, aspect='normal')
pp.close()
