---
name: visual-pattern-recognition-in-spectral-data
description: Use when after database search algorithms have scored unknown MS samples
  against reference species, and you need to visually inspect and confirm species
  assignments or identify ambiguous classifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3172
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Visual pattern recognition in spectral data

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use RapidMass's visual interface to recognize and interpret mass spectrometry patterns for species discrimination through intuitive graphical outputs (heatmaps, classification plots) rather than numerical tables alone. This skill bridges computational database scoring with human pattern cognition to validate and interpret unknown sample classifications.

## When to use

After database search algorithms have scored unknown MS samples against reference species, and you need to visually inspect and confirm species assignments or identify ambiguous classifications. Particularly valuable when dealing with easily confused plant materials where numerical scores alone may not reveal the confidence or separability of assignments.

## When NOT to use

- Input data has not yet undergone database search scoring—visual patterns cannot be meaningfully generated without reference-based scoring results.
- Raw, unprocessed mass spectrometry data without automatic peak identification and data pre-processing—visual patterns will be obscured by noise and irrelevant peaks.
- Fully automated high-throughput workflows where human pattern inspection is not part of the validation pipeline and numerical score thresholds suffice for decisions.

## Inputs

- Mass spectrometry data files in DI-MS format
- Mass spectrometry data files in ASAP-MS format
- Pre-processed MS peak intensity tables with automatic peak identification applied
- Database search algorithm output (sample scores against reference species)

## Outputs

- Score heatmap visualization (sample × species scoring matrix)
- Classification plot (visual positioning of unknown samples in reference species space)
- Species assignments with visual confidence indicators
- Pattern interpretation report documenting discrimination outcome

## How to apply

Load pre-processed DI-MS or ASAP-MS data into RapidMass, execute the database search algorithm(s) to generate sample scores, then examine the resulting visual discrimination outputs (score heatmaps showing sample-to-species relationships, classification plots positioning unknowns relative to reference clusters). Use the visual layout to assess clustering tightness, outliers, and borderline cases; cross-reference visual patterns with numeric scores to evaluate classification confidence. The user-friendly interface allows interpretation without programming expertise, making pattern inspection a collaborative validation step before accepting final species assignments.

## Related tools

- **RapidMass** (Primary visualization and pattern recognition platform; integrates data pre-processing, database search scoring, and visual output generation for species discrimination) — github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry data source; one of the supported input formats)
- **ASAP-MS** (Atmospheric solid-analysis probe mass spectrometry data source; one of the supported input formats)

## Evaluation signals

- Classification plots show clear spatial separation between reference species clusters and unambiguous positioning of unknown samples within or near a single species cluster.
- Score heatmaps exhibit high contrast between the assigned species column (bright/high scores) and non-assigned species columns (dim/low scores), indicating confident discrimination.
- Visual patterns are reproducible across multiple database search algorithm runs, demonstrating robust underlying signal in the spectral data.
- Species assignments derived from visual inspection match ground-truth labels with satisfactory accuracy (as validated by task_001's documented outcome).
- Borderline or ambiguous samples (appearing near cluster boundaries or equidistant from multiple species) are visually detectable and flagged for additional investigation rather than silently misclassified.

## Limitations

- Visual pattern recognition is subjective and depends on user expertise; the user-friendly interface reduces barriers but does not eliminate interpretation variance.
- Easily confused plant materials (the primary validation use case) may exhibit overlapping spectral signatures that produce ambiguous visual patterns even after correct database scoring, requiring complementary analytical or taxonomic confirmation.
- No changelog is available in the public repository or article, limiting traceability of changes to the visualization algorithms and pattern-rendering logic over software versions.
- Performance has been validated specifically on plant materials; applicability to other organism classes or complex environmental samples is not documented.

## Evidence

- [intro] enabling direct discrimination of unknown sample species with intuitive visual outputs: "enabling direct discrimination of unknown sample species with intuitive visual outputs"
- [intro] RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise: "RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise"
- [readme] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
- [intro] integrates data pre-processing, analysis, and evaluation: "integrates data pre-processing, analysis, and evaluation"
- [intro] supports data from multiple instruments, including DI-MS and ASAP-MS: "supports data from multiple instruments, including DI-MS and ASAP-MS"
