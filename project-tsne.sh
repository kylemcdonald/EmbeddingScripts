set -x

function tsne {
	# run bhtsne in 2d and 3d
	if [ ! -f $1/$2.2d.tsne ]; then
		python bh_tsne/bhtsne.py -v -d 2 -p $2 -i $1/vectors -o $1/.cache
		cat $1/.cache | python normalize.py > $1/$2.2d.tsne
		rm $1/.cache
	fi
	if [ ! -f $1/$2.3d.tsne ]; then
		python bh_tsne/bhtsne.py -v -d 3 -p $2 -i $1/vectors -o $1/.cache
		cat $1/.cache | python normalize.py > $1/$2.3d.tsne
		rm $1/.cache
	fi
	# if tsne succeeds, plot the results, otherwise quit
	if [ -s $1/$2.2d.tsne ]; then
		if [ ! -f $1/$2-plot.pdf ]; then
			python plot-tsne.py -i $1 -p $2
		fi
	else
		rm $1/$2.2d.tsne
		rm $1/$2.3d.tsne
		exit
	fi
}

if [ ! -f $1/vectors ]; then
	# if there are no vectors
	if [ ! -f $1/tokens ]; then
		# and no tokens, use word2vec to create vectors
		python3 words-to-vectors.py -i $1
	else
		# otherwise create vectors from tokens
		# cp $1/wordlist $1/words
		# python tokens-to-vectors.py -i $1
		# or create correlation vectors
		python tokens-to-correlation.py -i $1
	fi
fi

tsne $1 1
# tsne $1 5
# tsne $1 10
# tsne $1 50
# tsne $1 100
# tsne $1 500
# tsne $1 1000
# tsne $1 5000