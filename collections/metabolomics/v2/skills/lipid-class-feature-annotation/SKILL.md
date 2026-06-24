---
name: lipid-class-feature-annotation
description: Use when when loading lipidomics data (from Skyline CSV, numerical matrix,
  or Metabolomics Workbench) and encountering parsing warnings or molecules with names
  that do not follow standard lipid nomenclature patterns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
  - Skyline
  - SummarizedExperiment
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Class and Feature Annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematic annotation and validation of lipid molecule names to ensure they follow supported naming patterns, enabling accurate parsing into lipid class, chain length, and unsaturation features for downstream enrichment analysis. This skill is essential for preparing raw lipidomics data for feature-level biological interpretation.

## When to use

When loading lipidomics data (from Skyline CSV, numerical matrix, or Metabolomics Workbench) and encountering parsing warnings or molecules with names that do not follow standard lipid nomenclature patterns (e.g., non-standard abbreviations, missing chain annotations, or ambiguous formatting). This occurs before quality control and before any statistical analysis, as unparsed molecules cannot be stratified by lipid class or chain properties.

## When NOT to use

- Input data already contains pre-validated, uniformly formatted lipid names following a single supported standard (e.g., all molecules already annotated as PC(32:1), PE(36:2)).
- Analysis goal is solely univariate statistics on raw peak intensities without biological stratification by lipid class or structural features.
- Data has already passed through a validated preprocessing pipeline that guarantees consistent lipid nomenclature.

## Inputs

- LipidomicsExperiment object with unparsed or partially parsed lipid molecule names
- Skyline CSV export or numerical matrix with lipid identifiers in non-standard format
- Sample annotation table with clinical/phenotype metadata

## Outputs

- LipidomicsExperiment object with corrected, uniformly parsed lipid names
- Validated lipid class, chain length, and unsaturation annotations as metadata
- List of removed or renamed molecules and rationale

## How to apply

After loading the LipidomicsExperiment object, examine the parsing warnings generated during data import to identify molecules with unsupported naming patterns. Inspect these molecules using the lipidr data accessor functions, then either remove them from the dataset, rename them to follow supported patterns (lipid class followed by chain length and unsaturation, e.g., PC(32:1)), or retain them as unmapped features. Validate that molecules are correctly parsed by checking that the resulting lipid class, chain length, and unsaturation annotations are consistent with the input nomenclature. Set the logged and normalized status flags appropriately so downstream differential analysis and enrichment functions can operate on the correct feature space.

## Related tools

- **lipidr** (Primary package for loading, parsing, and validating lipid molecule names; provides LipidomicsExperiment object structure and set_logged/set_normalized functions) — https://github.com/ahmohamed/lipidr
- **Skyline** (Data acquisition and export format; lipidr ingests Skyline CSV output and handles molecule name parsing from that format)
- **SummarizedExperiment** (Underlying Bioconductor class that LipidomicsExperiment extends; provides metadata and annotation accessor infrastructure)

## Examples

```
d <- read_skyline('Skyline_export.csv'); d <- add_sample_annotation(d, 'clin.csv'); d <- set_logged(d, 'Area', TRUE); d <- set_normalized(d, 'Area', TRUE)
```

## Evaluation signals

- No parsing warnings or error messages when loading the corrected LipidomicsExperiment object.
- All lipid molecules successfully stratified into lipid classes (e.g., PC, PE, CL, TG) with non-empty counts per class.
- Chain length and unsaturation annotations are numeric, non-missing, and biologically plausible (e.g., chain length 28–40 carbons, unsaturation 0–6 double bonds).
- Downstream lipid set enrichment analysis (lsea) executes without errors and returns enrichment results for recognized lipid classes and chain-length features.
- Removal of unparsed molecules does not eliminate >20% of the total feature space, indicating most molecules were successfully parsed.

## Limitations

- lipidr supports a finite set of lipid nomenclature patterns; non-standard, proprietary, or emerging lipid class abbreviations may not parse correctly.
- Manual renaming of molecules requires expert knowledge of lipid chemistry and nomenclature standards and is labor-intensive for large datasets.
- Removing unparsed molecules without careful review may discard biologically relevant lipid species if the naming convention differs from the supported standard.
- Validation of renamed molecules is manual and error-prone; no automated cross-check against external lipid databases is described in the article.

## Evidence

- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
- [intro] We can examine these molecules, remove them from the dataset or change their names, if desired.: "We can examine these molecules, remove them from the dataset or change their names, if desired."
- [intro] Update and correct molecule names that do not follow supported patterns: "Update and correct molecule names that do not follow supported patterns"
- [intro] Set logged and normalized status for data: "Set logged and normalized status for data"
- [readme] lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages.: "lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages."
- [readme] Lipids can be filtered by their %CV. Normalization methods with and without internal standards are also supported.: "Lipids can be filtered by their %CV. Normalization methods with and without internal standards are also supported."
