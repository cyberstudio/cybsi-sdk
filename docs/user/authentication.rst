.. _authentication:

Authentication
==============

This document discusses using of authentication with Threat Analyzer.

API-Key
-------

Threat Analyzer API authentication occurs through API-Key.
The client receives a Bearer Token using the api-key and then authenticates in the Threat Analyzer API using this token.

In the example below we create new user and generate his API-Key.

.. literalinclude:: ../../examples/authentication/user_api_key_generation.py
