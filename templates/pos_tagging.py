# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    with open("sentences.txt", "r") as f:
        cands = {}      # make set for recognising pos tags
        pos = []        # store all (word, tag) tuples
        plurals = []
        for line in f:
            pos += [(w,t) for (w,t) in (tuple(p.split('|')) for p in line.split()) if (t == "NNS" or t == "NN")]
        for (w, t) in pos:
            try:
                if t not in cands[w]:
                    cands[w] += [t]
            except KeyError:
                cands[w] = [t]

        for w in cands:
            if len(cands[w]) == 2:
                plurals += [w]
        return plurals

unchanging_plurals_list = unchanging_plurals()
# print(sorted(unchanging_plurals_list))

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    if s in unchanging_plurals_list:
        return s
    elif s[-3:] == "men":
        return s[:-3] + "man"
    else:
        # blatant copy from verb_stem
        if re.match(r"[a-z]+([^aeiousxyz]|([^cs]h))s\b", s):        # eats, tells, shows
            hyp = s[:-1]
        elif re.match(r"[a-z]+[aeiou]ys\b", s):                     # pays, buys
            hyp = s[:-1]
        elif re.match(r"[a-z]+[^aeiou]ies\b", s):                   # flies, tries, unifies
            hyp = s[:-3] + 'y'                                      # assume rules followed if pluralised
        elif re.match(r"[^aeiou]ies\b", s):                         # dies, lies, ties
            hyp = s[:-1]
        elif re.match(r"[a-z]+([ox]|[cs]h|[s]s|[z]z)es\b", s):      # goes, boxes, attaches, washes, dresses, fizzes
            hyp = s[:-2]
        elif re.match(r"[a-z]+[^sz](se|ze)s\b", s):                 # loses, dazes, lapses, analyses
            hyp = s[:-1]
        elif re.match(r"[a-z]+([^iosxz]|([^cs]h))es\b", s):         # likes, hates, bathes
            hyp = s[:-1]
        else:
            hyp = ""
        return hyp

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tagset = ['P', 'N', 'A', 'I', 'T']
    base_tags = []
    full_tags = []
    for tag in tagset:
        base_tags += [tag for w in lx.getAll(tag) if w == wd]
        base_tags += [tag for v in lx.getAll(tag) if v == verb_stem(wd)]
        base_tags += [tag for n in lx.getAll(tag) if n == noun_stem(wd)]
    # if wd in function_words:
    #     tags += [t for (w, t) in function_words_tags if w == wd]
    if 'P' in base_tags:
        full_tags += ['P']
    if 'N' in base_tags:
        if wd in unchanging_plurals_list:
            full_tags += ['Np', 'Ns']
        elif noun_stem(wd):
            full_tags += ['Np']
        else:
            full_tags += ['Ns']
    if 'A' in base_tags:
        full_tags += ['A']
    if 'T' in base_tags:
        if verb_stem(wd):
            full_tags += ['Ts']
        else:
            full_tags += ['Tp']
    if 'I' in base_tags:
        if verb_stem(wd):
            full_tags += ['Is']
        else:
            full_tags += ['Ip']
    if wd in function_words:
        full_tags += [t for (w, t) in function_words_tags if w == wd]

    return full_tags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.

lx = Lexicon()
lx.add("John","P")
lx.add("Mary","P")
lx.add("like","T")
lx.add("likes","T")
lx.add("fish","T")
lx.add("fish","I")
lx.add("fish","N")
lx.getAll("P")
print tag_words(lx, ["John", "fish"])
