all: cleanup

# Clean up archive
cleanup: glove.twitter.27B.200d.txt
	rm *.zip


# Unzip all text files within and touch em
glove.twitter.27B.200d.txt: glove.twitter.27B.zip
	unzip -o glove.twitter.27B.zip
	touch *.txt

# Download zip from Standford NLP
glove.twitter.27B.zip:
	wget --no-use-server-timestamps \
	http://nlp.stanford.edu/data/glove.twitter.27B.zip
