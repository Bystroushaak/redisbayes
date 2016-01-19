#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
Simple bayess classifier.
"""
#
# Imports =====================================================================
import re
import math
from collections import defaultdict


# Variables ===================================================================
__version__ = "0.1.0"

english_ignore_list = set("""
a able about above abroad according accordingly across actually adj after
afterwards again against ago ahead ain't all allow allows almost alone along
alongside already also although always am amid amidst among amongst an and
another any anybody anyhow anyone anything anyway anyways anywhere apart
appear appreciate appropriate are aren't around as a's aside ask asking
associated at available away awfully b back backward backwards be became
because become becomes becoming been before beforehand begin behind being
believe below beside besides best better between beyond both brief but by c
came can cannot cant can't caption cause causes certain certainly changes
clearly c'mon co co. com come comes concerning consequently consider
considering contain containing contains corresponding could couldn't course
c's currently d dare daren't definitely described despite did didn't different
directly do does doesn't doing done don't down downwards during e each edu eg
eight eighty either else elsewhere end ending enough entirely especially et
etc even ever evermore every everybody everyone everything everywhere ex
exactly example except f fairly far farther few fewer fifth first five
followed following follows for forever former formerly forth forward found
four from further furthermore g get gets getting given gives go goes going
gone got gotten greetings h had hadn't half happens hardly has hasn't have
haven't having he he'd he'll hello help hence her here hereafter hereby herein
here's hereupon hers herself he's hi him himself his hither hopefully how
howbeit however hundred i i'd ie if ignored i'll i'm immediate in inasmuch inc
inc. indeed indicate indicated indicates inner inside insofar instead into
inward is isn't it it'd it'll its it's itself i've j just k keep keeps kept
know known knows l last lately later latter latterly least less lest let let's
like liked likely likewise little look looking looks low lower ltd m made
mainly make makes many may maybe mayn't me mean meantime meanwhile merely
might mightn't mine minus miss more moreover most mostly mr mrs much must
mustn't my myself n name namely nd near nearly necessary need needn't needs
neither never neverf neverless nevertheless new next nine ninety no nobody non
none nonetheless noone no-one nor normally not nothing notwithstanding novel
now nowhere o obviously of off often oh ok okay old on once one ones one's
only onto opposite or other others otherwise ought oughtn't our ours ourselves
out outside over overall own p particular particularly past per perhaps placed
please plus possible presumably probably provided provides q que quite qv r
rather rd re really reasonably recent recently regarding regardless regards
relatively respectively right round s said same saw say saying says second
secondly see seeing seem seemed seeming seems seen self selves sensible sent
serious seriously seven several shall shan't she she'd she'll she's should
shouldn't since six so some somebody someday somehow someone something
sometime sometimes somewhat somewhere soon sorry specified specify specifying
still sub such sup sure t take taken taking tell tends th than thank thanks
thanx that that'll thats that's that've the their theirs them themselves then
thence there thereafter thereby there'd therefore therein there'll there're
theres there's thereupon there've these they they'd they'll they're they've
thing things think third thirty this thorough thoroughly those though three
through throughout thru thus till to together too took toward towards tried
tries truly try trying t's twice two u un under underneath undoing
unfortunately unless unlike unlikely until unto up upon upwards us use used
useful uses using usually v value various versus very via viz vs w want wants
was wasn't way we we'd welcome well we'll went were we're weren't we've what
whatever what'll what's what've when whence whenever where whereafter whereas
whereby wherein where's whereupon wherever whether which whichever while
whilst whither who who'd whoever whole who'll whom whomever who's whose why
will willing wish with within without wonder won't would wouldn't x y yes yet
you you'd you'll your you're yours yourself yourselves you've z zero
successful greatest began including being all for close but
""".split())  #: Default ignore list.


# Functions & classes =========================================================
def tidy(text):
    """
    Convert `text` to unicode. Replace special characters with spaces.

    Args:
        text (str / unicode): Input sentence.

    Returns:
        unicode: Cleaned sentece.
    """
    if not isinstance(text, basestring):
        text = str(text)

    if not isinstance(text, unicode):
        text = text.decode('utf8')

    text = text.lower()

    return re.sub(r'[\_.,<>:;~+|\[\]?`"!@#$%^&*()\s]', ' ', text, re.UNICODE)


def english_tokenizer(text, ignore_list=english_ignore_list):
    """
    Simple english tokenizer used to split input sentence to list of words.

    Words are normalized to lowercase.

    Args:
        text (str/unicode): Input sentence.
        ignore_list (set): Set of words which wouln't be classified. Default
            :attr:`english_ignore_list`.

    Returns:
        list: Strings / words without special characters and separators.
    """
    words = tidy(text).split()

    return [
        word
        for word in words
        if len(word) > 2 and word not in ignore_list
    ]


def occurances(words):
    """
    Count how many times is each word present in input list `words`.

    Args:
        words (list): Tokenized sentence.

    Returns:
        dict: Dictionary ``{"word": int(occurances)}``.
    """
    counts = defaultdict(int)

    for word in words:
        counts[word] += 1

    return counts


class SimpleBayes(object):
    """
    Simple naive bayes classificator, which may be used for spam
    classification.

    Attributes:
        db_backend (obj): Dict-like object used to store values.
        correction (float): Value used as weight for unclassified words.
        tokenizer (ref): Reference to function used for text tokenization.
        sub_dict (ref): Reference to function used for construction of
            sub-dicts.
        _original_keys (set): Set of keys which were in :attr:`db_backend` when
            the constructor was called. This is used to prevent cleaning of
            such keys when the :meth:`reset` is called.
    """
    def __init__(self, db_backend=None, correction=0.1, tokenizer=None,
                 sub_dict=dict):
        """
        Constructor for :class:`SimpleBayes`.

        Args:
            db_backend (dict-like object): Database connector or just plain old
                dict. If ``None``, ``{}`` will be used. Default ``None`.
            correction (float): Value used in classificator in case that the
                word wasn't yet classified. Default ``0.1``.
            tokenizer (func reference): Reference to function used for word
                tokenization. If ``None``, :func:`english_tokenizer` is used.
                Default ``None``.
            sub_dict (func): Function used to construct sub-dictionaries in
                dictionary. Default :func:`dict`.
        """
        self.db_backend = db_backend
        self.correction = correction
        self.tokenizer = tokenizer or english_tokenizer
        self.sub_dict = sub_dict

        if not self.db_backend:
            self.db_backend = {}

        self._original_keys = set(self.db_backend.keys())

    def reset(self):
        """
        Remove trained set from database.
        """
        keys_to_remove = set(self.db_backend.keys()) - self._original_keys

        for cat in keys_to_remove:
            del self.db_backend[cat]

    def train(self, category, text):
        """
        Train bayess classificator to put `text` into `category`.

        Args:
            category (str): Name of the category for `text`.
            text (str): Classified text.
        """
        if category not in self.db_backend:
            self.db_backend[category] = self.sub_dict()

        for word, count in occurances(self.tokenizer(text)).iteritems():
            # defaultdict is not used to allow `self.sub_dict`
            old = self.db_backend[category].get(word, 0)
            self.db_backend[category][word] = old + count

    def untrain(self, category, text):
        """
        Make the classsifier forgot, that `text` belongs to `category`.

        Args:
            category (str): Name of the category into `text` which text was
                classified by mistake.
            text (str): Classified text.
        """
        for word, count in occurances(self.tokenizer(text)).iteritems():
            cur = self.db_backend.get(word)
            if cur:
                new = int(cur) - count
                if new > 0:
                    self.db_backend[category][word] = new
                else:
                    del self.db_backend[category][word]

        if self._tally(category):
            del self.db_backend[category]

    def classify(self, text):
        """
        Let the classificator tell you, where the `text` should belong.

        Args:
            text (str): Sentence for classification.

        Returns:
            str: Name of the category.
        """
        score = self.score(text)
        if not score:
            return None

        return sorted(score.iteritems(), key=lambda (k, v): v)[-1][0]

    def score(self, text):
        """
        Get score of category probability for given `text`.

        Args:
            text (str): Sentence for classification.

        Returns:
            dict: ``{"category": int(probability)}``.
        """
        occurs = occurances(self.tokenizer(text))

        scores = {}
        for category in self.db_backend.keys():
            tally = self._tally(category)
            if tally == 0:
                continue

            scores[category] = 0.0
            for word in occurs.keys():
                score = self.db_backend[category].get(word, self.correction)

                scores[category] += math.log(float(score) / tally)

        return scores

    def _tally(self, category):
        """
        Get sum of weights for all words in given `category`.

        Args:
            category (str): Name of the category learnt by :meth:`train`.

        Returns:
            int: Sum of all values in this category.
        """
        tally = sum(self.db_backend[category].values())

        assert tally >= 0, "corrupt bayesian database"

        return tally
