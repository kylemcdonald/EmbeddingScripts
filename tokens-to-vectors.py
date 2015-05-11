#!/usr/bin/env python
import argparse, sys, numpy

parser = argparse.ArgumentParser(
	description='Generate a .tsv from tab separated tokens.')
parser.add_argument('-i', '--input', default='data')
args = parser.parse_args()

# read through file once to get all tokens
unique = set()
with open('{}/tokens'.format(args.input)) as f:
	for line in f:
		tokens = line.strip().split('\t')
		unique.update(tokens)

# read through file again to output vectors
vectors = []
with open('{}/tokens'.format(args.input)) as f:
	for line in f:
		vector = []
		tokens = line.strip().split('\t')
		for ref in unique:
			if ref in tokens:
				vector.append(1)
			else:
				vector.append(0)
		vectors.append(vector)

numpy.savetxt('{}/vectors'.format(args.input), vectors, fmt='%.1f', delimiter='\t')
