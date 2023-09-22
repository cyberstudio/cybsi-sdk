.. _release-process:

Release Process and Rules
=========================

The SDK version consists of 4 parts: ``{major}.{minor}.{hotfix}{suffix}``.

Major and minor versions of SDK mirror major and minor versions of Threat Analyzer REST API.

Major versions do not preserve backward compatibility. Minor versions and hotfixes preserve backward compatibility.

Hotfix versions of SDK are incremented independently of Threat Analyzer REST API.

Suffixes are used to mark work-in-progress versions of SDK.
For example, SDK with version ``2.8.x`` covers the entire Threat Analyzer API spec ``2.8.0``.
SDK with version ``2.8.xa3`` covers the entire Threat Analyzer API spec ``2.7.0``, but may not cover the entire Threat Analyzer API spec for ``2.8.0``.
