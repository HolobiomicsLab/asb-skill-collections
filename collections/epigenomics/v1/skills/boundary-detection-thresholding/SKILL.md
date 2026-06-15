---
name: boundary-detection-thresholding
description: Use when when you have computed per-bin insulation scores from a Hi-C cooler file using cooltools.insulation and need to identify discrete genomic boundaries that separate topological domains.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0440
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3173
  tools:
  - cooltools.insulation
  - cooler
  - pandas
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# boundary-detection-thresholding

## Summary

Automated detection of topologically associating domain (TAD) boundaries from Hi-C insulation scores using statistical thresholding (Li or Otsu methods). This skill converts continuous insulation profiles into discrete boundary annotations for characterizing genome compartmentalization.

## When to use

When you have computed per-bin insulation scores from a Hi-C cooler file using cooltools.insulation and need to identify discrete genomic boundaries that separate topological domains. Use this skill when insulation scores are available as a numeric array with values corresponding to window-specific measures of local domain insulation, and you need boolean boundary annotations for downstream visualization or structural analysis.

## When NOT to use

- Input contact matrix is low-resolution (<10 kb bins) or sparse; insulation scores become unreliable below ~5 kb resolution.
- Hi-C data lacks sufficient sequencing depth or has extreme bias artifacts; thresholding will fail to separate signal from noise.
- Boundaries have already been called by another method and you need only to intersect or validate them; use boundary comparison/overlap tools instead.

## Inputs

- cooler file (.cool or .mcool) containing Hi-C contact matrix and bin table
- window size parameter (integer, in base pairs or as number of bins)
- genomic region coordinates (optional, for subsetting analysis)

## Outputs

- pandas DataFrame with columns: region1, region2, insulation_score (numeric), is_boundary_{window} (boolean)
- BED format file of detected boundaries (chrom, start, end, is_boundary flag)
- insulation score table exportable as TSV or CSV

## How to apply

Apply cooltools.insulation with a specified window size parameter (e.g., 50 kb or 100 kb) to compute insulation scores for each genomic bin. The function simultaneously performs thresholding to detect insulating boundaries using either Li or Otsu automated threshold selection. Li thresholding assumes a bimodal distribution of insulation scores (signal vs. background), while Otsu maximizes between-class variance. The output includes per-bin insulation score values and boolean is_boundary_{window} columns indicating which bins cross the computed threshold. Choose the thresholding method based on your domain's expected boundary prominence: Otsu is more conservative and works well for clear TAD structure, while Li may be more sensitive to subtle boundaries. Validate that output scores fall within expected numeric ranges and boundary annotations are strictly boolean; verify row count matches input bin count.

## Related tools

- **cooltools.insulation** (Core function that computes per-bin insulation scores and applies threshold detection (Li or Otsu) to annotate boundaries) — https://github.com/open2c/cooltools
- **cooler** (File format API for loading and querying high-resolution Hi-C contact matrices and bin metadata) — https://github.com/open2c/cooler
- **pandas** (Data manipulation and export of insulation score tables and boundary annotations as DataFrames and CSV/TSV)

## Examples

```
from cooltools import insulation; import cooler; c = cooler.Cooler('sample.cool'); insulation_table = insulation(c, window_bp=50000); print(insulation_table[['region1', 'region2', 'insulation_score', 'is_boundary_50000']])
```

## Evaluation signals

- Output DataFrame row count equals number of bins in cooler file; no rows are dropped or duplicated.
- Insulation scores are numeric (float) and fall within plausible ranges (typically -1 to +1 or normalized 0 to 1); no NaN or inf values except at edge bins.
- is_boundary_{window} columns contain only boolean (True/False) values; no missing or mixed-type entries.
- Boundary positions are monotonically increasing along the chromosome and occur at bin indices within the valid range [0, num_bins).
- BED format export matches boundary annotations: each True entry in is_boundary_{window} produces one line in BED with correct chrom, start, end coordinates derived from bin table.

## Limitations

- Thresholding performance depends critically on window size choice; window too small (< 10 kb) yields noisy scores, window too large may merge adjacent domains.
- Otsu and Li thresholding assume bimodal insulation score distributions; highly fragmented or continuous landscapes may produce spurious or missed boundaries.
- Method is sensitive to Hi-C data quality, sequencing depth, and normalization; poor-quality or heavily biased libraries produce unreliable insulation profiles and thresholds.
- Boundary detection is local and does not account for higher-order hierarchy; TADs detected at one resolution may not correspond to those at different resolutions.

## Evidence

- [other] Apply cooltools.insulation with a specified window size parameter to compute per-bin insulation scores and detect insulating boundaries using either Li or Otsu thresholding.: "Apply cooltools.insulation with a specified window size parameter to compute per-bin insulation scores and detect insulating boundaries using either Li or Otsu thresholding."
- [other] Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns.: "Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns."
- [other] Cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features.: "Cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features."
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced cooler format readily handles storage of high-resolution datasets"
- [readme] how to extract insulation profiles and call boundaries using insulation profile minima: "how to extract insulation profiles and call boundaries using insulation profile minima"
