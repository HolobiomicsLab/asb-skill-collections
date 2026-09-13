---
name: notification-payload-formatting
description: Use when when a QC check fails during an LC-MS instrument run and you
  need to alert users in real time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Slack API
  - Email service
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_rapid_qc_ms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c00786
  all_source_dois:
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# notification-payload-formatting

## Summary

Format and structure QC-failure event metadata into a notification payload suitable for dispatch via Slack or email. This skill ensures that alert information (timestamp, check type, severity) is correctly extracted, organized, and serialized for delivery to configured notification channels.

## When to use

When a QC check fails during an LC-MS instrument run and you need to alert users in real time. Specifically, when you have detected a QC-fail event and have identified the target notification channel (Slack channel ID or email address) from system configuration, but have not yet formatted the alert metadata into a structure compatible with Slack API or email service requirements.

## When NOT to use

- QC check has passed or no failure is detected — notification is unnecessary
- No configured notification targets exist in system configuration — dispatch would fail
- Notification dispatch mechanism (Slack API or email service) is unavailable or offline — payload formatting alone cannot complete delivery

## Inputs

- QC-fail event object (timestamp, check type, severity)
- Configured notification target (Slack channel ID or email address)
- System configuration file or database

## Outputs

- Slack API payload (JSON format with channel, message, metadata)
- Email payload (subject, body, recipient address)
- Formatted alert notification ready for dispatch

## How to apply

After detecting a QC-fail status, parse the QC-fail event to extract alert metadata including timestamp, check type (e.g., internal standard retention time, m/z, or intensity deviation), and severity level. Retrieve the configured notification targets (Slack channel ID or email address) from system configuration. Structure the extracted metadata into a payload object compatible with the target service: for Slack, serialize to JSON with channel, message text, and metadata fields; for email, format with subject line, body text, and recipient address. Validate payload structure against the target service's API schema before dispatch. The rationale is to ensure consistent, parseable alert information reaches users and to prevent delivery failures due to malformed payloads.

## Related tools

- **Slack API** (Dispatch formatted notification payload to Slack channel for real-time user alert)
- **Email service** (Dispatch formatted notification payload to configured email address for user alert)

## Evaluation signals

- Payload contains all required metadata fields (timestamp, check type, severity) without null or missing values
- Payload structure matches target service schema (valid JSON for Slack; valid email headers and body for email)
- Timestamp is ISO 8601 formatted or matches service-specific time format requirement
- Notification target (Slack channel ID or email address) is correctly populated from system configuration
- Dispatch attempt succeeds (HTTP 2xx response from Slack API or SMTP delivery confirmation) or fails with clear error indicating payload vs. service connectivity issue

## Limitations

- Payload formatting does not verify connectivity to Slack API or email service — valid formatting does not guarantee successful delivery
- System configuration must already contain valid Slack channel IDs or email addresses; malformed or non-existent targets will cause delivery failure
- Email payload formatting assumes availability of an email service integration; Rapid QC-MS does not specify which email provider or SMTP configuration is supported
- Slack payload formatting is compatible with Slack API v1; changes in Slack API schema may require payload structure updates

## Evidence

- [other] Parse QC check results for fail status detection. Parse QC-fail event and extract alert metadata (timestamp, check type, severity).: "Parse QC-fail event and extract alert metadata (timestamp, check type, severity)."
- [other] Retrieve and use configured notification targets from system configuration.: "Retrieve configured notification targets (Slack channel ID or email address) from system configuration."
- [other] Dispatch notification payload via Slack API or email service to the target channel/address.: "Dispatch notification payload via Slack API or email service to the target channel/address."
- [readme] Realtime updates on QC failures via Slack or email notifications are a key feature of Rapid QC-MS.: "Realtime updates on QC fails in the form of Slack or email notifications"
- [readme] Python packages required include Slack API for notification dispatch.: "various Python packages, including: Pandas, SQLAlchemy, Plotly Dash, Bootstrap, Watchdog, Google API, Slack API"
