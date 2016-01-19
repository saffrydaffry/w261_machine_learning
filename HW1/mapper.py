#!/usr/bin/python
import re
import sys
import os
import numpy as np

# store a regex expression into a pattern object
# that seeks words including underscores and single quotes
WORD_RE = re.compile(r"[\w']+")
TRUTH_RE = re.compile(r"\t(\d)\t")

# file input
filename = sys.argv[1]

# for this part, just assume word_list is length 1
word_list = sys.argv[2]

# Avoid KeyError if no data in chunk
#counts_dict = dict.fromkeys(['0', '1'], 0)
counts_dict = {}

spam_count = 0
ham_count  = 0

with open(filename, 'rU') as f:
    for line in f.readlines():
        # Remove punctuation
        line = re.sub(r'[^\w\s]','',line)
        truth = TRUTH_RE.findall(line)[0]
        if truth == '1':
            spam_count += 1
        else:
            ham_count += 1
        for category in ['0','1']:
            counts_dict[category] = {}
            
            for word in word_list.split():
                
                counts = [1 if x == word else 0 for x in WORD_RE.findall(line)]
                counts = np.array(counts)  
                
                if counts.sum() > 0:
                    count = 1
                    counts_dict[category][word] = counts_dict[category].get(word, 0) + int(count)
                else:
                    counts_dict[category][word] = 0
               

for category, word_dictionary in counts_dict.iteritems():
    for words, count in counts_dict[category].iteritems():
        print category + "\t" + words + "\t" + str(count) + "\t" + str(spam_count) +"\t" + str(ham_count)
        