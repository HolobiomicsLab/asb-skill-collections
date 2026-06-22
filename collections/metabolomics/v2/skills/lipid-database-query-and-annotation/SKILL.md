---
name: lipid-database-query-and-annotation
description: Use when you have parsed MRM transition data (m/z values, retention times, transition parameters) from mass spectrometry experiments and need to map each detected transition to a known lipid identity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - Lipid_MRM_parser.ipynb
  - CLAW-MRM lipid_database
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  dedup_kept_from: coll_claw_mrm_cq
schema_version: 0.2.0
---

# lipid-database-query-and-annotation

## Summary

Query a lipid reference database and annotate mass spectrometry transitions with lipid identities by matching m/z values, retention times, and transition parameters against known lipid records. This skill standardizes the assignment of chemical identity to detected MRM features, enabling downstream statistical and comparative analysis.

## When to use

You have parsed MRM transition data (m/z values, retention times, transition parameters) from mass spectrometry experiments and need to map each detected transition to a known lipid identity. Apply this skill when you have a curated lipid reference database available and require confident, ranked lipid assignments with quality metrics to filter and prioritize matches before statistical analysis or visualization.

## When NOT to use

- Input transition table has not been parsed or does not contain validated m/z and retention-time values.
- No curated, mass-calibrated lipid reference database is available or has not been validated against your instrument platform.
- Matches have already been assigned by an orthogonal method (e.g., manual review or prior annotation) and you are validating rather than discovering identities.

## Inputs

- Parsed MRM transition table (m/z values, retention times, transition parameters)
- Lipid reference database (mass and chromatographic properties indexed by lipid name and class)
- Mass tolerance threshold (e.g., ppm or Da)
- Retention-time alignment window

## Outputs

- Labeled lipid-identity table (transition ID, matched lipid name, lipid class, match confidence)
- Match quality metrics and confidence scores per transition
- Filtered high-confidence lipid annotation set

## How to apply

Load the parsed MRM transition table containing detected m/z values, retention times, and transition parameters from the parsing step. Apply a matching algorithm that compares each transition against a lipid reference database using mass tolerance and retention-time alignment criteria as selection thresholds. Assign confidence scores or match quality metrics to each transition–lipid pair based on mass accuracy and chromatographic fit. Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition. Generate and export a labeled lipid-identity table associating each MRM transition with its matched lipid name, lipid class, and match confidence score. Manual expert review of borderline or ambiguous matches is recommended to validate the annotation layer before downstream analysis.

## Related tools

- **Lipid_MRM_parser.ipynb** (Upstream Python notebook that parses raw mzML files and generates the parsed MRM transition table consumed by the matching module.) — https://github.com/chopralab/CLAW
- **CLAW-MRM lipid_database** (Curated reference database of lipid masses, retention times, and metadata used to match parsed transitions.) — https://github.com/chopralab/CLAW

## Evaluation signals

- All transitions in the parsed table receive a lipid annotation; no unmapped transitions remain unless explicitly filtered.
- Match confidence scores are within the expected range [0, 1] or comparable scale, with scores ≥ threshold retained and lower-confidence matches excluded or flagged.
- Mass accuracy of matched transitions falls within the specified tolerance window (e.g., ±5 ppm for high-resolution MS).
- Retention-time alignment between observed and database-predicted values is within the specified chromatographic window; outliers are logged or manually reviewed.
- Lipid class distribution in the annotated table is biologically plausible and consistent with prior knowledge of the sample (e.g., enrichment in phospholipids for brain or plasma samples).

## Limitations

- Match quality depends critically on the completeness and accuracy of the reference lipid database; missing or mis-calibrated database records will cause false negatives.
- Mass tolerance and retention-time alignment thresholds must be tuned for the specific instrument platform and column chemistry; overly strict thresholds reduce sensitivity, overly permissive thresholds increase false positives.
- Isomeric lipids (same m/z and similar retention time) cannot be resolved by mass and chromatographic matching alone; additional fragmentation or ion mobility data may be required.
- Manual expert review is recommended for low-confidence or ambiguous matches, but is labor-intensive and does not scale to large cohorts.

## Evidence

- [other] Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches.: "Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches."
- [other] Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit.: "Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit."
- [other] Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition.: "Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition."
- [readme] Uses custom parser to match data with specific lipid classes and extract relevant information.: "Uses custom parser to match data with specific lipid classes and extract relevant information."
- [intro] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
