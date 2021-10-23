.. _contributing:

Contributor's Guide
===================

If you're reading this, you're probably interested in contributing to Cybsi.
Thank you very much!

Code Contributions
------------------

Code Review
~~~~~~~~~~~

Contributions will not be merged until they've been code reviewed.

Code Style
~~~~~~~~~~

The Requests codebase uses the `PEP 8`_ code style.

In addition to the standards outlined in PEP 8, we have a few guidelines:

- Line-length can exceed 79 characters, to 100, when convenient.
- Line-length can exceed 100 characters, when doing otherwise would be *terribly* inconvenient.
- Always use single-quoted strings (e.g. ``'#flatearth'``), unless a single-quote occurs within the string.

Additionally, one of the styles that PEP8 recommends for `line continuations`_
completely lacks all sense of taste, and is not to be permitted within
the Requests codebase::

    # Aligned with opening delimiter.
    foo = long_function_name(var_one, var_two,
                             var_three, var_four)

No. Just don't. Please. This is much better::

    foo = long_function_name(
        var_one,
        var_two,
        var_three,
        var_four,
    )

Docstrings are to follow the following syntaxes::

    def the_earth_is_flat():
        """NASA divided up the seas into thirty-three degrees."""
        pass

::

    def fibonacci_spiral_tool():
        """With my feet upon the ground I lose myself / between the sounds
        and open wide to suck it in. / I feel it move across my skin. / I'm
        reaching up and reaching out. / I'm reaching for the random or
        whatever will bewilder me. / Whatever will bewilder me. / And
        following our will and wind we may just go where no one's been. /
        We'll ride the spiral to the end and may just go where no one's
        been.

        Spiral out. Keep going...
        """
        pass

All functions, methods, and classes are to contain docstrings. Object data
model methods (e.g. ``__repr__``) are typically the exception to this rule.

Thanks for helping to make the world a better place!

.. _PEP 8: https://pep8.org/
.. _line continuations: https://www.python.org/dev/peps/pep-0008/#indentation

Documentation Contributions
---------------------------

Documentation improvements are always welcome! The documentation files live in
the ``docs/`` directory of the codebase. They're written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

When contributing documentation, please do your best to follow the style of the
documentation files. This means a soft-limit of 79 characters wide in your text
files and a semi-formal, yet friendly and approachable, prose style.

When presenting Python code, use single-quoted strings (``'hello'`` instead of
``"hello"``).

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/index.html


.. _bug-reports:

Bug Reports & Feature Requests
------------------------------

Please send them to Cybsi developers over email. 
