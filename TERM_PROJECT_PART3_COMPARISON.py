####### LING78100 TERM PROJECT
####### PART 3: WORD FREQUENCY COMPARISON

####### original code provided by Kyle Gorman 
####### edited by Winnie Yan 


# !/usr/bin/env python
"""Computes token-level log-odds ratios.

This computes token-level log-odds ratios using the informative Dirichlet prior
method introduced by:

Monroe, B. L., Colaresi, M. P., and Quinn, K. M. 2008.  Fightin' words: lexical
feature selection and evaluation for identifying the content of political
conflict. Political Analysis 16(4): 372-40.

The user provides the paths to three TSV files:

* frequencies in the first target corpus
* frequencies in the second target corpus
* frequencies in the third control corpus

All three TSV files should have two columns:

1. the token itself, normalized however is desired
2. the token frequency expressed as an integer

The tool then prints log-odds, in decreasing order, for any token present in
all three files."""


import logging
import math
import operator
import os

from typing import Dict, List


Freqs = Dict[str, int]


def _read_freq_tsv(path: str) -> Freqs:
    """Reads TSV file into dictionary."""
    result: Freqs = {}
    with open(path, "r", encoding = "utf-16") as source:
        for line in source:
            (token, freq) = line.rstrip().split("\t", 1)
            result[token] = int(freq)
    return result


def _log_odds_idp(fx: int, f3: int, nx: int, n3: int) -> float:
    """Computes log-odds ratio with informative prior counts."""
    num = fx + f3
    den = nx + n3 - fx - f3    
    return math.log2(num/den)


def _log_odds_ratio_idp(
    f1: int, f2: int, f3: float, n1: int, n2: int, n3: int
) -> float:
    """Computes log-odds ratio with an informative Dirichlet prior."""
    return _log_odds_idp(f1, n1, f3, n3) - _log_odds_idp(f2, n2, f3, n3)


def _var_log_odds_ratio_idp(f1: int, f2: int, f3: float) -> float:
    """Computes the sample variance of log-odds ratio with an informative Dirichlet prior."""
    return 1.0 / (f1 + f3) + 1.0 / (f2 + f3)


def main():
    logging.info("Reading frequencies")
    corpus1 = _read_freq_tsv("BushWordCount/BushSpeechesWordCount.txt")
    corpus2 = _read_freq_tsv("ObamaWordCount/ObamaSpeechesWordCount.txt")
    corpus3 = _read_freq_tsv("Reuters/ReutersWordCount.txt")
    logging.info("Computing denominators")
    n1 = sum(corpus1.values())
    n2 = sum(corpus2.values())
    n3 = sum(corpus3.values())
    pairs: List[Tuple[str, float]] = []
    logging.info("Computing supported tokens")
    supported_tokens: Set[str] = set(corpus1.keys())
    supported_tokens &= corpus2.keys()
    supported_tokens &= corpus3.keys()
    logging.info("Computing scores")
    for token in supported_tokens:
        f1 = corpus1[token]
        f2 = corpus2[token]
        f3 = corpus3[token]
        score = _log_odds_ratio_idp(f1, f2, f3, n1, n2, n3)
        
        # Removed because control corpus outweighed corpus 1 and 2 data
        '''if not args.raw:
            var = _var_log_odds_ratio_idp(f1, f2, f3)
            score /= math.sqrt(var)'''
        
        pairs.append((token, score))
    logging.info("Sorting scores")
    pairs.sort(reverse=True, key=operator.itemgetter(1))
    logging.info("Writing scores")
    
    directory = "Frequencies/"
    try:
        os.mkdir(directory)
    except OSError:
        print ("Creation of the directory %s failed" % directory)
    else:
        print ("Successfully created the directory %s " % directory)
    
    with open(directory + "FrequencyScores.txt", "w", encoding = "utf-16") as writer:
        for (token, score) in pairs:
            writer.write(f"{token}\t{score}\n")


main()