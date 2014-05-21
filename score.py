#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from utils import *

fn1 = sys.argv[1]
fn2 = sys.argv[2]

ref_data = load_wt(fn1)
tst_data = load_wt(fn2)

w_count = 0
w_accuracy = 0
oovw_count = 0
oovw_accuracy = 0

for wt_ref, wt_tst in zip(ref_data, tst_data):
  w_count += 1.0

  if wt_ref[1] == wt_tst[1]:
    w_accuracy += 1.0

  if wt_tst[0] == 'oov':
    oovw_count += 1.0
    if wt_ref[1] == wt_tst[1]:
      oovw_accuracy += 1.0



print "Tagging accuracy:    ", w_accuracy/w_count*100.0
if oovw_count:
  print "OOV Tagging accuracy:", oovw_accuracy/oovw_count*100.0
else:
  print "OOV Tagging accuracy: no OOVs"
print
print "Number of OOVs(%):  ", oovw_count/w_count*100.0


