---
name: spectral-database-search-and-scoring
description: Use when you have preprocessed mass spectrometry data (peak-picked, baseline-corrected)
  from DI-MS, ASAP-MS, or LDI-MS instruments and need to identify unknown samples
  by comparing their spectral fingerprints against a validated reference database
  of known species or compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  - LDI-MS
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

# spectral-database-search-and-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply database search algorithms to score and classify unknown mass spectrometry samples against reference spectral libraries, enabling automated species authentication. This skill assigns taxonomic or chemical identity to unknowns by matching their MS peaks to curated reference databases.

## When to use

You have preprocessed mass spectrometry data (peak-picked, baseline-corrected) from DI-MS, ASAP-MS, or LDI-MS instruments and need to identify unknown samples by comparing their spectral fingerprints against a validated reference database of known species or compounds. Use this skill when manual peak interpretation is infeasible and automated scoring across multiple reference entries is required.

## When NOT to use

- Raw, unprocessed MS data without peak detection and baseline correction — preprocess first
- When no validated reference database exists for your sample type — build or validate the database separately
- For de novo structure elucidation or fragment annotation — this skill identifies samples, not chemical structures

## Inputs

- preprocessed MS spectral data with peak list (DI-MS, ASAP-MS, or LDI-MS format: mzML, mzXML, or vendor native)
- curated reference spectral database with known species or compound spectra
- ground-truth species labels (for validation)

## Outputs

- species assignments for unknown samples
- database search scores (match confidence metrics)
- ranked candidate species list per unknown
- visual discrimination output (score heatmap, classification plot)
- classification accuracy metrics (when ground truth available)

## How to apply

Load the preprocessed unknown MS spectrum (with automatically identified interested peaks) into RapidMass alongside a curated reference database. Select an appropriate database search algorithm from RapidMass's available scoring methods to compute similarity or matching scores between the unknown and each reference entry. The algorithm scores unknown samples and ranks candidate species by match confidence. Retrieve the top-ranked species assignment(s) and associated confidence metrics. Evaluate the classification accuracy by comparing results against ground-truth labels if available, or validate consistency across multiple unknowns from the same source material.

## Related tools

- **RapidMass** (primary platform integrating database search algorithms, peak scoring, and visual output generation for spectral matching and species authentication) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (direct infusion mass spectrometry data source for database search input)
- **ASAP-MS** (ambient solid analysis probe mass spectrometry data source for database search input)
- **LDI-MS** (laser desorption/ionization mass spectrometry data source compatible with RapidMass database search pipeline)

## Evaluation signals

- Classification accuracy against ground-truth species labels meets or exceeds the validation baseline established on easily confused plant materials
- Unknown samples from the same source material cluster together in the visual discrimination output (heatmap or classification plot)
- Database search scores show clear separation between true-match and non-match candidate entries (e.g., top-ranked hit score substantially higher than competitors)
- Reproducibility: repeated database searches on the same unknown with the same algorithm and reference database produce identical assignments and scores
- Cross-validation: species assignments remain consistent when tested against alternative database search algorithms in RapidMass

## Limitations

- Performance depends on the quality and comprehensiveness of the reference database; underrepresented or poorly characterized species may be misidentified
- Easily confused plant materials with highly similar spectral profiles may produce ambiguous scores requiring manual review or additional analytical methods
- Database search algorithms assume that the unknown sample is represented in the reference library; samples from novel or uncatalogued species will receive low-confidence assignments
- LDI-MS data ingestion is described as an extension capability; validation against DI-MS/ASAP-MS baseline must be performed separately for new instrument types

## Evidence

- [other] Execute database search algorithm(s) to score and classify unknown samples against reference species.: "Execute database search algorithm(s) to score and classify unknown samples against reference species."
- [intro] RapidMass offers several database search algorithms to achieve unknown sample scoring: "RapidMass offers several database search algorithms to achieve unknown sample scoring"
- [other] RapidMass validation on easily confused plant materials produced satisfactory species-discrimination results.: "RapidMass validation on easily confused plant materials produced satisfactory species-discrimination results."
- [other] Evaluate classification accuracy against ground-truth species labels and document satisfactory discrimination outcome.: "Evaluate classification accuracy against ground-truth species labels and document satisfactory discrimination outcome."
- [intro] RapidMass enables direct discrimination of unknown sample species with intuitive visual outputs: "RapidMass enables direct discrimination of unknown sample species with intuitive visual outputs"
- [readme] integrates data pre-processing, analysis, and evaluation, enabling direct discrimination of unknown sample species with intuitive visual outputs: "integrates data pre-processing, analysis, and evaluation, enabling direct discrimination of unknown sample species with intuitive visual outputs"
