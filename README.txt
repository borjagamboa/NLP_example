
FILES:

	1. NLP_methods.py
	    Contains my own methods based on light modifications of the defined methods of the NLTK book
	    https://www.nltk.org/book/ch05.html
		Unigram Parser and NaiveBayesClassifier are inherit classes of RegexParser. One can test the methods from this
		file.
		I am using Bigram Tagging for the words and three different methods for chunking. The idea is to simulate a
		order processing tool for a restaurant.
	
	2. GUI.py
	    Just a simple GUI to test the models. It parses the sentence once to identify food and quantity

	3. GUI_dosparsers.py
		Same GUI, it parses the sentence twice though. At first it identifies the order and then it parses the order to
		differentiate between food and quantity

	4. Chunkers.py
	    Chunkers from NLTK book modified to apply them here
	
	5.ConsecutiveNPChunkTagger_trained.p, trained_spanish_tagger.p, Trained_unigram_chunker_None.py
	    Trained models that can be used to save time. They must be refresh once the grammar is modified.

IMPROVEMENTS:
	- Bigger corpus and more train sentences
	- Cleaner coding and structure
	- Split GUI and methods

	