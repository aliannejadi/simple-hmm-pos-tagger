#!/usr/bin/env python

__author__ = 'moli'

import sys
import math

def main():

    input = sys.stdin
    output = sys.stdout
    tst = sys.argv[1]
    
    HMM = hmm()
    
    lines = input.readlines()
    
    HMM.read_train_stream(lines)
    
    HMM.train(lines)

    HMM.test(open(tst).readlines(), output)

class hmm:
    alpha = 0.000001
    def __init__(self):
        self.labels = dict()
        self.relabels = dict()
        self.words = dict()
        
        self.label_counter = 1 # 0 is reserved for the start state.
        self.word_counter = 0
        
        self.emission = None
        self.transition = None
        self.start = None
        self.seq_num = 0
        
        self.word_counts = None
        self.label_counts = None
        
    
    # Reads the training data and builds the three dictionaries of words, labels and reindexer of the labels for decoding.    
    def read_train_stream(self, train_lines):
        for l in train_lines:
            tokens = l.strip().split('\t')
            if not self.labels.has_key(tokens[1]):
                self.labels[tokens[1]] = self.label_counter
                self.relabels[self.label_counter] = tokens[1]
                self.label_counter += 1
            if not self.words.has_key(tokens[0]):
                self.words[tokens[0]] = self.word_counter
                self.word_counter += 1
    
    # Reads the training data again and builds the Start, Emission and Transition matrices.           
    def train(self, train_lines):
        # Initialization
        self.emission = [[0 for x in xrange(self.label_counter)] for x in xrange(self.word_counter)]
        self.transition = [[0 for x in xrange(self.label_counter)] for x in xrange(self.label_counter)]
        self.start = [0 for x in xrange(self.label_counter)]    
        self.word_counts = [0 for x in xrange(self.word_counter)]
        self.label_counts = [0 for x in xrange(self.label_counter)]
        
        previous_state = 0
        
        # In the first phase we count the observations.
        for l in train_lines:
            tokens = l.strip().split('\t')
            curr_state = self.labels[tokens[1]]
            curr_word = self.words[tokens[0]]
            
            if previous_state == 0:
                self.start[curr_state] += 1
            
            self.transition[curr_state][previous_state] += 1
            self.emission[curr_word][curr_state] += 1
        
            self.word_counts[curr_word] += 1
            self.label_counts[curr_state] += 1
        
            previous_state = curr_state
            
            if curr_word == '.': #this is the end of the current sequence
                previous_state = 0
                self.seq_num += 1
        
        # We then compute the log-likelihood of the observations.
        for w in range(self.word_counter):
            for l in range(self.label_counter):
                self.emission[w][l] = math.log((self.emission[w][l] + self.alpha) / (self.word_counts[w] + (self.alpha * self.label_counter)))
        
        for l in range(self.label_counter):
            self.start[l] = math.log((self.start[l] + self.alpha) / (self.seq_num + (self.alpha * self.label_counter)))
            for l2 in range(self.label_counter):
                self.transition[l][l2] = math.log((self.transition[l][l2] + self.alpha) / (self.label_counts[l] + (self.alpha * self.label_counter)))

    def viterbi(self, observations):
        V = [{}]
        path = {}
    
        oov_emission = [math.log(self.alpha) for x in range(self.label_counter)]
    
        if self.words.has_key(observations[0]):
            emit = self.emission[self.words[observations[0]]]
        else:
            emit = oov_emission
        # Initialize base cases (t == 0)
        for y in range(self.label_counter):
            V[0][y] = self.start[y] + emit[y]
            path[y] = [y]
    
        # Run Viterbi for t > 0
        for t in range(1, len(observations)):
            V.append({})
            newpath = {}
    
            for y in range(self.label_counter):
                if self.words.has_key(observations[t]):
                    emit = self.emission[self.words[observations[t]]]
                else:
                    emit = oov_emission
                (prob, state) = max((V[t-1][y0] + self.transition[y0][y] + emit[y], y0) for y0 in range(self.label_counter))
                V[t][y] = prob
                newpath[y] = path[state] + [y]
                
            path = newpath
        n = 0           
        if len(observations)!=1:
            n = t

        (prob, state) = max((V[n][y], y) for y in range(self.label_counter))
        return (prob, path[state])
    
    def test(self, test_lines, output_file):
        i = 0
        while i < len(test_lines):
            obs = []
            word = test_lines[i].split('\t')[0]
            while word != '.' and i < len(test_lines):
                word = test_lines[i].split('\t')[0]
                obs.append(word)
                i += 1
            
            vit_out = self.viterbi(obs)
            preds = [self.relabels[x] for x in vit_out[1]]
            
            for o,l in zip(obs,preds):
                output_file.write(o + '\t' + l + '\n')
                
if __name__ == "__main__":
    main()