# Evaluation Strategy

## Direct Checks

- verify that badge endpoint URLs from NLeSC/MAGMa README are accessible (HTTP status 200 or 301/302 redirect)
- verify that each badge endpoint returns a response body containing status/value metadata (robust to badge service format changes)
- verify that retrieved badge statuses are recorded in a structured table with columns: [badge_name, endpoint_url, reported_status, retrieval_timestamp]
- verify table file exists in expected_outputs and format_is CSV or JSON
- verify that at least 5 badge endpoints are queried and tabulated (Travis CI, Coveralls, Landscape.io, Docker Hub, Zenodo as listed in sub-task scope)

## Expert Review

- expert review whether the badge status values accurately reflect the live state of the project (requires manual inspection of live badge endpoints to confirm agent correctly parsed and recorded reported values)
- expert review whether any badge endpoint returned a deprecated or no-longer-maintained service error, and assess whether the README is outdated relative to current project infrastructure
