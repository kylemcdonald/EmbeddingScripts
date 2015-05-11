echo "Setting up Python 3"
pip3 install numpy gensim

echo "Setting up Python 2"
pip install numpy scipy scikit-learn matplotlib pylab
pip install git+https://github.com/dmishin/tsp-solver.git

echo "Downloading bh_tsne from http://lvdmaaten.github.io/tsne/"
curl -O http://lvdmaaten.github.io/tsne/code/bh_tsne.tar.gz
tar -zxvf bh_tsne.tar.gz
rm bh_tsne.tar.gz
cd bh_tsne

if [ -d /Applications/Xcode.app ]; then
	echo "Building bh_tsne for OSX..."
	g++ sptree.cpp tsne.cpp -o bh_tsne -O3 -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/System/Library/Frameworks/Accelerate.framework/Versions/Current/Frameworks/vecLib.framework/Headers/ -lcblas
else
	echo "Building bh_tsne for Linux..."
	g++ sptree.cpp tsne.cpp -o bh_tsne -O3 -I./CBLAS/include -L./ -lcblas
fi
echo "Done building bh_tsne"

echo "Downloading GoogleNews-vectors-negative300.bin.gz from https://code.google.com/p/word2vec/"
echo "(exit now if you don't want to use word2vec)"
curl -o "models/GoogleNews-vectors-negative300.bin.gz" -Lk "https://googledrive.com/host/0B7XkCwpI5KDYNlNUTTlSS21pQmM"
echo "Extracting GoogleNews-vectors-negative300.bin.gz"
gunzip models/GoogleNews-vectors-negative300.bin.gz
