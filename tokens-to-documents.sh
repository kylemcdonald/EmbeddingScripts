cd $1
mkdir documents
cp tokens documents
cd documents
split -l 1 tokens
rm tokens