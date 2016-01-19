#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

import simple_bayes
from simple_bayes import english_tokenizer


# Fixtures ====================================================================
@pytest.fixture
def sb():
    return simple_bayes.SimpleBayes()


# Tests =======================================================================
def test_constructor(sb):
    assert sb


def test_filtering(sb):
    sb.reset()

    assert sb.classify('nothing trained yet') is None

    sb.train('good', 'sunshine God love sex lobster sloth')
    sb.train('bad', 'fear death horror government zombie')

    assert sb.classify('sloths are so cute i love them') == 'good'

    assert sb.classify('i am a zombie and love the government') == 'bad'

    assert int(sb.score('i am a zombie and love the government')['bad']) == -7
    assert int(sb.score('i am a zombie and love the government')['good']) == -9

    sb.untrain('good', 'sunshine God love sex lobster sloth')
    sb.untrain('bad', 'fear death horror government zombie')

    assert not sb.score('lolcat')


def test_reset(sb):
    sb.train('good', 'sunshine God love sex lobster sloth')
    sb.train('bad', 'fear death horror government zombie')

    assert sb.classify('nothing trained yet')

    sb.reset()

    assert sb.classify('nothing trained yet') is None


def test_tokenizer():
    # Words are lowercased and unicode is supported:

    assert english_tokenizer("Æther")[0] == u"æther"

    # Common english words and 1-2 character words are ignored:

    assert english_tokenizer("greetings mary a b aa bb") == [u'mary']

    # Some characters are removed:

    assert english_tokenizer("contraction's")[0] == "contraction's"
    assert english_tokenizer("what|is|goth")[0] == "goth"
