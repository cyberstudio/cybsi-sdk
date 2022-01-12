.. _contributing:

Contributor's Guide
===================

If you're reading this, you're probably interested in contributing to Cybsi.
Thank you very much!

Code Contributions
------------------

Contributions will not be merged until they've been reviewed.

Please follow `PEP-20 <https://www.python.org/dev/peps/pep-0020/>`_ if you're in doubt.

Formatting is performed using ``make lint``. There are no compromises.

Documentation Contributions
---------------------------

The documentation files live in the ``docs/`` directory. Docs are written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/index.html

Developer Environment Setup
---------------------------
Run the following command:

.. code-block:: bash

  $ make tools

This will create a virtualenv with all dependencies installed.

After that you have to `install isort's plugin <https://github.com/pycqa/isort/wiki/isort-Plugins>`_
for your preferred text editor.

Releases
--------
Releases are performed manually.

To perform a release:

#. Update version in ``pyproject.toml``
#. Update version in ``__version__.py``
#. Update ``HISTORY.md``
#. Ensure everything builds nicely (``make lint test build-docs``)

And then run the following commands:

.. code-block:: bash
  $ poetry config (TODO repo name)
  $ poetry publish --build

.. _bug-reports:

Bug Reports & Feature Requests
------------------------------

Please send them to Cybsi developers over email.
