#!/usr/bin/env python
import argparse, sys, numpy
from collections import defaultdict

parser = argparse.ArgumentParser(
	description='Generate a .tsv from tab separated tokens using correlation of the tokens.')
parser.add_argument('-i', '--input', default='data')
args = parser.parse_args()

unique = set()
counts = defaultdict(
	lambda: defaultdict(
		lambda: 0.0))
with open('{}/tokens'.format(args.input)) as f:
	for line in f:
		tokens = line.strip().split('\t')
		unique.update(tokens)
		for a in tokens:
			for b in tokens:
				counts[a][b] += 1
				counts[b][a] += 1

words = []
vectors = []
for a in unique:
	words.append(a)
	vector = []
	for b in unique:
		vector.append(counts[a][b])
	vectors.append(vector / numpy.max(vector))

numpy.savetxt('{}/words'.format(args.input), words, fmt='%s')
numpy.savetxt('{}/vectors'.format(args.input), vectors, fmt='%.8f', delimiter='\t')
