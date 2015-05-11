#!/usr/bin/env python

import argparse
import nltk
import sys

parser = argparse.ArgumentParser(
	description='Convert text into tokens, then into word vectors.')
parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-w', '--window', type=int, default=100)
parser.add_argument('-s', '--stride', type=int, default=100)
parser.add_argument('-m', '--minfreq', type=int, default=3)
parser.add_argument('-v', '--vocabulary', action='store_true')
args = parser.parse_args()

raw = args.input.read().decode('ascii', 'ignore').lower()
tokens = nltk.word_tokenize(raw)
text = nltk.Text(tokens)
fdist = nltk.FreqDist(text)
# remove rare words
word_set = set(map(lambda x: x[0], filter(lambda x: x[1] >= args.minfreq, fdist.iteritems())))

def document_features(sub_set, word_set):
	vec = []
	for word in word_set:
	    if word in sub_set:
	    	vec.append(str(int(sub_set[word])))
	    else:
	    	vec.append('0')
	print ' '.join(vec)

if args.vocabulary:
	print '\n'.join(word_set)
	print len(word_set)
else:
	for offset in range(0, len(tokens) - args.window, args.stride):
		text = nltk.Text(tokens[offset:(offset + args.window)])
		sub_set = nltk.FreqDist(text)
		document_features(sub_set, word_set)
		# print ' '.join(text)
