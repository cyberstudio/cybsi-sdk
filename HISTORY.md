Release History
===============

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
