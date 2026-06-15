---
name: illumina-450k-epic-dataset-loading
description: Use when you have raw .idat files or a beta-valued matrix from an Illumina HumanMethylation450 or EPIC array experiment and need to import the full probe set into R for downstream quality control, normalization, and differential methylation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3674
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# illumina-450k-epic-dataset-loading

## Summary

Load raw Illumina HumanMethylation450 (450K) and EPIC array data from .idat files or beta-valued matrices into R memory using ChAMP, validating that pre-filter probe counts match expected array manifests (485,512 for 450K; 867,531 for EPIC) before any quality-based filtering.

## When to use

You have raw .idat files or a beta-valued matrix from an Illumina HumanMethylation450 or EPIC array experiment and need to import the full probe set into R for downstream quality control, normalization, and differential methylation analysis. This skill is the entry point for any ChAMP-based methylation array workflow.

## When NOT to use

- Input data has already been filtered to a reduced probe set (e.g., cross-reactive probes removed, SNP-associated probes excluded) — the pre-filter probe count will not match expected values and validation will fail.
- Array type is not HumanMethylation450 or EPIC (e.g., mouse array, custom array) — use ChAMPdata's appropriate manifest instead.
- Data is already in a processed form (e.g., M-values, combat-corrected, ComBat-adjusted) rather than raw intensities or uncorrected beta-values — use appropriate post-hoc import methods instead of champ.load().

## Inputs

- .idat files (paired Grn and Red channel files) from Illumina HumanMethylation450 or EPIC array
- beta-valued matrix with CpG rows and sample columns
- sample sheet or metadata file (CSV/TSV) mapping sample IDs to files

## Outputs

- ChAMP data object (S4 object) containing raw methylation intensities or beta-values
- Pre-filter probe count (485,512 for 450K; 867,531 for EPIC)
- Sample metadata and QC flags attached to the object

## How to apply

Use ChAMP's champ.load() or champ.import() function to ingest .idat files or matrix data, specifying the array type (450K or EPIC). The function automatically loads the corresponding probe manifest from ChAMPdata (which must be ≥2.23.1 for ChAMP ≥2.29.1). Before proceeding to filtering or normalization, inspect the returned object's probe count: it should equal exactly 485,512 for HumanMethylation450 arrays or 867,531 for EPIC arrays if no filtering has yet been applied. If counts deviate, verify that the correct array type was specified and that the .idat files or input matrix correspond to the declared platform. This validation step confirms successful data import and correct manifest loading before quality-based probe filtering.

## Related tools

- **ChAMP** (Primary data loading and import function (champ.load(), champ.import()) for Illumina methylation arrays) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing CpG-probe manifests and array annotations for 450K, EPIC v1, and EPIC v2; required dependency (≥2.23.1) for ChAMP ≥2.29.1) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative Illumina methylation data loading and normalization package; provides Functional Normalization available in ChAMP)

## Examples

```
library(ChAMP); myLoad <- champ.load(directory="./idat_files", method="minfi")
```

## Evaluation signals

- Returned ChAMP object probe count equals exactly 485,512 for HumanMethylation450 input or 867,531 for EPIC input (before any filtering).
- Object contains valid sample metadata and is coercible to matrix form with CpG rows and sample columns.
- No errors or warnings about missing array annotation files; ChAMPdata manifest loaded successfully.
- Reported probe counts in function output match counts extracted from the returned object's internal structure (e.g., nrow(beta_matrix) or equivalent slot).
- Array type can be inferred or verified from object metadata and matches the input .idat file directory structure or user-specified parameter.

## Limitations

- ChAMP requires ChAMPdata ≥2.23.1 for version 2.29.1 and later; version mismatches will cause manifest loading failures.
- Support for EPICv2 arrays is available only in ChAMP ≥2.29.1; earlier versions will not correctly load EPICv2 data.
- Pre-filter probe counts assume raw, unfiltered data; any upstream removal of probes (e.g., low-quality, cross-reactive, SNP-associated) will result in lower counts and validation failure.
- The skill does not validate sample identity, .idat file integrity, or plate/batch metadata; these must be checked separately via quality control plots and metadata inspection.

## Evidence

- [other] The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied.: "The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied."
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] provides a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "provides a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [readme] Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
- [readme] This is the data pacakge supporting the Methylatin Analysis R package ChAMP, which must be installed in your R environment along with ChAMP.: "This is the data pacakge supporting the Methylatin Analysis R package ChAMP, which must be installed in your R environment along with ChAMP."
