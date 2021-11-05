.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started
with Cybsi SDK.

First, make sure that:

* Cybsi SDK is :ref:`installed <install>` and up-to date.


Let's get started with some simple examples.

.. _register-generic-observation-example:

Register a generic observation
------------------------------
Generic observations are universal containers of facts about entities.

In the example below we make an observation about domain "test.com".
The content of the observation says that "test.com" is IoC and malicious with confidence of 0.9.

.. literalinclude:: ../../examples/register_generic.py

.. _implement-custom-external-db-example:

Implement an external database
------------------------------
External databases are useful for entity enrichment. An example of external database is global DNS system.

In the example below we pass IP received from enrichment task to
an imaginary system. The system can magically tell if IP is IoC or not.
We form an observation from results and register the observation in Cybsi API.

The example can be used as a general boilerplate for connectors to external databases.

.. literalinclude:: ../../examples/external_db_lookup_enricher.py

.. _implement-custom-analyzer-example:

Implement an analyzer
---------------------
Analyzers perform artifact analysis. Typical analyzers are network traffic analyzers and sandboxes.

In the example below we pass artifact and its content (i.e. bytes)
to an imaginary third-party analyzer. The analyzer can magically tell if file associated with our artifact is malicious or not.
We form a report from results and register the report in Cybsi API.

The example can be used as a general boilerplate for connectors to analyzers.

.. literalinclude:: ../../examples/artifact_analysis_enricher.py


.. _pagination-example:

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
