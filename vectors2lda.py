#!/usr/bin/env python

import argparse
import numpy as np
import lda
import sys

parser = argparse.ArgumentParser(
	description='Project frequency vectors using LDA.')
parser.add_argument('--ntopics', type=int, default=20)
parser.add_argument('--niter', type=int, default=500)
parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
args = parser.parse_args()

vectors = np.loadtxt(args.input)
model = lda.LDA(n_topics=args.ntopics, n_iter=args.niter, random_state=1)
model.fit(vectors)
np.savetxt(args.output, model.doc_topic_, fmt='%.8f', delimiter='\t')