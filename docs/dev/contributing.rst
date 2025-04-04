.. _contributing:

Contributor's Guide
===================

If you're reading this, you're probably interested in contributing to Threat Analyzer.
Thank you very much!

Code Contributions
------------------

Contributions will not be merged until they've been reviewed.

Please follow `PEP-20 <https://www.python.org/dev/peps/pep-0020/>`_ if you're in doubt.

Formatting is performed using ``make lint``. There are no compromises.

Documentation Contributions
---------------------------

We publish documentation to ReadTheDocs. ReadTheDocs builds docs using python3.11 (so are we).

The documentation files live in the ``docs/`` directory. Docs are written in
`reStructuredText`_, and use `Sphinx`_ to generate the full suite of
documentation.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org

Documentation tools update
~~~~~~~~~~~~~~~~~~~~~~~~~~

To update documentation tools do:

#. install docs dependencies ``make docs-tools``;
#. update dependencies at ``docs/requirements.in``;
#. use ``make update-docs-dependencies`` to update dependencies.

``make update-docs-dependencies`` packs packages ``docs/requirements.in`` with its transitive
dependencies to ``docs/requirements.txt``.
``docs/requirements.txt`` contains complete list of packages with specific versions used
to reproduce same documentation build environment.

See `ReadTheDocs: Reproducible Builds`_ for details.

.. _`ReadTheDocs: Reproducible Builds`: https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html

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
We bump SDK version on every merge request.

The exceptions are changes not affecting API in any way (tests, small changes to documentation, and similar).

An author of a merge request must to the following:

#. Bump version using :ref:`rules <release-process>`. Use ``make bump-version $NEW_VERSION``.
#. Ensure everything builds nicely (``make lint test build-docs``)

Stable versions are published to PyPI using GitHub release workflow or manually.

To do manually, run this once:

.. code-block:: bash

  $ poetry config repositories (TODO add repository)

And then use the following commands:

.. code-block:: bash

  $ git checkout master && git pull
  $ git tag v1.2.3a4  # See the actual version in pyproject.toml
  $ poetry publish --build -r
  $ git push origin v1.2.3a4

.. _bug-reports:

Bug Reports & Feature Requests
------------------------------

Please create a github issue.
