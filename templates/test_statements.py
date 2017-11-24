import pytest
from statements import Lexicon, FactBase, verb_stem, process_statement

# Short guide:
# pip install -U pytest

# Run $ pytest test_statements.py::test_processing to run single testcase
# or  $ pytest to run them all.

# test_stemming_with_tagging is probably very slow


word2stem = {
    "eats": 'eat',
    "tells": 'tell',
    "shows": 'show',

    "pays": "pay",
    "buys": 'buy',

    "flies": "fly",
    "tries": "try",
    "unifies": "unify",

    "dies": "die",
    "lies": "lie",
    "ties": "tie",

    "goes": "go",
    "boxes": "box",
    "attaches": "attach",
    "washes": "wash",
    "dresses": "dress",
    "fizzes": "fizz",

    "loses": "lose",
    "dazes": "daze",
    "lapses": "lapse",
    "analyses": "analyse",

    "has": "",

    "likes": "like",
    "hates": "hate",
    "bathes": "bathe",

    "flys": "",
}


def test_lexicon():
    lx = Lexicon()
    lx.add("John", "P")
    lx.add("Mary", "P")
    lx.add("like", "T")
    r = lx.getAll("P")
    assert 'John' in r and "Mary" in r


def test_fact_base():
    fb = FactBase()
    fb.addUnary("duck", "John")
    fb.addBinary("love", "John", "Mary")
    assert fb.queryUnary("duck", "John")
    assert not fb.queryBinary("love", "Mary", "John")


@pytest.mark.slowtest
def test_stemming_with_tagging():
    failures = []
    for word, stem in word2stem.items():
        if not verb_stem(word) == stem:
            failures.append(word)
    # some words are just not in brown :(
    assert failures == ['fizzes', 'analyses', 'dazes']


def test_tagger():
    assert not verb_stem('cats')


def test_processing():
    lx = Lexicon()
    fb = FactBase()

    sentences = [
        "Mary is a duck.",
        "John is purple.",
        "Mary flies.",

        # Love story
        "John likes Mary.",
        "Mary likes Joshua.",
        "Joshua likes John.",
    ]

    for s in sentences:
        assert process_statement(lx, s.rstrip('.').split(' '), fb) == ''

    assert "Mary" in lx.getAll("P")
    assert "duck" in lx.getAll("N")
    assert "purple" in lx.getAll("A")
    assert "fly" in lx.getAll("I")
    assert "like" in lx.getAll("T")

    assert fb.queryUnary("N_duck", "Mary")
    assert fb.queryUnary("A_purple", "John")
    assert fb.queryUnary("I_fly", "Mary")

    # love triangle:
    assert fb.queryBinary("T_like", "John", "Mary")
    assert not fb.queryBinary("T_like", "Mary", "John")
    assert fb.queryBinary("T_like", "Mary", "Joshua")
    assert fb.queryBinary("T_like", "Joshua", "John")
