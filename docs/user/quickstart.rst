.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started
with Cybsi SDK.

First, make sure that:

* Cybsi SDK is :ref:`installed <install>` and up-to date.


Let's get started with some simple examples.


Register a generic observation
------------------------------

.. literalinclude:: ../../examples/register_generic.py

Pagination
----------
You'll often need to work with collections of elements API provides.

Cybsi SDK provides two ways to traverse collections.

The **first** way is pages traversing.
This approach fits for cases when you need to get page's properties i.e. cursor.
For walking by page elements just iterate through the page.

.. literalinclude:: ../../examples/pagination_manual.py

The **second** way is elements traversing. This approach allows you to iterate through
collections without working with pages. To work with collections as with iterator use `chain_pages`.

.. literalinclude:: ../../examples/pagination_chained.py