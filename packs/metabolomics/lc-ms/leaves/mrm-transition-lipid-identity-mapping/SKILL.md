---
name: mrm-transition-lipid-identity-mapping
description: Use when after parsing raw MRM data into a transition table containing
  m/z values, retention times, and transition parameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - CLAW-MRM
  - Lipid_MRM_parser.ipynb
  - pymzml
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# mrm-transition-lipid-identity-mapping

## Summary

Maps parsed MRM (Multiple Reaction Monitoring) transitions to lipid identities by comparing detected m/z values and retention times against a lipid reference database, assigning confidence scores, and filtering matches to produce a labeled lipid-identity table. This skill bridges raw mass spectrometry data to standardized lipid nomenclature and annotation.

## When to use

Apply this skill after parsing raw MRM data into a transition table containing m/z values, retention times, and transition parameters. Use it when you need to convert unidentified mass spectrometry transitions into named lipid identities with confidence metrics for downstream statistical or visualization analysis.

## When NOT to use

- Input data is already a labeled lipid feature table with identities pre-assigned.
- Reference lipid database is absent, incomplete, or incompatible with your lipid classes of interest.
- Retention time information is unavailable or unreliable (e.g., from different chromatographic platforms with no alignment reference).

## Inputs

- Parsed MRM transition table (m/z values, retention times, transition parameters)
- Lipid reference database (with lipid names, classes, theoretical m/z values)
- Mass tolerance parameter (ppm or Da)
- Retention time alignment tolerance (seconds or minutes)

## Outputs

- Labeled lipid-identity table (transition ID → lipid name, class, match confidence)
- Match quality metrics (mass accuracy, chromatographic fit scores)
- Filtered high-confidence transition-lipid assignments

## How to apply

Load the parsed MRM transition table (output from the data parsing step) and apply a matching algorithm that compares each transition's m/z and retention time against a lipid reference database using mass tolerance and retention-time alignment criteria. Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit. Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition. Generate and export the labeled lipid-identity table that associates each MRM transition with its matched lipid name, class, and match confidence score. Manual expert review of ambiguous or low-confidence matches is recommended to ensure biological validity.

## Related tools

- **CLAW-MRM** (Implements the complete matching workflow including transition parsing, reference database comparison, confidence scoring, and labeled output generation.) — github.com/chopralab/CLAW
- **Lipid_MRM_parser.ipynb** (Jupyter notebook that executes the parsing and matching pipeline on lipid data from mzML files.) — github.com/chopralab/CLAW
- **pymzml** (Python library for reading and processing mzML mass spectrometry data files.)

## Evaluation signals

- All transitions in the output table have exactly one assigned lipid identity (no orphaned or multiply-matched transitions).
- Match confidence scores are within expected range (e.g., 0–1 or 0–100%) and correlate with mass accuracy and chromatographic alignment quality.
- Mass error for matched transitions is within specified tolerance (e.g., <5 ppm for high-resolution MS).
- Retention time differences between observed and database lipid standards are within specified alignment window.
- Spot-check of a random subset of assignments against independent lipid standards or expert knowledge confirms biological plausibility.

## Limitations

- Matching accuracy depends critically on reference database completeness and currency; lipids absent from or mislabeled in the database will not be identified.
- Isomeric or isobaric lipids sharing similar m/z and retention times may be ambiguous; confidence scores alone may not resolve them without additional orthogonal data (e.g., MS/MS fragmentation).
- Retention time alignment assumes chromatographic consistency; variation between analytical runs or instrument configurations can degrade matching performance.
- No changelog or version control information found in the CLAW repository, limiting reproducibility tracking across workflow updates.

## Evidence

- [other] CLAW-MRM includes a matching step as part of its workflow that processes data following the initial parsing phase, enabling standardized lipid data analysis.: "CLAW-MRM includes a matching step as part of its workflow that processes data following the initial parsing phase, enabling standardized lipid data analysis."
- [other] Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches.: "Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches."
- [other] Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit.: "Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit."
- [other] Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence.: "Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence."
- [readme] Uses custom parser to match data with specific lipid classes and extract relevant information.: "Uses custom parser to match data with specific lipid classes and extract relevant information."
