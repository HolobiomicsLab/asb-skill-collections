---
name: confidence-score-assignment-and-filtering
description: Use when after matching MRM transitions against a lipid reference database,
  when you have candidate lipid identities for each transition and need to rank them
  by quality and select a single match per transition for export to the labelled lipid-identity
  table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Lipid_MRM_parser.ipynb
  - CLAW-MRM
  techniques:
  - mass-spectrometry
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05039
  all_source_dois:
  - 10.1021/acs.analchem.4c05039
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# confidence-score-assignment-and-filtering

## Summary

Assign quality metrics to transition-lipid matches based on mass accuracy and chromatographic alignment, then filter candidates by quality thresholds to select high-confidence lipid identities. This step ensures only reliable lipid assignments enter downstream analysis.

## When to use

After matching MRM transitions against a lipid reference database, when you have candidate lipid identities for each transition and need to rank them by quality and select a single best match per transition for export to the labelled lipid-identity table.

## When NOT to use

- Input transitions have no candidate matches from the database; filtering will yield an empty result.
- Mass accuracy or retention-time calibration data are missing or unreliable; confidence scores cannot be meaningfully computed.
- The analysis goal is exploratory discovery requiring retention of all candidate matches, not deterministic assignment.

## Inputs

- Parsed MRM transition table with m/z values, retention times, and transition parameters
- Lipid reference database with known m/z, retention times, and lipid identities
- Candidate transition-lipid pairs from the matching algorithm with mass and retention-time alignment metrics

## Outputs

- Labelled lipid-identity table associating each MRM transition with matched lipid name, class, and match confidence score
- Quality-filtered transition-lipid assignments meeting confidence thresholds
- Match confidence metrics for each retained transition

## How to apply

For each transition-lipid pair from the matching step, calculate a confidence score combining mass accuracy (typically within instrument tolerance such as ppm-based error) and chromatographic fit (retention time alignment quality). Apply a quality threshold to filter matches—typically retaining only matches above a minimum confidence percentile or absolute score value. For transitions with multiple passing candidates, select the highest-confidence match. Document the filter criteria (mass tolerance, retention time window, minimum score) in your metadata so results are reproducible and comparable across samples.

## Related tools

- **Lipid_MRM_parser.ipynb** (Python Jupyter notebook that implements parsing, matching, and confidence-scoring workflows for MRM lipid data) — github.com/chopralab/CLAW
- **CLAW-MRM** (Parent lipidomics automation workflow providing standardized data processing pipeline including matching and filtering steps) — github.com/chopralab/CLAW

## Evaluation signals

- Confidence scores are numeric, bounded (e.g., 0–1 or 0–100), and present for all retained matches.
- Filtered transition count is less than or equal to input candidate count; no matches are duplicated or lost.
- Each retained transition is associated with exactly one lipid identity (single best match per transition).
- Mass accuracy of retained matches falls within the declared tolerance window (e.g., ppm cutoff); retention times align within specified window.
- Excluded matches have confidence scores below the declared quality threshold; threshold is documented in output metadata.

## Limitations

- Confidence scoring depends on accurate calibration of mass spectrometer and chromatographic system; poor calibration inflates false-positive matches.
- Filtering is only as good as the lipid reference database; lipids absent from the database cannot be matched, regardless of confidence calculation.
- Retention-time alignment assumes consistent chromatographic conditions across samples; method transfers or column changes may invalidate stored retention-time windows.
- No changelog was found in the repository; version stability and parameter history for confidence thresholds are unclear.

## Evidence

- [other] Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit.: "Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit."
- [other] Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition.: "Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition."
- [other] Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence.: "Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence."
- [other] Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches.: "Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches."
- [intro] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
