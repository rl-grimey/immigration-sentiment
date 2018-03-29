###############################################################################
# Makefile to download and convert GloVe models to word2vec					  #
###############################################################################

ZIP=glove/glove.twitter.27B.zip
DIM := 25 50 100 250
GLOVEFS := $(foreach d, $(DIM), glove/glove.twitter.$(d)d.txt)
WORDFS := $(foreach d, $(DIM), word2vec/word2vec.twitter.$(d)d.txt)
SCRIPT=python -m gensim.scripts.glove2word2vec

all: clean

# Download GloVe zip from internet
$(ZIP):
	mkdir -p glove/
	wget --no-use-server-timestamps -o $(ZIP) \
	http://nlp.stanford.edu/data/glove.twitter.27B.zip

# Unzip GloVe zip file and touch
$(GLOVEFS): $(ZIP)
	unzip -j -n $(ZIP) -d glove/
	touch $(GLOVEFS)

# Each word2vec is created directly from it's corresponding 
# GloVe n-dimension vector
$(WORDFS): $(GLOVEFS)
	mkdir -p word2vec/
	$(foreach d, $(DIM), \
		$(shell cp glove/a.b.$(d)d.txt -T word2vec/c.d.$(d)d.txt))

# Remove the downloaded zip file after the word2vec vectors are made
clean: $(WORDFS)
	rm $(ZIP)