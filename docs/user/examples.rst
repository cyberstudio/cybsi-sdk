.. _examples:

Examples
========

Artifacts
---------

.. _upload-download-artifact-example:

Upload and download an artifact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Artifacts are regular files with additional attributes. An artifact can be analyzed or unpacked by Threat Analyzer.
An artifact can be sent for analysis to analyzer (for example, sandbox).

The example shows how to upload and download artifacts.

Also see :ref:`upload-asynchronous-artifacts-example`.

.. literalinclude:: ../../examples/artifact_uploading_downloading.py

Data sources
------------

.. _register-data-source-example:

Register custom data source
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Data source describes software or identity who makes observation, describes objects, artifacts or reports.

In the example below we registering our own data source type CIRCL and data source MISP.

.. literalinclude:: ../../examples/data_sources_registration.py

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

.. _get-replist-changes-example:

Reputation list changes
-----------------------
Reputation list is a list of observed entities, united by some characteristic
through a stored query, for example: malicious entities, indicator hosts, etc.
Reputation list is dynamic and can change with the appearance of each new fact in the system.

In the example below we get a reputation list changes by specified cursor.

Also see :ref:`register-reputation-list`.

.. literalinclude:: ../../examples/replist_changes_getting.py