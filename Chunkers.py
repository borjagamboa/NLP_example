# This file contains the necessary methods to carry out UnigramChunker
# and NaiveBayesClassifier

import nltk
import os, pickle

def npchunk_features(sentence, i, history):
    features = {"suffix(1)": sentence[i][-1:],
                "suffix(2)": sentence[i][-2:],
                "suffix(3)": sentence[i][-3:]}
    if i==0:
        features["prev-word"] = "<START>"
        features["prev-tag"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
        features["prev-tag"] = history[i-1]
    return features

class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents, n=None):
        if not os.path.exists("Trained_unigram_chunker_"+str(n)):
            print("Building new Unigram Chunker...")
            train_data = [[(t, c) for w, t, c in nltk.chunk.tree2conlltags(sent)]
                          for sent in train_sents]
            self.tagger = nltk.UnigramTagger(train_data)
            # Guardamos el tagger entrenado en el directorio actual
            try:
                with open("Trained_unigram_chunker_"+str(n), "wb") as file:
                    pickle.dump(self.tagger, file)
            except:
                print("Failed to save trained Unigram Chunker")
        else:
            print("Existing Unigram Chunker found")
            try:
                with open("Trained_unigram_chunker_"+str(n), "rb") as file:
                    self.tagger = pickle.load(file)
            except:
                print("Failed to load existing Unigram Chunker")

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)

class ConsecutiveNPChunkTagger(nltk.TaggerI):
            # N is used to differentiate trained models
    def __init__(self, train_sents, n=None):
        if not os.path.exists("ConsecutiveNPChunkTagger_trained_"+str(n)):
            print("Building new NaiveBayesClassifier...")
            train_set = []
            for tagged_sent in train_sents:
                untagged_sent = nltk.tag.untag(tagged_sent)
                history = []
                for i, (word, tag) in enumerate(tagged_sent):
                    featureset = npchunk_features(untagged_sent, i, history)
                    train_set.append((featureset, tag))
                    history.append(tag)
            self.classifier = nltk.NaiveBayesClassifier.train(train_set)
            try:
                with open("ConsecutiveNPChunkTagger_trained_"+str(n), "wb") as file:
                    pickle.dump(self.classifier, file)
            except:
                print("Failed to save new NaiveBayesClassifier")
        else:
            print("Existing trained NaiveBayesClassifier found")
            try:
                with open("ConsecutiveNPChunkTagger_trained_"+str(n), "rb") as file:
                    self.classifier = pickle.load(file)
            except:
                print("Failed to load existing NaiveBayesClassifier")

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI):
    def __init__(self, train_sents, n=None):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents, n)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.conlltags2tree(conlltags)


