---
name: slack-api-integration
description: Use when rapid QC-MS detects a QC failure (e.g., internal standard retention
  time drift, m/z deviation, or intensity anomaly) during an active LC-MS instrument
  run and users have configured Slack as a notification target.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Slack API
  - Email service
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

# Slack API Integration for Realtime QC-Fail Notifications

## Summary

Dispatch realtime alerts to Slack channels when LC-MS quality control checks fail during instrument runs. This skill connects QC failure detection to user notification channels, enabling rapid response to data quality issues without manual monitoring.

## When to use

Apply this skill when Rapid QC-MS detects a QC failure (e.g., internal standard retention time drift, m/z deviation, or intensity anomaly) during an active LC-MS instrument run and users have configured Slack as a notification target. Use when human intervention or awareness is time-critical and asynchronous notification (rather than polling) is preferred.

## When NOT to use

- Slack is not configured as a notification target in the system; fall back to email or other channels.
- Users have disabled realtime notifications and prefer batch or manual log review.
- Slack API credentials are invalid, revoked, or the workspace/channel no longer exists; graceful fallback and logging are required.

## Inputs

- QC check result with fail status (timestamp, check type, severity)
- System configuration containing Slack channel ID and API credentials
- Alert metadata (internal standard m/z, retention time, intensity thresholds)

## Outputs

- Slack message posted to configured channel
- Dispatch log entry (timestamp, status: success/failure, message ID)
- Delivery confirmation or error traceback

## How to apply

Monitor QC check results for fail status during data acquisition. When a fail is detected, extract alert metadata (timestamp, check type, severity level) from the QC event. Retrieve the configured Slack channel ID and webhook endpoint from system configuration. Construct a notification payload with the alert details and dispatch it via the Slack API to the target channel. Log the dispatch status and confirm message delivery. Rationale: realtime push notification ensures users are informed immediately rather than discovering failures after instrument completion, enabling prompt troubleshooting of instrument or sample preparation issues.

## Related tools

- **Slack API** (Sends notification payloads to Slack channels and manages message delivery confirmation)
- **Email service** (Alternative notification channel when Slack is unavailable or not configured)

## Evaluation signals

- Slack message appears in the configured channel within seconds of QC fail detection.
- Message payload contains correct metadata: timestamp of QC check, check type (e.g., 'internal standard intensity'), severity level, and sample/run identifier.
- Dispatch log records successful delivery with Slack message ID; failed dispatches log error reason (network, invalid credentials, channel not found).
- Alert is not duplicated; only one message per unique QC failure event.
- Message formatting is human-readable and includes actionable information (e.g., which sample, which check, remediation hint).

## Limitations

- Requires valid Slack workspace, channel, and API credentials; expired or revoked tokens will silently fail unless error handling is comprehensive.
- Network latency or Slack API rate limits may delay notification delivery by seconds to minutes.
- Slack API changes or deprecation may require code updates; this skill is tightly coupled to Slack's webhook and message API.
- Only tested and deployed in Rapid QC-MS context; generalization to other QC or monitoring systems may require adaptation.
- Alert fatigue: if QC thresholds are too permissive, users may receive excessive Slack notifications, reducing signal-to-noise ratio.

## Evidence

- [intro] Realtime updates on QC fails in the form of Slack or email notifications: "Realtime updates on QC fails in the form of Slack or email notifications"
- [other] Parse QC-fail event and extract alert metadata (timestamp, check type, severity); Retrieve configured notification targets (Slack channel ID or email address); Dispatch notification payload via Slack API: "Parse QC-fail event and extract alert metadata (timestamp, check type, severity). 3. Retrieve configured notification targets (Slack channel ID or email address) from system configuration. 4."
- [readme] Rapid QC-MS provides Automated and user-defined quality control checks during instrument runs: "Automated and user-defined quality control checks during instrument runs"
