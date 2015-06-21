#!/usr/bin/env python3

import argparse, sys, numpy
from gensim.models import Word2Vec

parser = argparse.ArgumentParser(
	description='Generate a .tsv of word2vec vectors for a word list.')
parser.add_argument('-i', '--input', default='data')
parser.add_argument('-m', '--model', default='models/GoogleNews-vectors-negative300.bin')
args = parser.parse_args()

print('Loading wordlist from {}/wordlist'.format(args.input))
wordlist = numpy.genfromtxt('{}/wordlist'.format(args.input), dtype='str')
words = []
vectors = []
print('Loading model from ' + args.model)
model = Word2Vec.load_word2vec_format(args.model, binary=True)
print('Looking up {} words.'.format(len(wordlist)))
for word in wordlist:
	if word in model:
		print('added: {}'.format(word))
		words.append(word)
		vectors.append(model[word])
	else:
		print('no vector: {}'.format(word))
print('Saving {:.2%} of the words.'.format(len(words) / len(wordlist)))
numpy.savetxt('{}/words'.format(args.input), words, fmt='%s')
print('Saving word vectors.')
numpy.savetxt('{}/vectors'.format(args.input), vectors, fmt='%.8f', delimiter='\t')
