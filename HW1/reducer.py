#!/usr/bin/python

import sys
import numpy as np
import re
from math import log

WORD_RE = re.compile(r"[\w']+")
TRUTH_RE = re.compile(r"\t(\d)\t")
files_list = sys.argv[1].split()

## training, gather all the counts and calculate corpus-wide priors, etc
## data come in as strings, 
## TRUTH WORD COUNT SPAM_COUNT HAM_COUNT
counts_dict = {}
for category in ['0','1']:
    counts_dict[category] = {}

spam_total = 0
ham_total  = 0

for f in files_list:
    with open(f, 'rU') as countfile:
        for line in countfile.readlines():
            truth, word, count, spam_count, ham_count = line.split('\t')
            counts_dict[truth][word] = counts_dict[truth].get(word, 0) + int(count)
        spam_total += int(spam_count)
        ham_total  += int(ham_count)
        
priors = {'0': float(ham_total)/(spam_total+ham_total),
          '1': float(spam_total)/(spam_total+ham_total)}

prior_counts = {'0': float(ham_total),
          '1': float(spam_total)}

print "Priors are: "
for category in priors:
    print category + " " + str(priors[category]) + "\n"

spam_vocab = counts_dict['1'].keys()
ham_vocab  = counts_dict['0'].keys()

spam_vocab_n = len(counts_dict['1'].keys())
ham_vocab_n  = len(counts_dict['0'].keys())

## although we are not implementing Laplace Transform
# probably don't need these next two lines
#vocab = union(spam_vocab, ham_vocab)
#vocab_n = len(vocab)

## Calculate conditional probabilities
## P(word | class) 
posteriors = {}
for category in ['0', '1']:
    posteriors[category] = {}
    for word in counts_dict[category].keys():
        posteriors[category][word] = float(counts_dict[category][word])/prior_counts[category]

print "\nPosteriors are: "
for category in posteriors:
    for word in posteriors[category]:
        print word + " in class " + category + " " + str(posteriors[category][word]) + "\n"

## Testing the classifer
## Without laplacian transform 
print "DOC_ID | TRUTH | CLASS "
print "=======================\n"

doc_id = 0
correct = 0
with open("enronemail_1h.txt", 'rU') as testdata:
    for line in testdata.readlines():
        score = [0,0]
        line = re.sub(r'[^\w\s]','',line)
        truth = TRUTH_RE.findall(line)[0]
        
        for category in ['0', '1']:
            idx = int(category)
            score[idx] = log(priors[category])
            #score[idx] =  priors[category]
            for word in posteriors[category]:
                if word in WORD_RE.findall(line):
                    score[idx] += log(float(posteriors[category][word])+1)
                    #score[idx] *= float(posteriors[category][word])
                #print "\n", idx, score[idx], category, word
        score = np.array(score)
        prediction = score.argmax()
        doc_id +=1
        
        if int(prediction) == int(truth):
            correct +=1
        print str(doc_id) + "\t" + truth + "\t" +str(prediction) +  " " +str(score[0]) + " " + str(score[1])

accuracy = float(correct)/doc_id*100.0
print "Accuracy: ", accuracy