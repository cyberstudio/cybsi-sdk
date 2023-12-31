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


.. _register-generic-observation-async-example:

Register a generic observation asynchronously
---------------------------------------------

This one is the same as above, but for code written in asynchronous style.
It registers multiple observations concurrently.

.. literalinclude:: ../../examples/register_generic_async.py


.. _get-attribute-and-relationship-forecasts:

Get attribute and relationship forecasts
----------------------------------------
Forecasting is getting a metric to assess the confidence of the provided indicators and
keeping it up to date.

In the example below we get IsMalicious attribute forecast of ip-address "8.8.8.8".
Also we get link forecasts of ip-address "8.8.8.8" and forecast of relationship
that has form `ip-address("8.8.8.8") resolves domain-name("test.com")`

.. literalinclude:: ../../examples/get_forecasts.py
