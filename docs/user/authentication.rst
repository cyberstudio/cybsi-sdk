.. _authentication:

Authentication
==============

This document discusses using of authentication with Cybsi.

API-Key
-------

Cybsi API authentication occurs through API-Key.
The client receives a Bearer Token using the api-key and then authenticates in the Cybsi API using this token.

In the example below we create new user and generate his API-Key.

.. literalinclude:: ../../examples/generate_user_api_key.py


Licenses
--------

License - the right to use the software. Such a right is granted by concluding the appropriate License Agreement,
which regulates the scope of rights and restrictions regarding such use.
For the correct installation of the Cybsi obtained under the relevant License Agreement,
the user receives a license key on paper and/or an electronic key.

The example shows how to upload license.

.. literalinclude:: ../../examples/upload_license.py