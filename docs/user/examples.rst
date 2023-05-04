.. _examples:

Examples
========

Enrichment
----------

.. _implement-custom-external-db-example:

Implement an external database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

External databases are useful for entity enrichment. An example of external database is global DNS system.

In the example below we pass IP received from enrichment task to
an imaginary system. The system can magically tell if IP is IoC or not.
We form an observation from results and register the observation in Cybsi API.

The example can be used as a general boilerplate for connectors to external databases.

.. literalinclude:: ../../examples/external_db_lookup_enricher.py

.. _implement-custom-analyzer-example:

Implement an analyzer
~~~~~~~~~~~~~~~~~~~~~
Analyzers perform artifact analysis. Typical analyzers are network traffic analyzers and sandboxes.

In the example below we pass artifact and its content (i.e. bytes)
to an imaginary third-party analyzer. The analyzer can magically tell if file associated with our artifact is malicious or not.
We form a report from results and register the report in Cybsi API.

The example can be used as a general boilerplate for connectors to analyzers.

.. literalinclude:: ../../examples/artifact_analysis_enricher.py


Artifacts
---------

.. _upload-download-artifact-example:

Upload and download an artifact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Artifacts are regular files with additional attributes. An artifact can be analyzed or unpacked by Cybsi.
An artifact can be sent for analysis to analyzer (for example, sandbox).

The example shows how to upload and download artifacts.

.. literalinclude:: ../../examples/upload_download_artifact.py

Data sources
------------

.. _register-data-source-example:

Register custom data source
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Data source describes software or identity who makes observation, describes objects, artifacts or reports.

In the example below we registering our own data source type CIRCL and data source MISP.

.. literalinclude:: ../../examples/register_data_sources.py

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
