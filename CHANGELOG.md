## [0.6.0] 10-08-2021

### Bug Fixes

* Incorrect GitLab links have been removed

### New Features

* Repository - GitHub CI/CD pipeline with new badges, coverage and code quality reports

### Internal Changes

* Heroku deployment pipeline with environments
* GitHub bots - pre-commit, dependabot, codecov, lgtm

## [0.5.0] 16-06-2021

### Bug Fixes

_None_

### New Features

* API - Improved home endpoint

### Internal Changes

* Codebase is now 100% mypy compliant
* New mypy check in CI/CD lint stage
* More reusable test fixtures
* New shell script for running the application
* docker-compose for local development

## [0.4.0] 09-06-2021

### Bug Fixes

_None_

### New Features

* API - New endpoints for single image access
* Frontend - New icon for both Swagger and ReDoc
* Gitlab - New build passing/failing badge

### Internal Changes

* OpenAPI creation is now done manually
* SwaggerUI and ReDoc endpoints are created along with OpenAPI schema
* Refactor conftest
* New shell scripts mainly for CI/CD

## [0.3.0] 05-06-2021

### Bug Fixes

* LoginManager no longer depends on account username

### New Features

* Database - New Token table
* API - New endpoints for password changes + authentication token sent via email
* Other - Welcome email

### Internal Changes

* New lint stage in CI/CD

## [0.2.0] 28-05-2021

### Bug Fixes

_None_

### New Features

* Database - User management and image encoding/decoding history
* API - Changed some URL parameters to be part of body, added user routers with authentication
* API documentation - Better response schemas and descriptions

### Internal Changes

* 100% test coverage
* Automated deployment via CI/CD

## [0.1.0]

### Bug Fixes

_None_

### New Features

* First version of decoding and decoding
* First API version

### Internal Changes

_None_
