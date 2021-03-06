# coding=utf-8

# Copyright (C) 2013-2015 David R. MacIver (david@drmaciver.com)

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# END HEADER

from __future__ import division, print_function, absolute_import, \
    unicode_literals

from hypothesis.searchstrategy import strategy
from hypothesis.internal.verifier import Verifier
from hypothesis.searchstrategy.narytree import Leaf, Branch, NAryTree


def smallest_tree(predicate):
    d = NAryTree(int, int, int)
    strat = strategy(d)
    v = Verifier()
    return strat.reify(v.falsify(lambda t: not predicate(t), d)[0])


def test_tree_minimizes_to_leaf_with_minimal_value():
    assert smallest_tree(lambda t: True) == Leaf(0)


def test_tree_minimizes_number_of_branch_children():
    assert smallest_tree(lambda t: isinstance(t, Branch)) == Branch(
        0, ()
    )


def test_tree_minimizes_individual_branch_children():
    assert smallest_tree(
        lambda t: len(getattr(t, 'keyed_children', ())) > 1) == Branch(
            0, ((0, Leaf(0)), (0, Leaf(0)))
    )
