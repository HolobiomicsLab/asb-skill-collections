---
name: dna-methylation-quality-control
description: Use when immediately after loading raw .idat files or beta-value matrices from HumanMethylation450 or EPIC arrays when you need to exclude probes that fail quality control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0632
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - RnBeads
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

# dna-methylation-quality-control

## Summary

Apply detection p-value and bead count thresholds to remove low-quality probes from Illumina methylation array data (450K or EPIC). This filtering step is essential for downstream analysis, removing probes with insufficient signal reliability before normalization and differential methylation analysis.

## When to use

Apply this skill immediately after loading raw .idat files or beta-value matrices from HumanMethylation450 or EPIC arrays when you need to exclude probes that fail quality control. Specifically, use it when your input dataset contains detection p-values and bead count information and you have not yet performed downstream analyses (normalization, batch correction, or DMR detection).

## When NOT to use

- Input data has already been filtered by another pipeline or tool (detection p-values and bead counts no longer available)
- You are working with single-cell methylation data or non-array-based methods (WGBS, bisulfite sequencing)
- Your analysis explicitly requires retaining low-signal probes for specific methodological reasons

## Inputs

- Raw .idat files from Illumina methylation array (450K or EPIC)
- Beta-value matrix with detection p-values and bead count data
- Sample metadata (phenotype information, batch labels)

## Outputs

- Filtered probe count matrix (probes × samples)
- Quality control report documenting probe removal statistics
- Pre- and post-filter probe count comparison
- Bead count distribution plots

## How to apply

Load the methylation array data using ChAMP data import functions (from .idat files or beta-valued matrix), then apply champ.filter() with default parameters. This function performs two successive filtering steps: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe. Compare pre- and post-filter probe counts and examine bead count distributions to verify filtering efficacy. Document the number of probes retained and removed in a quality control report.

## Related tools

- **ChAMP** (Primary tool for filtering probes via champ.filter() function; provides comprehensive pipeline from data loading through quality control to differential methylation analysis) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Dependency package providing methylation array annotations and test datasets (HumanMethylation450, EPIC) required to run ChAMP filtering) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative package for 450K and EPIC array analysis; offers Functional Normalization and data import methods)
- **RnBeads** (Alternative pipeline for 450K or EPIC array analysis with comparable quality control and filtering capabilities)

## Examples

```
library(ChAMP); champ.filter(beta = your_beta_matrix, pd = your_sample_metadata)
```

## Evaluation signals

- Pre-filter probe count > post-filter probe count (probes successfully removed)
- Number of removed probes with detection p-value > 0.01 matches or exceeds expected frequency in the dataset
- Number of probes removed due to bead count < 3 in ≥5% of samples is documented and reasonable given sample size
- Post-filter probe matrix contains no probes with detection p-value > 0.01 (spot-check random probes)
- Bead count distribution before filtering shows probes below threshold; post-filter distribution shows threshold is respected

## Limitations

- Filtering thresholds (detection p-value > 0.01, bead count < 3 in ≥5% samples) are defaults that may not be optimal for all tissue types or array batches; users may need to adjust based on data characteristics
- Filtering requires that raw detection p-values and bead count data are preserved in the input object; some upstream pipelines may have already discarded this information
- The HumanMethylation450 test dataset contains only 8 samples (4 tumor, 4 control), which may not reflect filtering behavior in larger, more diverse cohorts
- ChAMP development version on GitHub is 'under intensive modification and upgrade'; formally released stable versions are maintained on Bioconductor

## Evidence

- [other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: "champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per"
- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [intro] The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C): "The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)"
- [readme] Note that this is NOT a proper release version ChAMP and under intensive modification and upgrade, the formally released one is on Bioconductor: "Note that this is NOT a proper release version ChAMP and under intensive modification and upgrade, the formally released one is on Bioconductor"
