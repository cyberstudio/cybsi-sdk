.. _api:

Developer Interface
===================

.. module:: cybsi

This part of the documentation covers all the public interfaces of Cybsi SDK.

Low-level client
----------------

Client interface
~~~~~~~~~~~~~~~~
.. autoclass:: cybsi.api.CybsiClient
    :members:
.. autoclass:: cybsi.api.CybsiAsyncClient
    :members:
.. autoclass:: cybsi.api.VersionView
    :members:
.. autoclass:: cybsi.api.Version
    :members:

Client configuration
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: cybsi.api.Config
    :members:
.. autoclass:: cybsi.api.Limits
.. autoclass:: cybsi.api.Timeouts

Artifacts
~~~~~~~~~
.. automodule:: cybsi.api.artifact
    :members:
    :imported-members:
    :inherited-members:
    :exclude-members: ArtifactTypes, ArtifactContentDownloadCompressionTypes

.. automodule:: cybsi.api.artifact.enums
    :members:
    :show-inheritance:

Auth
~~~~
.. autoclass:: cybsi.api.auth.APIKeyAuth

API-Keys
~~~~~~~~
.. automodule:: cybsi.api.auth.api_key
    :members:
    :inherited-members:
    :exclude-members: APIKeyAuth

Enrichment
~~~~~~~~~~
.. automodule:: cybsi.api.enrichment
    :members:
    :inherited-members:

.. automodule:: cybsi.api.enrichment.api
    :members:
    :inherited-members:

.. automodule:: cybsi.api.enrichment.enums
    :members:
    :show-inheritance:

Configuration
"""""""""""""
.. automodule:: cybsi.api.enrichment.config_rules
    :members:
    :inherited-members:

Tasks
"""""
.. automodule:: cybsi.api.enrichment.tasks
    :members:
    :inherited-members:

Task queue
""""""""""
.. automodule:: cybsi.api.enrichment.task_queue
    :members:
    :inherited-members:

External databases
""""""""""""""""""
.. automodule:: cybsi.api.enrichment.external_dbs
    :members:
    :inherited-members:

Analyzers
"""""""""
.. automodule:: cybsi.api.enrichment.analyzers
    :members:
    :inherited-members:

Observable entities
~~~~~~~~~~~~~~~~~~~
.. automodule:: cybsi.api.observable
    :members:
    :imported-members:
    :inherited-members:
    :exclude-members:  AttributeNames, EntityKeyTypes, EntityTypes, RelationshipKinds, ShareLevels, EntityAggregateSections, ThreatStatus, LinkDirection, NodeRole,IdentityClass,

.. automodule:: cybsi.api.observable.enums
    :members:
    :show-inheritance:

Observations
~~~~~~~~~~~~
.. automodule:: cybsi.api.observation.api
    :members:
    :inherited-members:

Archive
"""""""
.. automodule:: cybsi.api.observation.archive
    :members:
    :inherited-members:

DNS Lookup
""""""""""
.. automodule:: cybsi.api.observation.dns_lookup
    :members:
    :inherited-members:

Generic
"""""""
.. automodule:: cybsi.api.observation.generic
    :members:
    :inherited-members:

Network Session
"""""""""""""""
.. automodule:: cybsi.api.observation.network_session
    :members:
    :inherited-members:

Threat
""""""
.. automodule:: cybsi.api.observation.threat
    :members:
    :inherited-members:

WHOIS Lookup
""""""""""""
.. automodule:: cybsi.api.observation.whois_lookup
    :members:
    :inherited-members:

Common
""""""
.. automodule:: cybsi.api.observation.view
    :members:
    :inherited-members:

.. automodule:: cybsi.api.observation.enums
    :members:
    :inherited-members:
    :show-inheritance:

Data sources
~~~~~~~~~~~~

.. automodule:: cybsi.api.data_source.enums
    :members:
    :show-inheritance:

Types
"""""
.. automodule:: cybsi.api.data_source.api_types
    :members:
    :inherited-members:

Instances
"""""""""
.. automodule:: cybsi.api.data_source.api
    :members:
    :inherited-members:

Search
~~~~~~~~~~~~~~~~
.. automodule:: cybsi.api.search
    :members:
    :imported-members:
    :inherited-members:
    :exclude-members: QueryCompatibility, CybsiLangErrorCodes

.. automodule:: cybsi.api.search.enums
    :members:
    :show-inheritance:

.. automodule:: cybsi.api.search.error
    :members:
    :show-inheritance:

Reputation lists
~~~~~~~~~~~~~~~~
.. automodule:: cybsi.api.replist
    :members:
    :imported-members:
    :inherited-members:
    :exclude-members: EntitySetOperations, ReplistStatus

.. automodule:: cybsi.api.replist.enums
    :members:
    :show-inheritance:

Reports
~~~~~~~
.. automodule:: cybsi.api.report
    :members:
    :imported-members:
    :inherited-members:

Users
~~~~~
.. automodule:: cybsi.api.user
    :members:
    :imported-members:
    :inherited-members:
    :exclude-members: RoleName, ResourceName

.. automodule:: cybsi.api.user.enums
    :members:
    :show-inheritance:

Dictionaries
~~~~~~~~~~~~
.. automodule:: cybsi.api.dictionary
    :members:
    :imported-members:
    :inherited-members:

Licenses
~~~~~~~~
.. automodule:: cybsi.api.license
    :members:
    :imported-members:
    :inherited-members:

Common views and data types
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: cybsi.api.Null
.. autoclass:: cybsi.api.Nullable
.. autoclass:: cybsi.api.NullType
.. autoclass:: cybsi.api.Tag
.. autoclass:: cybsi.api.RefView
    :members:
.. autoclass::  cybsi.api.CybsiAPIEnum
     :members:

Pagination
~~~~~~~~~~
.. automodule:: cybsi.api.pagination
    :members:
    :inherited-members:

Exceptions
----------

.. automodule:: cybsi.api.error
    :members:
    :show-inheritance:

Converters
----------
.. automodule:: cybsi.utils.converters
    :members:

Entity views
------------
.. automodule:: cybsi.utils.views
    :members:

API Changes
-----------

Breaking API changes are documented here. There's no such changes yet.

Licensing
---------

TBD
