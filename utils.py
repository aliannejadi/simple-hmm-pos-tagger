#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

def save_data(file_name, sents):
  f = open(file_name, "w+")

  for s in sents:
    #f.write('SS\tSS\n')
    for w, t in s:
      f.write('%s\t%s\n' %(w, t))
    #f.write('SE\tSE\n')
  f.close()

def save_wt(file_name, wt):
  f = open(file_name, "w+")

  for w, t in wt:
    f.write('%s\t%s\n' %(w, t))
  f.close()

def load_wt(file_name):
  data = []
  f = open(file_name)

  for l in f:
    l = l.strip().split('\t')

    data.append((l[0], l[1]))

  return data

def save_dict(file_name, dct):
  f = open(file_name, "w+")

  for k in sorted(dct):
    f.write('%s\t%d\n' %(k, dct[k]))
  f.close()

def save_set(file_name, st):
  f = open(file_name, "w+")

  for e in sorted(st):
    f.write('%s\n' %(e))
  f.close()

def prune_dict(dct, n):
  d = {}

  for k in dct:
    if dct[k] > n:
      d[k] = dct[k]

  return d

def detect_missing_keys(dct1, dct2):
  dct1 = set(dct1.keys())
  dct2 = set(dct2.keys())

  return dct1 - dct2

def get_vocab(wt):
  vocab = Counter()

  for w, t in wt:
    vocab[w] += 1

  return vocab

def get_tags(wt):
  tags = Counter()

  for w, t in wt:
    tags[t] += 1

  return tags

def replace_rare_words(wt, dct):
  wtn = []

  for w, t in wt:
    if w not in dct:
      wtn.append(('oov', t))
    else:
      wtn.append((w, t))

  return wtn

