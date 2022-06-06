.. _advanced:

Advanced Usage
==============

This document covers some of Cybsi SDK more advanced features.

Timeouts and limits
-------------------

You can explicitly configure connect/read/write timeouts and maximum of number connection for CyberClient through the Config data class.

In the example below you can see how it can be used:

.. literalinclude:: ../../examples/client_configurations.py

Embed object URL
----------------

You can configure automatic URL inclusion for all Cybsi objects and references having uuid property.
Object URL is presented if :class:`~cybsi.api.client.Config` embed_object_url parameter is True.

In the example below you can see datasource type common view response with (and without) URL:

.. literalinclude:: ../../examples/data_source_embed_url.py

