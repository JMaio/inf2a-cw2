# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.lex = {}

    def add(self, stem, cat):
        if cat not in self.lex:
            self.lex[cat] = []
        self.lex[cat] += [stem]

    def getAll(self, cat):
        try:
            return list(set(self.lex[cat]))
        except KeyError:
            return []


class FactBase:
    """stores unary and binary relational facts"""
    fb = {}

    def addUnary(self, pred, e1):
        if pred not in self.fb:
            self.fb[pred] = []
        self.fb[pred] += [e1]

    def addBinary(self, pred, e1, e2):
        if pred not in self.fb:
            self.fb[pred] = {}
        if e1 not in self.fb[pred]:
            self.fb[pred][e1] = []
        self.fb[pred][e1] += [e2]

    def queryUnary(self, pred, e1):
        try:
            return e1 in self.fb[pred]
        except KeyError:
            return False

    def queryBinary(self, pred, e1, e2):
        try:
            return e2 in self.fb[pred][e1]
        except KeyError:
            return False


import re
from nltk.corpus import brown
b = brown.tagged_words()
vb = [(w, t) for (w, t) in b if (t == "VB" or t == "VBZ")]

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""

    if s == "has":  # has
        hyp = "have"
    elif re.match(r"[a-z]+([^aeiousxyz]|([^cs]h))s\b", s):      # eats, tells, shows
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

    # check tags
    for (w, t) in c:
        if s == w:
            return hyp

    hits  = [(w, t) for (w, t) in vb if (w == s or w == hyp)]

    # print(c)
    t_s   = [(w, t) for (w, t) in hits if w == s and t == 'VBZ']
    if t_s:
        return hyp
    else:
        t_hyp = [t for (w, t) in hits if w == hyp and t == 'VB']
    if not (t_s or t_hyp):
        hyp = ""
    return hyp


def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_' + wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_' + wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_' + stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_' + stem, wlist[0], wlist[2])
    return msg

# End of PART A.

# fb = FactBase()
# fb.addUnary("duck","John")
# fb.addBinary("love","John","Mary")
# print(fb.queryUnary("duck","John")) # returns True
# print(fb.queryBinary("love","Mary","John")) # returns False

# print(verb_stem("tells"))
# print(verb_stem("says"))
# print(verb_stem("ties"))
# print(verb_stem("pays"))
# print(verb_stem("unifies"))
# print(verb_stem("ties"))
# print(verb_stem("says"))
# print(verb_stem("unties"))
# print(verb_stem("says"))
# print(verb_stem("says"))
# print(verb_stem("attaches"))
# print(verb_stem("analyzes"))
# print(verb_stem("has"))
# print(verb_stem("says"))
# print(verb_stem("ties"))
# print(verb_stem("bathes"))
# print(verb_stem("flys"))
# print(verb_stem("says"))
