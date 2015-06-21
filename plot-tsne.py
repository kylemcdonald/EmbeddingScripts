#!/usr/bin/env python
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.backends.backend_pdf import PdfPages
from scipy.spatial import Voronoi, voronoi_plot_2d
from centroids import calculate_polygon_centroid

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

pad = .1

data2d = np.vstack((data2d, [-pad, -pad]))
data3d = np.vstack((data3d, [0, 0, 0]))
labels.append('')

data2d = np.vstack((data2d, [1+pad, -pad]))
data3d = np.vstack((data3d, [0, 0, 0]))
labels.append('')

data2d = np.vstack((data2d, [1+pad, 1+pad]))
data3d = np.vstack((data3d, [0, 0, 0]))
labels.append('')

data2d = np.vstack((data2d, [-pad, 1+pad]))
data3d = np.vstack((data3d, [0, 0, 0]))
labels.append('')

vor = Voronoi(data2d)

for i in range(len(data2d)):
    if vor.point_region[i] != -1:
		region = vor.regions[vor.point_region[i]]
		if not -1 in region:
			polygon = [vor.vertices[j] for j in region]
			# plt.fill(*zip(*polygon), color=data3d[i], edgecolor='black')
			plt.fill(*zip(*polygon), color=data3d[i])

font_size = 8
max_offset = .05
print('annotating')
for i in range(len(data2d)):
    if vor.point_region[i] != -1:
		region = vor.regions[vor.point_region[i]]
		if not -1 in region:
			polygon = [vor.vertices[j] for j in region]
			polygon = np.vstack((polygon, polygon[0])) # close polygon
			origin = np.array(data2d[i])
			centroid = np.array(calculate_polygon_centroid(polygon))
			if centroid[0] > 1 or centroid[0] < 0 or centroid[1] > 1 or centroid[1] < 0:
				centroid = origin
			offset = centroid - origin
			distance = np.linalg.norm(offset)
			if distance > max_offset:
				centroid = origin + offset * (max_offset / distance)
			plt.annotate(labels[i], centroid,
				size=font_size, va = 'center', ha = 'center', color='white',
				path_effects=[pe.withStroke(linewidth=2, foreground='black', alpha=.5)])
plt.axis('off')
plt.xlim([0,1])
plt.ylim([0,1])

print('writing pdf')
pp = PdfPages('{0}/{1}-plot.pdf'.format(args.input, args.perplexity))
plt.savefig(pp, format='pdf', bbox_inches=0, pad_inches=0, aspect='normal')
pp.close()
