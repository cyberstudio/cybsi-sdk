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

Custom entity views
-------------------

You can configure entity view in some Cybsi API methods: :meth:`~cybsi.api.replist.ReplistsAPI.entities` and :meth:`~cybsi.api.replist.ReplistsAPI.changes`.

Specify `entity_view` parameter in API method. Default basic view includes only entity types and natural keys.
You can find builtin views in :mod:`~cybsi.utils.views` or use :meth:`~cybsi.api.observable.view.EntityViewsAPI` to retrieve information about them.

In the example below you can see replist entities in PT Multiscanner view:

.. literalinclude:: ../../examples/register_replist_with_custom_query.py