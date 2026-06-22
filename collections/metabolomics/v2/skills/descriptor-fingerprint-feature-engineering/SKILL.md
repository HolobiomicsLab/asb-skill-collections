---
name: descriptor-fingerprint-feature-engineering
description: Use when use when the workflow requires descriptor-fingerprint-feature-engineering.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - alvaDesc
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
---

# descriptor-fingerprint-feature-engineering

## When to use

Use when the workflow requires descriptor-fingerprint-feature-engineering.
