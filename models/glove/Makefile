

# Unzip all text files within and touch em
%.txt: glove.twitter.27B.zip
	@unzip -o glove.twitter.27B.zip
	$@touch

# Download zip from Standford NLP
glove.twitter.27B.zip:
	wget --no-use-server-timestamps \
	http://nlp.stanford.edu/data/glove.twitter.27B.zip