---
name: dna-methylation-array-data-import
description: Use when you have raw .idat files or beta-valued matrices from Illumina HumanMethylation450 (450K) or EPIC array experiments and need to import them into R for quality control and downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
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

# DNA Methylation Array Data Import

## Summary

Load raw DNA methylation array data (IDAT files or beta-value matrices) from HumanMethylation450 or EPIC arrays into R, verifying correct probe counts before downstream filtering and analysis. This skill ensures data integrity at the entry point of the methylation analysis pipeline.

## When to use

You have raw .idat files or beta-valued matrices from Illumina HumanMethylation450 (450K) or EPIC array experiments and need to import them into R for quality control and downstream analysis. Apply this skill at the very start of a methylation study before any probe filtering, normalization, or statistical testing.

## When NOT to use

- Data has already been loaded and filtered; you are starting mid-pipeline with a processed feature table
- Working with non-Illumina methylation platforms (e.g., whole-genome bisulfite sequencing, enzymatic methyl-seq) — ChAMP is designed specifically for 450K and EPIC beadarray data
- Input is already a normalized or batch-corrected matrix; this skill addresses raw data import, not downstream corrections

## Inputs

- .idat raw intensity files (paired Red and Green channel files per sample)
- Beta-value matrix (numeric matrix with CpG probes as rows, samples as columns)
- Sample metadata or phenotype file (optional but recommended for context)

## Outputs

- ChAMP data object containing loaded probe intensities or beta values
- Pre-filter probe count (485,512 for 450K or 867,531 for EPIC)
- Sample-level quality metrics and import summary

## How to apply

Use ChAMP's champ.load() or champ.import() functions to read data from .idat files or a beta-value matrix. For 450K arrays, verify the pre-filter probe count equals 485,512; for EPIC arrays, verify it equals 867,531. These counts confirm successful loading before quality-based filtering removes low-quality or cross-hybridizing probes. Extract the returned probe count from the output object and compare against the expected reference values for your array type. If counts deviate significantly, check for file corruption, incomplete sample sets, or array type mismatch.

## Related tools

- **ChAMP** (Primary function (champ.load, champ.import) for reading .idat or beta-value data from 450K/EPIC arrays) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Provides CpG-probe manifest annotations and reference probe counts for 450K, EPIC v1, and EPIC v2 arrays) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative package offering functional normalization and complementary data import methods)

## Examples

```
library(ChAMP); myLoad <- champ.load(directory='./idat_files/', arraytype='450K'); print(dim(myLoad$beta))
```

## Evaluation signals

- Pre-filter probe count matches expected value: 485,512 for 450K arrays or 867,531 for EPIC arrays
- Output object structure contains valid probe identifiers, sample names, and methylation intensities or beta values with no missing or NaN values for expected probes
- Reported import summary shows all expected samples loaded with consistent dimensions across replicates
- No error or warning messages related to file corruption, mismatched array types, or incomplete IDAT pairs
- Sample-level quality metrics (e.g., detection p-values, bisulfite conversion efficiency) are available and within expected ranges for the tissue type

## Limitations

- ChAMP probe counts assume unfiltered array definitions; counts may not match if vendor has released updated manifest versions
- IDAT file pairs must be complete and uncorrupted; missing or damaged files will cause import failure without detailed error guidance
- Beta-value import assumes external normalization has already been applied; raw intensity import requires access to corresponding IDAT files for proper preprocessing
- Some simulated or custom DMR datasets (e.g., EPICSimData) may contain fewer simulated DMRs than the theoretical full probe set, affecting reproducibility expectations
- ChAMP version 2.29.1+ supports EPICv2; earlier versions do not — ensure dependency versions are correct for your array type

## Evidence

- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [other] The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied.: "The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied"
- [readme] Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
