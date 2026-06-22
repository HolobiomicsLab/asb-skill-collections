---
name: m-z-database-matching-with-mass-tolerance
description: Use when you have a set of observed m/z values extracted from a Cardinal MSImagingExperiment object, raw LC-MS data, or similar high-throughput MS dataset, and you need to assign them to known metabolites in a reference database (HMDB, Lipidmaps, etc.) with control over mass accuracy tolerance and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - R
  - Cardinal
  - HMDB database
  - Lipidmaps database
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-database-matching-with-mass-tolerance

## Summary

Match observed mass-to-charge (m/z) values from MS imaging or LC-MS experiments against a reference metabolite database using a user-specified parts-per-million (ppm) error tolerance and specified adduct types. This skill enables structural annotation of detected features by resolving which database metabolites plausibly correspond to observed ions.

## When to use

You have a set of observed m/z values extracted from a Cardinal MSImagingExperiment object, raw LC-MS data, or similar high-throughput MS dataset, and you need to assign them to known metabolites in a reference database (HMDB, Lipidmaps, etc.) with control over mass accuracy tolerance and ionization mode (e.g., negative [M-H, M+Cl] or positive adducts). Use this skill when ppm-scale mass measurement precision and adduct multiplicity are critical to reducing false-positive annotations.

## When NOT to use

- Your dataset is already a pre-annotated feature table or peak list; re-matching risks introducing inconsistency or redundant computation.
- You lack a properly formatted reference database or your database does not include accurate monoisotopic masses for your metabolites of interest.
- Your mass measurement accuracy is much poorer than your intended ppm_error tolerance (e.g., if instrument calibration is ±50 ppm but you specify ppm_error=3), leading to systematic under-annotation.

## Inputs

- Observed m/z values (numeric vector or extracted from Cardinal MSImagingExperiment.featureData)
- Reference metabolite database object (HMDB_db, Lipidmaps_db, or similar formatted database)
- Mass tolerance parameter in ppm (numeric scalar, e.g., 3, 5, or 15)
- Adduct specification (character vector, e.g., c('M-H', 'M+Cl') or c('M+H', 'M+Na', 'M+K'))
- Polarity mode (character, 'negative' or 'positive')

## Outputs

- Annotated data.frame with columns: observed_mz, database_match_name, calculated_ppm_error, adduct, and optionally database_mz and metabolite metadata
- Count of successfully matched m/z values (e.g., 67,060 out of 767,528 features)

## How to apply

Extract all m/z feature values from your MS dataset using featureData() or equivalent accessor (e.g., 767,528 features from a Cardinal object). Call the annotation function (AnnotateBigData or AnnotateSM in SpaMTP) with explicit parameters: db=[chosen reference database], ppm_error=[tolerance in ppm, e.g., 3 or 15], adducts=[vector of expected adduct types, e.g., c('M-H', 'M+Cl') for negative mode], and polarity=['negative' or 'positive']. The function returns a data.frame of matches where each observed m/z is paired with database_match_name, observed_mz, calculated_ppm_error, and adduct columns. Validate output by confirming row counts, inspecting ppm_error distributions (all must be ≤ your specified threshold), and spot-checking a subset of assignments against expected metabolites for your biological context.

## Related tools

- **SpaMTP** (R package providing AnnotateBigData and AnnotateSM functions for m/z-to-metabolite annotation with configurable ppm_error and adduct parameters) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Cardinal** (R package for MS imaging data representation and manipulation; provides featureData() accessor to extract m/z values from MSImagingExperiment objects) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **HMDB database** (Reference metabolite database with accurate monoisotopic masses, used as input db parameter for annotation queries)
- **Lipidmaps database** (Reference lipid metabolite database with monoisotopic masses, alternative or complementary to HMDB for lipid-focused annotation)

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = c('M+H', 'M+Na'))
```

## Evaluation signals

- Output data.frame row count equals the expected number of annotated m/z values (e.g., 67,060); unmatched features are either reported separately or absent.
- All calculated_ppm_error values in output are ≤ the specified ppm_error threshold (e.g., all ≤ 3 ppm when ppm_error=3).
- Presence of required columns: observed_mz, database_match_name, calculated_ppm_error, and adduct; no null/NA values in critical columns unless explicitly expected.
- Spot validation: manually check 10–20 high-abundance annotated metabolites to confirm they are plausible for your biological sample (e.g., known lipids in liver tissue).
- Adduct distribution is consistent with expected ionization mode (e.g., predominantly [M-H]⁻ and [M+Cl]⁻ in negative mode; [M+H]⁺, [M+Na]⁺, [M+K]⁺ in positive mode).

## Limitations

- Multiple database matches per m/z are possible if ppm_error tolerance is loose or database entries are clustered; rank matches by ppm_error or apply downstream filtering (e.g., pathway association, colocalization).
- Annotation accuracy depends critically on database completeness and mass accuracy; metabolites absent from the reference database will not be matched regardless of ppm_error stringency.
- Adduct multiplicity increases computational complexity; specifying too many adducts may inflate false-positive matches. The article notes ppm_error filtering and lipid nomenclature refinement (RefineLipids) are required post-annotation steps.
- The manuscript notes two refinement sections ('Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data') are marked 'To come!', suggesting additional validation strategies were planned but not yet implemented.

## Evidence

- [other] Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative': "Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'. 3. Return the annotated results data.frame and verify the row count equals the reported"
- [other] Extract all m/z values from the Cardinal MSImagingExperiment object (767,528 features) using featureData(): "Extract all m/z values from the Cardinal MSImagingExperiment object (767,528 features) using featureData()."
- [other] Inspect the output structure to confirm presence of observed_mz, database_match_name, ppm_error, and adduct columns: "Inspect the output structure to confirm presence of observed_mz, database_match_name, ppm_error, and adduct columns."
- [methods] ppm_error = 15, adducts = 'M+K': "PPM error filtering  [section=methods; evidence='ppm_error = 15, adducts = "M+K"']"
- [readme] m/z metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression and pathway analysis: "this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis"
