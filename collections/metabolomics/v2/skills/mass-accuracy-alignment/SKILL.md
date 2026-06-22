---
name: mass-accuracy-alignment
description: Use when after parsing MRM transition tables (m/z values, retention times, transition parameters) from mzML data, before statistical analysis or visualization. Use this skill when you have detected but unannotated transitions and need to map them to lipid species with quantified confidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Lipid_MRM_parser.ipynb
  - pymzml
  - lipid_database
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-alignment

## Summary

Apply mass tolerance and retention-time alignment criteria to compare detected MRM transitions against a lipid reference database, scoring and filtering matches to assign confident lipid identities. This skill bridges raw mass spectrometry feature detection and annotated lipid identity tables.

## When to use

After parsing MRM transition tables (m/z values, retention times, transition parameters) from mzML data, before statistical analysis or visualization. Use this skill when you have detected but unannotated transitions and need to map them to lipid species with quantified confidence.

## When NOT to use

- Input is already a feature table with lipid identities assigned — skip to statistical analysis.
- MRM transitions have not yet been parsed from raw mzML files — apply data parsing step first.
- Retention time information is unavailable or unreliable — mass-only matching may be necessary instead.

## Inputs

- Parsed MRM transition table (m/z values, retention times, transition parameters)
- Lipid reference database (mass and retention-time annotations)
- Mass tolerance threshold (ppm)
- Retention-time tolerance window

## Outputs

- Labelled lipid-identity table (MRM transition → lipid name, class, match confidence)
- Match quality metrics and confidence scores per transition
- Filtered high-confidence transition-lipid assignments

## How to apply

Load the parsed MRM transition table output from the parsing step. Apply a matching algorithm that compares each transition's m/z value and retention time against a lipid reference database, using pre-defined mass tolerance (typically reported in ppm) and retention-time alignment criteria as dual filters. Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit. Filter matches according to quality thresholds (e.g., minimum confidence score) and select the highest-confidence lipid identity for each transition. Export the result as a labelled lipid-identity table that associates each MRM transition with its matched lipid name, class, and match confidence score. Manual expert review of borderline or ambiguous matches is recommended.

## Related tools

- **Lipid_MRM_parser.ipynb** (Jupyter notebook that executes the matching algorithm after data parsing; compares parsed transitions against lipid database using mass tolerance and RT alignment) — github.com/chopralab/CLAW
- **pymzml** (Python library for reading and parsing mzML files; upstream source of raw transition data)
- **lipid_database** (Reference database of lipid mass, retention-time, and identity annotations used for matching) — github.com/chopralab/CLAW

## Evaluation signals

- All transitions in the input table receive a match assignment (no orphaned transitions).
- Match confidence scores fall within a plausible range (e.g., 0–1 or 0–100%); scores are monotonically related to mass accuracy and RT fit.
- Filtered high-confidence matches show consistency: the same m/z and RT values across samples map to the same lipid identity.
- Manual spot-checks of borderline matches (e.g., confidence near threshold) confirm that mass accuracy and RT alignment are correctly applied.
- Output lipid identities and classes conform to standard nomenclature (e.g., PE 36:2, PC 18:0/18:1) with no obviously malformed names.

## Limitations

- Match quality depends critically on mass tolerance and RT criteria; poorly calibrated instruments or drifting RT may cause mismatches or low confidence scores.
- Isobaric lipids (same m/z, different structure) may not be resolved by mass accuracy and RT alone; additional orthogonal data (MS/MS fragmentation, ion mobility) may be needed.
- Reference database must be comprehensive and up-to-date; missing or incorrect lipid annotations in the database will propagate to unmatched or incorrectly matched transitions.
- No changelog is provided in the repository, so version history and parameter tuning guidance are unclear.

## Evidence

- [other] Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches.: "Apply a matching algorithm to compare each transition against a lipid reference database, using mass tolerance and retention-time alignment criteria to identify candidate lipid matches."
- [other] Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit.: "Assign confidence scores or match quality metrics to each transition-lipid pair based on mass accuracy and chromatographic fit."
- [other] Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition.: "Filter matches according to quality thresholds and select the highest-confidence lipid identity for each transition."
- [other] Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence.: "Generate and export the labelled lipid-identity table associating each MRM transition with its matched lipid name, class, and match confidence."
- [readme] Uses custom parser to match data with specific lipid classes and extract relevant information.: "Uses custom parser to match data with specific lipid classes and extract relevant information."
