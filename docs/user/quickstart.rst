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
The code is written in asynchronous style, but you can use synchronous style if necessary.

.. literalinclude:: ../../examples/generic_registration.py

.. _get-attribute-and-relationship-forecasts:

Get attribute and relationship forecasts
----------------------------------------
Forecasting is getting a metric to assess the confidence of the provided indicators and
keeping it up to date.

In the example below we get IsMalicious attribute forecast of ip-address "8.8.8.8".
Also we get link forecasts of ip-address "8.8.8.8" and forecast of relationship
that has form `ip-address("8.8.8.8") resolves domain-name("test.com")`

.. literalinclude:: ../../examples/forecasts_getting.py

.. _register-reports-example:

Register a report
-----------------
A report is a container that contains a list of observations and artifacts and
general meta-information about them.

In the example below we register reports with other observations and artifacts.
The code is written in asynchronous style, but you can use synchronous style if necessary.

.. literalinclude:: ../../examples/report_registration.py

.. _register-reputation-list:

Register a reputation list
--------------------------
Reputation list is a list of observed entities, united by some characteristic
through a stored query, for example: malicious entities, indicator hosts, etc.
Reputation list is dynamic and can change with the appearance of each new fact in the system.
It is the main mechanism for publishing aggregated information in the system.

In the example below we register stored query `ENT { IsIoC }` to search for observable entities
that are indicators. Based on it, we create a reputation list.

.. literalinclude:: ../../examples/replist_registration.py