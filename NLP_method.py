# This script contains my own methods based on light modifications of the defined methods of the NLTK book. These
# are in Chunkers.py

import pickle
from nltk import UnigramTagger, BigramTagger
from nltk.corpus import cess_esp
from Chunkers import *

# RegexParser class, inherits from Unigram Parser and NaiveBayesClassifier
class RegexParser:
    # Initiate the tagger with corpus cess_esp and RegexParser with the grammar
    # train_sents will be used in next parsers
    def __init__(self, grammar):
        self.grammar = grammar
        self.tagger_sents = cess_esp.tagged_sents()
        self.train_sents = corpus = ["Me pones un pincho de tortilla, por favor?", "quiero una pizza margherita",
                                     "4 manzanas anda", "ocho pizzas", "2 chorizos, si tenéis"]

        # Automatically initiate tagger and parser
        self.get_tagger()
        self.init_regex()

    # Look for trained tagger or train a new one
    def get_tagger(self):
        # Confirm there is no existing tagger
        if not os.path.exists("trained_bigram_tagger.p"):
            print("Generating new tagger...")
            # Load tagged sentences from corpus CESS
            self.defaultTagger = nltk.DefaultTagger('nc0')
            self.unigram_tagger = UnigramTagger(self.tagger_sents, backoff=self.defaultTagger)
            self.bigram_tagger = BigramTagger(self.tagger_sents, backoff=self.unigram_tagger)

            # Save trained tagger in directory to reuse it
            try:
                with open("trained_bigram_tagger.p", "wb") as file:
                    pickle.dump(self.bigram_tagger, file)
            except:
                print("Failed to save tagger")
        else:
            print("Trained tagger exists")
            try:
                with open("trained_bigram_tagger.p", "rb") as file:
                    self.bigram_tagger = pickle.load(file)
                print("Tagger loading success")
            except:
                print("Failed to load tagger")

    def init_regex(self):
        self.regex_parser = nltk.RegexpParser(self.grammar)

    # Get parsed training sentences for the grammar model
    def get_train_sents_parsed(self):
        tagged_train_sents = []
        self.train_sents_parsed = []
        for sentence in self.train_sents:
            tokens = nltk.word_tokenize(sentence)
            tagged = self.bigram_tagger.tag(tokens)
            tagged_train_sents.append(tagged)
        for sentence in tagged_train_sents:
            parsed = self.regex_parser.parse(sentence)
            self.train_sents_parsed.append(parsed)

    # Función para parsear
    def regex_parse(self, sentence):
        print("\n######## REGEX PARSER ########\n")
        sentence_tokens = nltk.word_tokenize(sentence)
        tagged_sentence = self.bigram_tagger.tag(sentence_tokens)
        return self.regex_parser.parse(tagged_sentence)

class MyUnigramChunker(RegexParser):
    def __init__(self, grammar, n=None):
        super().__init__(grammar)

        self.train_sents_parsed = []
        self.get_train_sents_parsed()
        self.get_chunker(n)

    # Models from the book
    def get_chunker(self, n):
        self.unigram_chunker = UnigramChunker(self.train_sents_parsed, n)

    def parse(self, sentence):
        print("\n######## UNIGRAM PARSER ########\n")
        sentence_tokens = nltk.word_tokenize(sentence)
        tagged_sentence = self.bigram_tagger.tag(sentence_tokens)
        parsed = self.unigram_chunker.parse(tagged_sentence)
        return parsed

class NaiveBayesChunker(RegexParser):
    def __init__(self, grammar, n=None):
        super().__init__(grammar)

        self.train_sents_parsed = []
        self.get_train_sents_parsed()
        self.get_chunker(n)

    # models from book
    def get_chunker(self, n):
        self.chunker = ConsecutiveNPChunker(self.train_sents_parsed, n)

    def parse(self, sentence):
        print("\n######## NAIVEBAYESCLASSIFIER ########\n")
        sentence_tokens = nltk.word_tokenize(sentence)
        tagged_sentence = self.bigram_tagger.tag(sentence_tokens)
        parsed = self.chunker.parse(tagged_sentence)
        return parsed



def main():

    grammar_1 = r"""
        PETICIÓN: {<d.*><nc.*>?<aq.*>}
                {<d.*><nc.*>}
                {<Z><nc.*>}
                """
    grammar_2 = r"""
        COMIDA: {<nc.*>}
        CANTIDAD: {<dn.*>}
                  {<di.*>}
                  {<Z>}
                """
    # FRASE DE ENTRADA
    sentence = "tres pizzas"

    print("##### REGEX PARSER #####")
    regexParser = RegexParser(grammar_2)
    r_parsed = regexParser.regex_parse(sentence)
    for n in r_parsed:
        if isinstance(n, nltk.tree.Tree):
            if n.label() == 'FOOD':
                print("FOOD: " + str(n.leaves()[0][0]))
            elif n.label() == 'QUANTITY':
                print("QUANTITY: " + str(n.leaves()[0][0]) + "\n")
                pass

    print("##### UNIGRAM CHUNKER #####")
    unigram = MyUnigramChunker(grammar_2)
    u_parsed = unigram.parse(sentence)
    for n in u_parsed:
        if isinstance(n, nltk.tree.Tree):
            if n.label() == 'FOOD':
                print("FOOD: " + str(n.leaves()[0][0]))
            elif n.label() == 'QUANTITY':
                print("QUANTITY: " + str(n.leaves()[0][0]) + "\n")
                pass

    print("##### NAIVEBAYESCLASSIFIER #####")
    naive = NaiveBayesChunker(grammar_2)
    n_parsed = naive.parse(sentence)
    for n in n_parsed:
        if isinstance(n, nltk.tree.Tree):
            if n.label() == 'FOOD':
                print("FOOD: " + str(n.leaves()[0][0]))
            elif n.label() == 'QUANTITY':
                print("QUANTITY: " + str(n.leaves()[0][0]) + "\n")
                pass

if __name__ == '__main__':
    main()

