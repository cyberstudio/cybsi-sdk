.. _api:

Developer Interface
===================

.. module:: cybsi_sdk

This part of the documentation covers all the interfaces of Cybsi SDK. For
parts where Cybsi SDK depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Authentication
--------------

.. automodule:: cybsi_sdk.auth
    :members:

Low-level client
----------------
.. automodule:: cybsi_sdk.client
    :members:
    :imported-members:

Auth
~~~~
.. automodule:: cybsi_sdk.client.auth
    :members:
    :imported-members:


Enrichment
~~~~~~~~~~
.. automodule:: cybsi_sdk.client.enrichment
    :members:
    :imported-members:


Observable entities
~~~~~~~~~~~~~~~~~~~
.. automodule:: cybsi_sdk.client.observable
    :members:
    :imported-members:

.. autoenum:: cybsi_sdk.enums.AttributeNames
.. autoenum:: cybsi_sdk.enums.EntityTypes
.. autoenum:: cybsi_sdk.enums.EntityKeyTypes
.. autoenum:: cybsi_sdk.enums.RelationshipKinds
.. autoenum:: cybsi_sdk.enums.ShareLevels


Observations
~~~~~~~~~~~~
.. automodule:: cybsi_sdk.client.observations
    :members:
    :imported-members:


Reputation lists
~~~~~~~~~~~~~~~~
.. automodule:: cybsi_sdk.client.replists
    :members:
    :imported-members:

.. autoenum:: cybsi_sdk.enums.ReplistOperations

Reports
~~~~~~~
.. automodule:: cybsi_sdk.client.reports
    :members:
    :imported-members:


Exceptions
----------

.. automodule:: cybsi_sdk.exceptions
    :members:


Converters
----------
.. automodule:: cybsi_sdk.utils.converters
    :members:


API Changes
-----------

Breaking API changes are documented here. There's no such changes yet.

Licensing
---------

TBD
