---
name: bead-count-threshold-filtering
description: Use when apply this filter after loading raw .idat files or beta-valued matrices from HumanMethylation450 or EPIC methylation arrays when you need to remove probes with insufficient bead counts that may introduce measurement noise or bias into downstream differential methylation or enrichment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
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

# bead-count-threshold-filtering

## Summary

Remove low-quality probes from methylation array data by filtering out probes with fewer than 3 beads in at least 5% of samples. This quality control step eliminates unreliable measurements before downstream analysis on HumanMethylation450 or EPIC arrays.

## When to use

Apply this filter after loading raw .idat files or beta-valued matrices from HumanMethylation450 or EPIC methylation arrays when you need to remove probes with insufficient bead counts that may introduce measurement noise or bias into downstream differential methylation or enrichment analyses.

## When NOT to use

- Input probes have already been filtered for bead count or quality — applying champ.filter() again risks over-filtering and loss of biological signal.
- Analysis requires probes at the boundaries of technical reliability for hypothesis-driven validation — the threshold may exclude important but marginal probes.
- Bead count data is not available or has been discarded during preprocessing — the filter cannot be applied without this information.

## Inputs

- HumanMethylation450 or EPIC array intensity data (in RGChannelSet or MethylSet format)
- Detection p-value matrix (optional, for sequential filtering context)
- Bead count matrix (automatically generated from .idat files or provided separately)

## Outputs

- Filtered probe matrix with low-bead-count probes removed
- Pre- and post-filter probe count comparison
- Quality control report documenting number of probes retained and removed
- Bead count distribution plots (before and after filtering)

## How to apply

Use ChAMP's champ.filter() function with default parameters, which applies bead-count filtering as the second successive quality control step (after detection p-value filtering). The filter removes any probe where fewer than 3 beads are detected in at least 5% of samples in the dataset. This threshold is based on the Illumina bead array technical design, where probes with fewer than 3 beads per sample are considered unreliable. Execute the filter on the full probe set, then compare pre- and post-filter probe counts and bead count distributions to verify that low-bead probes have been removed and that the majority of probes (expected >95% retention) remain for analysis.

## Related tools

- **ChAMP** (Primary tool providing champ.filter() function for sequential quality control filtering (detection p-value and bead-count thresholds) on methylation array data) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package supporting ChAMP with methylation array annotations and test datasets (HumanMethylation450, EPIC v1/v2)) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative R package for methylation array preprocessing and quality control; offers complementary normalization methods)

## Examples

```
champ.filter(beta = myBeta, pd = myPhenoData, beadcount = myBeadcount)
```

## Evaluation signals

- Post-filter probe count is ≥95% of pre-filter count, confirming that only low-bead probes have been removed
- Bead count distribution after filtering shows no probes with <3 beads in ≥5% of samples across the dataset
- Detection p-value filtering is applied first (as a successive step), confirming correct filter order and dual-threshold logic
- Quality control report explicitly states the number of probes removed due to bead-count threshold and the 5% sample cutoff applied
- Filtered probe matrix dimensions match expected output (samples unchanged, probes reduced by <5%)

## Limitations

- The 3-bead and 5%-of-samples thresholds are hard-coded defaults in champ.filter(); the article does not document whether these parameters can be customized for dataset-specific requirements.
- No guidance provided on how to handle datasets with very low sample counts (<20) where 5% may represent <1 sample, potentially leading to aggressive filtering.
- Bead count data must be available at the time of filtering; if raw .idat files are not accessible, the filter cannot be applied to pre-computed beta matrices.
- The filter assumes technical bead-count noise is independent of biological signal; highly variable biological probes may coincidentally fall below the 3-bead threshold and be incorrectly removed.

## Evidence

- [other] removal of probes with fewer than 3 beads in at least 5% of samples per probe: "removal of probes with fewer than 3 beads in at least 5% of samples per probe."
- [other] champ.filter() applies two successive filtering steps by default: "champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per"
- [other] Verify that probes with fewer than 3 beads in at least 5% of samples have been removed by examining bead count distributions before and after filtering: "Verify that probes with fewer than 3 beads in at least 5% of samples have been removed by examining bead count distributions before and after filtering."
- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [other] The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C): "The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)"
