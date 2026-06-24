---
name: email-delivery-integration
description: Use when when a QC check fails during an active LC-MS run and configured
  email notification targets exist in the system. Use this skill to ensure that QC
  failures are communicated to stakeholders immediately, complementing Slack-based
  alerts for users who prefer or require email notification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - Email service
  - Slack API
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans:
- '**Realtime updates on QC fails** in the form of Slack or email notifications'
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

# email-delivery-integration

## Summary

Integrate email notification dispatch into a real-time QC monitoring system to alert users of QC failures during LC-MS instrument runs. This skill routes QC-fail events to configured email addresses, capturing alert metadata and confirming delivery.

## When to use

When a QC check fails during an active LC-MS run and configured email notification targets exist in the system. Use this skill to ensure that QC failures are communicated to stakeholders immediately, complementing Slack-based alerts for users who prefer or require email notification.

## When NOT to use

- QC check has passed (no fail event detected); email dispatch is not triggered.
- No email notification targets are configured in the system.
- Email service is unavailable or misconfigured; dispatch will fail and should be retried or escalated to Slack as fallback.

## Inputs

- QC-fail event (timestamp, check type, severity)
- Configured email recipient list from system configuration
- Email service credentials and endpoint

## Outputs

- Email notification message delivered to configured recipient(s)
- Dispatch status log entry (success/failure, timestamp, recipient)
- Delivery confirmation record

## How to apply

On detection of a QC-fail status, parse the QC-fail event to extract alert metadata including timestamp, check type, and severity level. Retrieve the configured email notification targets (recipient addresses) from system configuration. Construct a notification payload containing the extracted metadata and dispatch it via an email service (SMTP or equivalent). Log the dispatch status and confirm delivery by verifying the email service response. This workflow ensures that email alerts are triggered synchronously with QC failure detection and logged for audit and debugging purposes.

## Related tools

- **Email service** (Dispatch notification payload to configured email recipient addresses)
- **Slack API** (Alternative real-time notification channel for QC failures (parallel to email))

## Evaluation signals

- Email message received at all configured recipient addresses within expected latency (e.g., <30 seconds of QC-fail event)
- Email payload contains correct alert metadata (timestamp, check type, severity)
- Dispatch status log records success or failure for each recipient
- Email service response code indicates successful acceptance (e.g., HTTP 200 or SMTP 250)
- Audit trail shows no duplicate notifications for the same QC-fail event

## Limitations

- Email delivery is not instantaneous and may be delayed by email service latency or network conditions; Slack is preferred for time-critical alerts.
- Email address configuration errors or invalid addresses will cause dispatch to fail silently or with retry delays; email targets must be validated during system setup.
- Email service outages or authentication failures will prevent notification delivery; a fallback or manual escalation mechanism is required.

## Evidence

- [other] Monitor QC check results for fail status detection. Parse QC-fail event and extract alert metadata (timestamp, check type, severity).: "Monitor QC check results for fail status detection. Parse QC-fail event and extract alert metadata (timestamp, check type, severity)."
- [other] Retrieve configured notification targets (Slack channel ID or email address) from system configuration. Dispatch notification payload via Slack API or email service to the target channel/address.: "Retrieve configured notification targets (Slack channel ID or email address) from system configuration. Dispatch notification payload via Slack API or email service to the target channel/address."
- [readme] Realtime updates on QC fails in the form of Slack or email notifications: "Realtime updates on QC fails in the form of Slack or email notifications"
- [other] Rapid QC-MS sends realtime updates on QC failures through Slack or email notifications to alert users during instrument runs.: "Rapid QC-MS sends realtime updates on QC failures through Slack or email notifications to alert users during instrument runs."
- [other] Log dispatch status and confirm delivery.: "Log dispatch status and confirm delivery."
