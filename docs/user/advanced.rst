.. _advanced:

Advanced Usage
==============

This document covers some of Cybsi SDK more advanced features.

Licenses
--------

License - the right to use the software. Such a right is granted by concluding the appropriate License Agreement,
which regulates the scope of rights and restrictions regarding such use.
For the correct installation of the Threat Analyzer obtained under the relevant License Agreement,
the user receives a license key on paper and/or an electronic key.

The example shows how to upload license.

.. literalinclude:: ../../examples/advanced/license_uploading.py

Timeouts and limits
-------------------

You can explicitly configure connect/read/write timeouts and maximum of number connection for CyberClient through the Config data class.

In the example below you can see how it can be used:

.. literalinclude:: ../../examples/advanced/client_configurations.py

Embed object URL
----------------

You can configure automatic URL inclusion for all Threat Analyzer objects and references having uuid property.
Object URL is presented if :class:`~cybsi.api.client.Config` embed_object_url parameter is True.

In the example below you can see datasource type common view response with (and without) URL:

.. literalinclude:: ../../examples/advanced/embed_url_configurations.py

Custom entity views
-------------------

You can configure entity view in some Cybsi API methods: :meth:`~cybsi.api.replist.ReplistsAPI.entities` and :meth:`~cybsi.api.replist.ReplistsAPI.changes`.

Specify `entity_view` parameter in API method. Default basic view includes only entity types and natural keys.
You can find builtin views in :mod:`~cybsi.utils.views` or use :meth:`~cybsi.api.observable.view.EntityViewsAPI` to retrieve information about them.

In the example below you can see replist entities in PT Multiscanner view:

.. literalinclude:: ../../examples/advanced/entity_view_getting.py

.. _upload-asynchronous-artifacts-example:

Asynchronous artifacts uploading
--------------------------------

You can upload artifacts asynchronously using multipart/form-data streams.
For usage pass asyncio/aiohttp `StreamReader` or `AsyncIterator` as argument to :meth:`~cybsi.api.artifact.ArtifactsAsyncAPI.upload`.

In the example below you can see local and remote files uploading:

.. literalinclude:: ../../examples/advanced/artifact_multipart_uploading.py

Enrichment
----------

.. _implement-custom-external-db-example:

Implement an external database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

External databases are useful for entity enrichment. An example of external database is global DNS system.

In the example below we pass IP received from enrichment task to
an imaginary system. The system can magically tell if IP is IoC or not.
We form an observation from results and register the observation in Threat Analyzer API.

The example can be used as a general boilerplate for connectors to external databases.

.. literalinclude:: ../../examples/advanced/enricher_external_db_lookup.py

.. _implement-custom-analyzer-example:

Implement an analyzer
~~~~~~~~~~~~~~~~~~~~~
Analyzers perform artifact analysis. Typical analyzers are network traffic analyzers and sandboxes.

In the example below we pass artifact and its content (i.e. bytes)
to an imaginary third-party analyzer. The analyzer can magically tell if file associated with our artifact is malicious or not.
We form a report from results and register the report in Threat Analyzer API.

The example can be used as a general boilerplate for connectors to analyzers.

.. literalinclude:: ../../examples/advanced/enricher_artifact_analysis.py
