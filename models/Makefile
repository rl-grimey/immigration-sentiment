###############################################################################
# Makefile to download and convert GloVe models to word2vec					  #
###############################################################################

ZIP=glove/glove.twitter.27B.zip
DIM:= 25 50 100 200
GLOVEFS:=$(foreach d, $(DIM), glove/glove.twitter.27B.$(d)d.txt)
WORDFS:=$(foreach d, $(DIM), word2vec/word2vec.twitter.27B.$(d)d.txt)
CONDA= $(shell which conda)
SCRIPT=python -m gensim.scripts.glove2word2vec

all: clean

# Download GloVe zip from internet
$(ZIP):
	mkdir -p glove
	mkdir -p word2vec	
	wget --no-use-server-timestamps -O $(ZIP) \
	http://nlp.stanford.edu/data/glove.twitter.27B.zip

# Unzip GloVe zip file and touch
$(GLOVEFS): $(ZIP)
	unzip -j -n $(ZIP) -d glove/

# Each word2vec is created directly from it's corresponding 
# GloVe n-dimension vector
$(WORDFS): $(GLOVEFS)
	$(foreach dim, $(DIM), \
		python -m gensim.scripts.glove2word2vec \
			-i glove/glove.twitter.27B.$(dim)d.txt -o word2vec/word2vec.twitter.27B.$(dim)d.txt;)


# Remove the downloaded zip file after the word2vec vectors are made
clean: $(WORDFS)
	rm $(ZIP)

.PHONY: clean
