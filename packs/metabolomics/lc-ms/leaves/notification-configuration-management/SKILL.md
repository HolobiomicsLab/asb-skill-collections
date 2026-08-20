---
name: notification-configuration-management
description: Use when setting up a Rapid QC-MS monitoring job and you need to define WHERE and HOW QC-fail alerts should be sent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Slack API
  - Email service
  techniques:
  - LC-MS
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

# notification-configuration-management

## Summary

Configure and manage realtime alert routing for QC failures in LC-MS instrument runs, directing notifications to Slack channels or email addresses based on user-defined targets. This skill ensures that QC-fail events are dispatched to the correct users with appropriate metadata during active data acquisition.

## When to use

Use this skill when setting up a Rapid QC-MS monitoring job and you need to define WHERE and HOW QC-fail alerts should be sent. Specifically: when you have identified the Slack channel IDs or email addresses where users should receive notifications, and you want to bind those targets to a specific QC job so that failures detected during instrument runs trigger automatic dispatch.

## When NOT to use

- If users do not require realtime alerts and only want post-acquisition QC reporting, skip this skill and use only batch QC result visualization.
- If the LC-MS instrument is offline or not acquiring data, notification configuration is not needed until the next run begins.
- If notification credentials or API keys are not available for Slack or email services, defer this skill until infrastructure is in place.

## Inputs

- QC job configuration (JSON or config file specifying job parameters)
- User-defined notification targets (Slack channel IDs or email addresses)
- System configuration store (database or file containing notification endpoint credentials)
- QC-fail event payload (timestamp, check type, severity metadata)

## Outputs

- Configured notification target registry (mapping job ID to Slack/email endpoints)
- Dispatch log entries (one per notification attempt, including status and timestamp)
- Delivery confirmation records (proof of successful Slack API or email service receipt)

## How to apply

During Rapid QC-MS job initialization, retrieve the configured notification targets (Slack channel ID or email address) from the system configuration store. Map each target to its delivery service (Slack API or email service). When a QC-fail event is detected and alert metadata (timestamp, check type, severity) is extracted, construct a notification payload and dispatch it via the configured service. Log the dispatch status and confirm delivery to ensure the alert reached its destination. The rationale is that centralizing notification target configuration at job setup time decouples alert definition from routing logic, allowing the same QC checks to notify different teams without code changes.

## Related tools

- **Slack API** (Dispatches notification payloads to Slack channels; enables realtime alert delivery to user groups)
- **Email service** (Routes notification payloads to configured email addresses; alternative to Slack for recipients without Slack access)

## Evaluation signals

- Configured notification targets are successfully stored and retrieved from system configuration without errors.
- A test QC-fail event generates a notification payload with correct metadata (timestamp, check type, severity) and is dispatched to the target Slack channel or email address within seconds.
- Dispatch log entries record the outcome (success or failure) for each notification attempt, including the timestamp and target service used.
- Delivery confirmation is received from Slack API or email service and logged; absence of delivery confirmation raises an alert.
- Multiple concurrent QC jobs can each maintain independent notification target configurations without interference or cross-routing.

## Limitations

- Notification configuration is job-specific; users must reconfigure targets for each new QC job. No global default or template inheritance is described in the documentation.
- Realtime notification dispatch depends on continuous network connectivity to Slack or email servers; offline instrument computers or network interruptions will queue or drop notifications.
- Rapid QC-MS has been tested extensively only on Thermo Fisher instruments and acquisition sequences; notification dispatch behavior with non-Thermo vendor formats is not documented and may exhibit bugs.
- The README does not specify retry logic, timeout thresholds, or fallback behavior if a primary notification target becomes unavailable during a run.

## Evidence

- [other] Retrieve configured notification targets (Slack channel ID or email address) from system configuration.: "Retrieve configured notification targets (Slack channel ID or email address) from system configuration."
- [readme] Realtime updates on QC failures via Slack or email notifications: "Realtime updates on QC fails in the form of Slack or email notifications"
- [other] Dispatch notification payload via Slack API or email service to the target channel/address.: "Dispatch notification payload via Slack API or email service to the target channel/address."
- [other] Parse QC-fail event and extract alert metadata (timestamp, check type, severity).: "Parse QC-fail event and extract alert metadata (timestamp, check type, severity)."
- [other] Log dispatch status and confirm delivery.: "Log dispatch status and confirm delivery."
