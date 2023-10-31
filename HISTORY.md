Release History
===============

2.12.0a1 (2023-10-31)
-------------------
- Add Platforms attribute

2.11.0 (2023-09-30)
-------------------
- Update docs

2.11.0a10 (2023-09-28)
----------------------
- Fix license in pyproject.toml

2.11.0a9 (2023-09-27)
---------------------
- Add async page chaining helper

2.11.0a8 (2023-09-26)
---------------------
- Boost API client authentication
- Add license Apache License 2.0
- Fix documentation

2.11.0a7 (2023-07-31)
---------------------
- Refactor register dictionary item

2.11.0a6 (2023-07-26)
---------------------
- Add related dictionary items api
- Fix register dictionary item

2.11.0a5 (2023-07-18)
---------------------
- Add new PotentialDamage attribute

2.11.0a4 (2023-07-10)
---------------------
- Add dictItemUUID parameter to entity aggregation method

2.11.0a3 (2023-06-19)
---------------------
- Rename Country attribute to RegistrationCountry

2.11.0a2 (2023-06-19)
---------------------
- Increase client default timeout

2.11.0a1 (2023-06-05)
---------------------
- Add new Country attribute

2.10.0 (2023-06-05)
---------------------
- Fix urllib library

2.10.0a9 (2023-05-12)
---------------------
- Fix cybsi-cybsi entity view attribute values

2.10.0a8 (2023-05-04)
---------------------
- Add license API

2.10.0a7 (2023-04-07)
---------------------
- Add multi-value attributes support to Cybsi entity view

2.10.0a6 (2023-03-29)
---------------------
- Add new NodeRoles attribute values

2.10.0a5 (2023-03-13)
---------------------
- Add passwords field in analyzer task parameters

2.10.0a4 (2023-02-20)
---------------------
- Add ExploitedVulnerabilities and TargetedSectors attributes
- Change Sectors attribute value type from enums to dictionary item
- Delete targets and exploits relationship kinds

2.10.0a3 (2023-02-03)
---------------------
- Add cybsi-cybsi entity view

2.10.0a2 (2023-01-27)
---------------------
- Add Campaigns, ThreatActors, AffectedCountries attributes
- Add ASN, Statuses to attribute value convertor func (cherry-pick from release 2.9.1)

2.10.0a1 (2023-01-27)
---------------------
- Add closed dictionary properties

2.9.0 (2023-01-12)
------------------
- Sync SDK with API specification 2.9.0

2.9.0a25(2023-01-10)
--------------------
- Asynchronous artifacts uploading (see advanced.rst)

2.9.0a24(2023-01-09)
--------------------
- Update the underlying HTTP library (httpx)
- Improve type hints

2.9.0a23(2022-12-26)
--------------------
- Extend dictionary item view in attribute values

2.9.0a22(2022-12-15)
--------------------
- Add entities async API (cherry-pick from release 2.8.4)

2.9.0a21(2022-12-09)
--------------------
- Add new NodeRoles attribute values

2.9.0a20(2022-12-08)
--------------------
- Add URL to basic entity view

2.9.0a19(2022-11-30)
--------------------
- Extend NodeRoles attribute values

2.9.0a18(2022-11-23)
--------------------
- PTMS entity view schema update

2.9.0a17(2022-11-23)
--------------------
- Delete scan session

2.9.0a16(2022-11-16)
--------------------
- Add attach and filter report artifacts API

2.9.0a15(2022-11-02)
--------------------
- Remove AVScanStatistic section in observable entity api

2.9.0a14(2022-11-02)
--------------------
- Add ThreatCategory attribute
- Add MalwareName attribute
- Add Enum as allowed attribute value type in generic observation builder.

2.9.0a13(2022-10-24)
--------------------
- Add async replist API

2.9.0a12(2022-10-24)
--------------------
- PTMS entity view example description fixup

2.9.0a11(2022-10-21)
--------------------
- Add PTMS entity view support

2.9.0a10(2022-10-11)
--------------------
- Entity view API route fixup

2.9.0a9(2022-09-22)
-------------------
- Add Entity view API
- Add ability to change entity views for replist entities and changes

2.9.0a8(2022-09-22)
-------------------
- Remove ripeID identity key

2.9.0a7(2022-09-22)
-------------------
- Add new attributes obtained from DNS/Whois

2.9.0a6(2022-09-19)
-------------------
- Add dictionary not found API error

2.9.0a5(2022-09-10)
-------------------
- Remove dictionary item description registration
- Split SynonymConflict error

2.9.0a4(2022-08-31)
-------------------
- Add MF/MC attributes to kebab converter

2.9.0a3(2022-08-10)
-------------------
- Fix dictionary item view initialization

2.9.0a2(2022-08-10)
-------------------
- Expand dictionary API

2.9.0a1(2022-07-22)
-------------------
- Add dictionary API
- Allow registrate fact value of dictionary item
- Remove datasource sorting by uuid

2.8.3(2022-12-09)
-----------------
- Fix enum fact value serialization

2.8.2(2022-07-11)
-----------------
- First stable version of SDK
- Use keyword-only args for public methods

2.8.1a10(2022-06-20)
--------------------
- Add keyword-only args to filters
- Expand filters parameters of API resources for cybsi 2.8.0

2.8.1a9(2022-06-17)
-------------------
- Add managing user profile API

2.8.1a8(2022-06-03)
-------------------
- Add embed object URL setting to global SDK config

2.8.1a7(2022-05-25)
-------------------
- Make some replist API parameters keyword only
- Update stored query validation error codes
- Improve cursor documentation

2.8.1a6(2022-05-13)
-------------------
- Remove unused build dependencies

2.8.1a5(2022-05-13)
-------------------
- Document and improve release process

2.8.1a4(2022-05-12)
-------------------
- Add client timeouts and limits settings

2.8.1a3 (2022-04-29)
--------------------
- Add reports async API
- Add data source async API
- Add enrichment async API
- Add artifacts async API

2.8.1a2 (2022-04-20)
--------------------
- Fix authorization flow bug causing duplicate requests

2.8.1a1 (2022-04-19)
--------------------
**Don't use this version, it has a critical bug, see 2.8.1.a2**

- Implement asynchronous client
- Add async functions for generic observations

2.8.0a10 (2022-04-19)
---------------------
- Fix replist entities + changes API view
- Update API error message with empty suffix

2.8.0a9 (2022-04-12)
--------------------
- Change connector library from requests to httpx

2.8.0a8 (2022-04-08)
--------------------
- Add CybsiAPIEnum class to documentation

2.8.0a7 (2022-04-04)
--------------------
- Add enums: NodeRoles, IdentityClasses, IndustrySectors
- Add enum attribute value conversion

2.8.0a6 (2022-03-29)
--------------------
- Add enum value converter to enum classes

2.8.0a5 (2022-03-28)
--------------------
- Add string to enum converter

2.8.0a4 (2022-03-04)
--------------------
- Restore compatibility with Python 3.7
- Fix link forecast statistics view

2.8.0a3 (2022-02-10)
--------------------
- Add enum of user roles and its permissions
- Add cybsi_data_model/examples sections in documentation

2.8.0a2 (2022-01-27)
--------------------
- Fix artifact view initialization crash

2.8.0a1 (2022-01-21)
--------------------
This is the first version of SDK supporting the entire Cybsi REST API.

As Cybsi 2.8.0 is in development right now, the SDK is released as alpha.

- Add User API
- Simplify installation
- Implement enrichment config rule filter/edit methods
- Implement filter methods for stored queries, external DBs and analyzers
- Implement API key API
- Fix relationship names
- Add annotations API
- Allow adding entity keys
- Extend Report API with `attach_observations` and `filter_observations`
- Implement Replist statistic
- Implement API spec/server version API

0.0.18 (2022-01-11)
-------------------
- Support analyzedArtifactUUID in report API

0.0.17 (2022-01-11)
-------------------
- Extend Artifact common view
- Add Data source filtering API

0.0.16 (2021-12-27)
-------------------
- Add entity/attribute/relationship forecast API
- Add all routes for Observations API
- Add report filtering API
- Use poetry for project building and publishing

0.0.15 (2021-12-22)
-------------------
- Extend ReportForm constructor parameters
- Add entity relationships to generic observations form
- Add Data source API
- Add functions to edit data sources, replists, search queries, analyzers, external databases
- Add Task API
- Add entity registration and aggregation APIs

0.0.14 (2021-12-02)
-------------------
- Add API for external databases
- Add API for stored queries
- Add API for enrichment config rules
- Add API for reports

0.0.13 (2021-11-16)
-------------------
- Describe API errors
- Implement Artifact API

0.0.12 (2021-11-11)
-------------------
- Fix replist route 

0.0.11 (2021-11-11)
-------------------
- Fix URI for API client

0.0.10 (2021-11-10)
-------------------
- Fix serialization token for API client

0.0.9 (2021-11-10)
------------------
- Add text description for errors for client API

0.0.8 (2021-11-08)
------------------
The update contains backward-incompatible changes, the SDK was restructured.

- Implement Task queue API
- Implement part of Artifact API
- Implement part of Report API
- Provide examples of enrichers

0.0.7 (2021-11-08)
------------------
- Fix converter errors

0.0.6 (2021-11-01)
------------------
- Fix converters

0.0.5 (2021-10-19)
------------------
- Add Replist API

0.0.4 (2021-10-14)
------------------
- Add IsDGA attribute

0.0.1 - 0.0.3 (2021-09-10)
--------------------------

- Bootstrap SDK
