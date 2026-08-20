---
name: realtime-alert-dispatch
description: Use when a QC check fails during an active LC-MS instrument run and you
  need to immediately notify configured users (via Slack channel or email address)
  of the failure event, including timestamp, check type, and severity metadata.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Slack API
  - Email service
  techniques:
  - LC-MS
  license_tier: open
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

# realtime-alert-dispatch

## Summary

Dispatch realtime notifications (Slack or email) to configured users when QC failures are detected during LC-MS instrument runs. This skill enables rapid alerting so users can respond to data quality issues without manual monitoring.

## When to use

Apply this skill when a QC check fails during an active LC-MS instrument run and you need to immediately notify configured users (via Slack channel or email address) of the failure event, including timestamp, check type, and severity metadata.

## When NOT to use

- QC check passed or no actionable failure occurred — no alert is needed
- No Slack API key or email service credentials are configured in the system
- User has opted out of or disabled notifications for this QC check type

## Inputs

- QC check result with fail status and metadata (timestamp, check type, severity)
- System configuration containing Slack channel IDs or email addresses

## Outputs

- Slack or email notification message sent to configured channel/address
- Dispatch status log entry confirming delivery

## How to apply

Monitor QC check results for fail status during data acquisition. When a failure is detected, parse the QC-fail event to extract alert metadata (timestamp, check type, severity). Retrieve the configured notification targets (Slack channel ID or email address) from system configuration. Construct and dispatch the notification payload via the Slack API or email service to the target channel/address. Log the dispatch status and confirm delivery to complete the alert chain.

## Related tools

- **Slack API** (Send realtime QC-fail notifications to Slack channels)
- **Email service** (Send realtime QC-fail notifications via email)

## Evaluation signals

- Notification message arrives in configured Slack channel within seconds of QC failure detection
- Email notification is received at configured address with correct alert metadata (timestamp, check type, severity)
- Dispatch status log contains entry confirming successful delivery or failure reason
- Notification payload contains expected fields: QC check name, failure reason, timestamp, and severity level
- Delivery confirmation aligns with QC-fail timestamp (no stale or delayed alerts)

## Limitations

- Slack or email service must be configured and credentials must be valid; missing configuration will silently fail or require manual setup
- Network connectivity or service outages may prevent notification delivery; retry logic and fallback mechanisms are not documented
- Email delivery depends on mail server configuration and may be delayed or filtered as spam if sender domain is not authenticated

## Evidence

- [other] Rapid QC-MS sends realtime updates on QC failures through Slack or email notifications to alert users during instrument runs.: "Rapid QC-MS sends realtime updates on QC failures through Slack or email notifications to alert users"
- [other] workflow: 1. Monitor QC check results for fail status detection. 2. Parse QC-fail event and extract alert metadata (timestamp, check type, severity). 3. Retrieve configured notification targets (Slack channel ID or email address) from system configuration. 4. Dispatch notification payload via Slack API or email service to the target channel/address. 5. Log dispatch status and confirm delivery.: "Parse QC-fail event and extract alert metadata (timestamp, check type, severity). Retrieve configured notification targets (Slack channel ID or email address) from system configuration. Dispatch"
- [readme] Realtime updates on QC fails in the form of Slack or email notifications: "Realtime updates on QC fails in the form of Slack or email notifications"
- [other] Slack API and Email service are listed as tools for this workflow: "tools: Slack API, Email service"
