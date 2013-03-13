================
 Hypothesis
================

Hypothesis is a library for falsifying its namesake.

The primary entry point into the library is the hypothesis.falsify method.

What does it do?

You give it a predicate and a specification for how to generate arguments to
that predicate and it gives you a counterexample.

Examples!

.. code:: python

    In [1]: from hypothesis import falsify

    In [2]: falsify(lambda x,y,z: (x + y) + z == x + (y +z), float,float,float)
    Out[2]: (1.0, 1.0, 0.0387906318128606)

    In [3]: falsify(lambda x: sum(x) < 100, [int])
    Out[3]: ([6, 29, 65],)

    In [4]: falsify(lambda x: sum(x) < 100, [int,float])
    Out[4]: ([18.0, 82],)

    In [5]: falsify(lambda x: "a" not in x, str)
    Out[5]: ('a',)

    In [6]: falsify(lambda x: "a" not in x, {str})
    Out[6]: (set(['a']),)

Sometimes we ask it to falsify things that are true:

.. code:: python

    In [7]: falsify(lambda x: x + 1 == 1 + x, int)
    Unfalsifiable: Unable to falsify hypothesis <function <lambda> at 0x2efb1b8>

of course sometimes we ask it to falsify things that are false but hard to find:

.. code:: python

    In [8]: falsify(lambda x: x != "I am the very model of a modern major general", str)
    Unfalsifiable: Unable to falsify hypothesis <function <lambda> at 0x2efb398>

It's not magic, and when the search space is large it won't be able to do very much
for hard to find examples.

How does it work?

Fundamentally it knows how to do two things with types: 

1. Produce them
2. Simplify them

The relevant operations are defined in hypothesis.produce and hypothesis.simplify

A producer is a function, (Producers, int) -> value, while a simplifier is a function
(Simplifiers, value) -> generator(value).

The idea is that the Producers and Simplifiers objects are "context objects" that
know how to map types to things which produce or simplify them. Passing these around
allows you to configure your production and simplification of types in a fairly 
fine grained way.

The specific behaviour requirements are deliberately vague and poorly defined.
Approximately:

* Producers should produce values which are "of about this level of complexity". What that actually means is completely implementation defined. Additionally, it should ideally be possible to produce any value at any size. All that should change is the expected complexity.
* Simplifiers should produce a generator with a finite number of elements, each of which is simpler than the starting element in some completely implementation defined sense.

WARNING: This software should be considered super pre alpha. It probably works
pretty well, maybe, perhaps, but the API is still heavily under flux and the 
internals are liable to change significantly. I'd estimate you currently have 
about an 80% chance of hitting a bug or other rough edge if you were to try and
use it in anger.