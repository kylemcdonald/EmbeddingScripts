# Embedding Scripts

A small collection of scripts to project/embed high dimensional data in two dimensions.

First run `./setup.sh` which will make sure python has the necessary libraries. It will also compile Barnes-Hut t-SNE from source, and download a word2vec model trained on the Google News dataset (a very large file that will decompress to ~3.6GB).

Each dataset is stored in a folder. Inside the folder you might have:

- `tokens` a tab-separated file of samples, where each column has one token in it. For example, one line of `cocktails/tokens` might look like `whiskey\tginger ale\tlemon`
- `wordlist` are words that are going to be projected using word2vec. For example `moods/wordlist` might read `happy\nsad\nhungry\ndelighted\n`
- `vectors` is a tab-separated list of high dimensional vectors used as input to the nonlinear projection algorithms.
- `words` is a list of labels for each of the lines in `vectors`. If the `vectors` are generated from `wordlist`, some words maybe not have word2vec definitions and `words` will be a subset of `wordlist`.

## Scripts

All Python scripts take `-i` as an argument for your input folder.


## word-to-vectors.py

This will generate `vectors` from `wordlist` using word2vec. It will also generate `words` which may be a subset of `wordlist`.

### tokens-to-vectors.py

This will generate binary `vectors` from `tokens`. So if you have 600 cocktails with 3-8 ingredients each, and 180 unique ingredients, the output will be 600 vectors of length 180 with 3-8 values set to 1.

### tokens-to-correlation.py

This will generate floating point `vectors` from `tokens` using the correlation/co-occurence between different tokens. If you have 600 cocktails with 3-8 ingredients each, and 180 unique ingredients, the output will be 180 vectors of length 180, and if there are ingredients that co-occur more often the value will be higher. Except for very complex datasets, most elements will be 0.

### plot-reduction.py

After generating `vectors` using one of the above techniques or by providing them directly, this script will attempt to run many nonlinear dimensionality reduction algorithms from scikit-learn on the input data. This is usually a good way to figure out what direction to head next.

### plot-correlation.py

This plots a basic correlation matrix, with the rows sorted by solving a travelling salesperson problem. It will also print a list of labels "sorted by similarity". Output is stored in the input folder as a png file.

### project.sh

This takes one argument for the input folder, and will generate `vectors` if they don't exist, either using `tokens-to-vectors.py` or `word-to-vectors.py` depending on which files are present, and then run `bh_tsne` with perplexities of 1, 5, 10, 50, 100 and 500 for both 2d projection and 3d projection. The results are stored in the input folder.

The visualization uses the 2d projection to determine locations for the labels/annotations, and to build a voronoi diagram where each cell is colored according to the 3d projection. This can sometimes help visualize whether an adjacency is "strong" (similar colors, nearby in a higher dimensional space) or "weak" (different colors, separated in a higher dimensional space).

### plot-tsne.py

Besides the argument for the input folder, this script also takes an argument for the perplexity to process using `-p`. It then takes the results of `bh_tsne` and projects it using the 2d projection for placing labels and 3d projection for choosing colors for voronoi cells in the background that can provide a high dimensional intuition for distances in some cases. Output image is saved in the input folder as a pdf file.