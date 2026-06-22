---
name: qc-failure-event-detection
description: Use when rapid QC-MS is actively monitoring LC-MS data acquisition and a QC check result (e.g., internal standard retention time drift, m/z deviation, or intensity threshold breach) returns a fail status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Slack API
  - Email service
  - MS-DIAL
  - Rapid QC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC-failure-event-detection

## Summary

Detect QC check failures during LC-MS instrument runs and trigger realtime alert dispatch. This skill monitors QC result streams from MS-DIAL or equivalent data processing pipelines, identifies fail-status events, and routes failure metadata to configured notification channels (Slack/email) with minimal latency.

## When to use

Apply this skill when Rapid QC-MS is actively monitoring LC-MS data acquisition and a QC check result (e.g., internal standard retention time drift, m/z deviation, or intensity threshold breach) returns a fail status. Trigger occurs during instrument runs when automated quality control checks detect anomalies that require immediate user attention.

## When NOT to use

- QC checks are running in post-acquisition batch mode only (no realtime monitoring active during instrument runs).
- Input is QC pass-status results; this skill only applies to fail-status detection.
- Notification targets (Slack/email) are not configured or credentials are missing — fall back to UI dashboard polling instead.

## Inputs

- QC check result stream (fail-status events from MS-DIAL processed LC-MS data)
- QC check metadata (check type, threshold, severity classification)
- Notification configuration (Slack channel IDs, email addresses, API credentials)
- System timestamp (UTC or instrument-local time)

## Outputs

- Dispatched Slack or email notification payload
- Notification delivery confirmation record
- QC-fail event log entry (timestamp, check type, severity, notification recipient)
- Alert metadata cached for interactive visualization

## How to apply

Monitor QC check result streams for fail-status detection in real time. Parse the QC-fail event to extract alert metadata including timestamp, check type (e.g., retention time, m/z, intensity), and severity level. Retrieve configured notification targets (Slack channel ID or email address) from system configuration or user preferences. Construct and dispatch the notification payload via Slack API or email service to the target channel or address. Log the dispatch status, confirm delivery, and record the alert in the QC results database for audit and historical tracking.

## Related tools

- **Slack API** (Dispatch realtime QC-fail notifications to configured Slack channels)
- **Email service** (Dispatch realtime QC-fail notifications via email to configured recipients)
- **MS-DIAL** (Upstream data processing and QC check execution that produces fail-status events) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Rapid QC-MS** (Orchestrates QC check monitoring, event detection, and notification dispatch) — https://github.com/czbiohub-sf/Rapid-QC-MS

## Evaluation signals

- Notification is delivered to the configured Slack channel or email address within 1–5 seconds of QC-fail event detection.
- Notification payload includes complete and accurate metadata: timestamp, QC check type, threshold, measured value, and severity.
- QC-fail event log entry is created with matching timestamp and metadata; no log gaps or duplicates occur.
- Slack/email delivery confirmation is received and recorded; failed deliveries are flagged in logs.
- Interactive dashboard updates to reflect the failed QC check and alert status; users can view historical alerts.

## Limitations

- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers; other vendor formats may have untested bugs in QC check execution and event detection.
- Realtime notification dispatch depends on network availability and valid Slack/email credentials; failures in external services will delay or prevent alert delivery.
- QC-fail detection is limited to checks defined in the user configuration; custom or ad-hoc checks not in the configuration will not trigger alerts.
- Windows platform is required for full functionality (MSConvert and MS-DIAL dependencies); MacOS users can monitor but may have limited QC processing capabilities.

## Evidence

- [intro] QC check monitoring and fail-status event detection: "Monitor QC check results for fail status detection."
- [intro] Metadata extraction from QC-fail event: "Parse QC-fail event and extract alert metadata (timestamp, check type, severity)."
- [intro] Notification target retrieval and dispatch via Slack API or email service: "Retrieve configured notification targets (Slack channel ID or email address) from system configuration. Dispatch notification payload via Slack API or email service to the target channel/address."
- [readme] Realtime QC-fail notification capability documented in Rapid QC-MS: "Realtime updates on QC fails in the form of Slack or email notifications"
- [readme] Slack API and email service as required Python dependencies: "Slack API and various Python packages, including: Pandas, SQLAlchemy, Plotly Dash, Bootstrap, Watchdog, Google API, Slack API"
