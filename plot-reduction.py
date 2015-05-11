#!/usr/bin/env python
import argparse
from time import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble, lda, random_projection)

parser = argparse.ArgumentParser(
  description='Plot many kinds of dimensionality reduction algorithms.')
parser.add_argument('-i', '--input', default='data')
args = parser.parse_args()

y = []
with open('{}/words'.format(args.input)) as f:
  for line in f:
    y.append(line.strip())

X = np.loadtxt('{}/vectors'.format(args.input))
n_samples, n_features = X.shape
n_neighbors = 30


#----------------------------------------------------------------------
# Scale and visualize the embedding vectors
def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(y[i]),
                 # color=plt.cm.Set1(y[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})

    if hasattr(offsetbox, 'AnnotationBbox'):
        # only print thumbnails with matplotlib > 1.0
        shown_images = np.array([[1., 1.]])  # just something big
        for i in range(X.shape[0]):
            dist = np.sum((X[i] - shown_images) ** 2, 1)
            if np.min(dist) < 4e-3:
                # don't show points that are too close
                continue
            # shown_images = np.r_[shown_images, [X[i]]]
            # imagebox = offsetbox.AnnotationBbox(
            #     offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
            #     X[i])
            # ax.add_artist(imagebox)
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)


#----------------------------------------------------------------------
# Plot images
# n_img_per_row = 20
# img = np.zeros((10 * n_img_per_row, 10 * n_img_per_row))
# for i in range(n_img_per_row):
#     ix = 10 * i + 1
#     for j in range(n_img_per_row):
#         iy = 10 * j + 1
#         img[ix:ix + 8, iy:iy + 8] = X[i * n_img_per_row + j].reshape((8, 8))

# plt.imshow(img, cmap=plt.cm.binary)
# plt.xticks([])
# plt.yticks([])
# plt.title('A selection from the 64-dimensional digits dataset')


#----------------------------------------------------------------------
# Random 2D projection using a random unitary matrix
# print("Computing random projection")
# rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
# X_projected = rp.fit_transform(X)
# plot_embedding(X_projected, "Random Projection")


#----------------------------------------------------------------------
# Projection on to the first 2 principal components

try:
  print("Computing PCA projection")
  t0 = time()
  X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
  plot_embedding(X_pca,
                 "Principal Components projection (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Projection on to the first 2 linear discriminant components

try:
  print("Computing LDA projection")
  X2 = X.copy()
  X2.flat[::X.shape[1] + 1] += 0.01  # Make X invertible
  t0 = time()
  X_lda = lda.LDA(n_components=2).fit_transform(X2, y)
  plot_embedding(X_lda,
                 "Linear Discriminant projection (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Isomap projection dataset
try:
  print("Computing Isomap embedding")
  t0 = time()
  X_iso = manifold.Isomap(n_neighbors, n_components=2).fit_transform(X)
  print("Done.")
  plot_embedding(X_iso,
                 "Isomap projection (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Locally linear embedding dataset
try: 
  print("Computing LLE embedding")
  clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                        method='standard')
  t0 = time()
  X_lle = clf.fit_transform(X)
  print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
  plot_embedding(X_lle,
                 "Locally Linear Embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Modified Locally linear embedding dataset
try:
  print("Computing modified LLE embedding")
  clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                        method='modified')
  t0 = time()
  X_mlle = clf.fit_transform(X)
  print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
  plot_embedding(X_mlle,
                 "Modified Locally Linear Embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# HLLE embedding dataset
try:
  print("Computing Hessian LLE embedding")
  clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                        method='hessian')
  t0 = time()
  X_hlle = clf.fit_transform(X)
  print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
  plot_embedding(X_hlle,
                 "Hessian Locally Linear Embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# LTSA embedding dataset
try:
  print("Computing LTSA embedding")
  clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                        method='ltsa')
  t0 = time()
  X_ltsa = clf.fit_transform(X)
  print("Done. Reconstruction error: %g" % clf.reconstruction_error_)
  plot_embedding(X_ltsa,
                 "Local Tangent Space Alignment (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# MDS  embedding dataset
try:
  print("Computing MDS embedding")
  clf = manifold.MDS(n_components=2, n_init=1, max_iter=100)
  t0 = time()
  X_mds = clf.fit_transform(X)
  print("Done. Stress: %f" % clf.stress_)
  plot_embedding(X_mds,
                 "MDS embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Random Trees embedding dataset
try:
  print("Computing Totally Random Trees embedding")
  hasher = ensemble.RandomTreesEmbedding(n_estimators=200, random_state=0,
                                         max_depth=5)
  t0 = time()
  X_transformed = hasher.fit_transform(X)
  pca = decomposition.TruncatedSVD(n_components=2)
  X_reduced = pca.fit_transform(X_transformed)

  plot_embedding(X_reduced,
                 "Random forest embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# Spectral embedding dataset
try:
  print("Computing Spectral embedding")
  embedder = manifold.SpectralEmbedding(n_components=2, random_state=0,
                                        eigen_solver="arpack")
  t0 = time()
  X_se = embedder.fit_transform(X)

  plot_embedding(X_se,
                 "Spectral embedding (time %.2fs)" %
                 (time() - t0))
except:
  pass

#----------------------------------------------------------------------
# t-SNE embedding dataset
try:
  print("Computing t-SNE embedding")
  tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
  t0 = time()
  X_tsne = tsne.fit_transform(X)

  plot_embedding(X_tsne,
    "t-SNE embedding (time %.2fs)" %
    (time() - t0))
except:
  pass
  
plt.show()
