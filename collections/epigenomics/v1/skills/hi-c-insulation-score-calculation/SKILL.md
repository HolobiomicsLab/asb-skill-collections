---
name: hi-c-insulation-score-calculation
description: Use when you have a cooler-format Hi-C contact matrix and need to identify TAD boundaries and insulation strength along the genome. Use this skill when your research question requires quantifying local chromatin compartmentalization or annotating structural domain edges for downstream analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3465
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0080
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

# hi-c-insulation-score-calculation

## Summary

Compute per-bin insulation scores and detect topologically associating domain (TAD) boundaries from high-resolution Hi-C cooler files using cooltools.insulation with a specified window size parameter. This quantitative measure identifies genomic regions of local sequence isolation based on contact frequency asymmetry.

## When to use

You have a cooler-format Hi-C contact matrix and need to identify TAD boundaries and insulation strength along the genome. Use this skill when your research question requires quantifying local chromatin compartmentalization or annotating structural domain edges for downstream analysis (e.g., correlation with epigenetic marks, structural variant detection, or 3D model parameterization).

## When NOT to use

- Input contact matrix is sparse, low-resolution (>100 kb bins), or lacks sufficient read depth; insulation scores become unreliable when bin-pair contact counts are near zero.
- You need to preserve raw contact values unchanged; insulation score computation requires access to off-diagonal contact patterns and may require preliminary normalization or filtering of bad bins.
- Your Hi-C data are already annotated with validated TAD calls from orthogonal methods (e.g., directionality index, chromatin immunoprecipitation); recomputing insulation scores may introduce inconsistent boundary definitions.

## Inputs

- cooler file (.cool or .mcool format) containing normalized Hi-C contact matrix
- window size parameter (numeric; typical range 2–10 Mb depending on resolution and biology)

## Outputs

- pandas DataFrame with columns: region1, region2, insulation_score (numeric), is_boundary_{window} (boolean)
- BED-format file of called TAD boundaries with genomic coordinates

## How to apply

Load a cooler file using the cooler Python API, then apply cooltools.insulation with a window size parameter (e.g., 2–10 Mb) to compute per-bin insulation scores measuring contact asymmetry across diagonal bands. The function outputs a pandas DataFrame with bin coordinates and numeric insulation_score values. Apply either Li or Otsu thresholding to convert scores into boolean boundary annotations (is_boundary_* columns). Validate that output scores fall within expected numeric ranges (typically 0–1 or unbounded depending on normalization) and that boundary flags are strictly boolean. Convert the annotated boundaries to BED format for integration with external visualization and genomic feature annotation tools.

## Related tools

- **cooltools.insulation** (Primary function for computing per-bin insulation scores and boundary annotation from cooler-format Hi-C matrices) — https://github.com/open2c/cooltools
- **cooler** (File format and Python API for storing and accessing high-resolution Hi-C contact matrices with bin metadata) — https://github.com/open2c/cooler
- **pandas** (DataFrame construction, manipulation, and export of insulation score tables and boundary annotations)

## Examples

```
from cooltools.insulation import insulation; import cooler; c = cooler.Cooler('path/to/file.cool'); insulation_table = insulation(c, window_bp=1_000_000, threshold_percentile=None); insulation_table.to_csv('insulation_scores.tsv', sep='\t')
```

## Evaluation signals

- Output file exists, contains expected row count matching number of genomic bins, and displays no null values in required columns (region1, region2, insulation_score, is_boundary_*).
- Insulation scores are numeric (float or int) and fall within biologically plausible ranges; verify no NaN or infinite values except at chromosome boundaries or filtered bins.
- Boolean boundary columns (is_boundary_*) contain only True/False values with no mixed types; verify that at least one boundary is called per chromosome (not degenerate to all True or all False).
- BED-format output contains valid genomic coordinates (chrom, start, end) in ascending order with no overlapping or out-of-bounds intervals.
- Insulation scores show expected spatial autocorrelation: adjacent bins have similar scores, and score minima co-localize with detected boundaries.

## Limitations

- Insulation score reliability depends on adequate contact coverage per bin; low-coverage regions or sparse Hi-C experiments yield unstable boundary calls.
- Window size is a critical hyperparameter; smaller windows detect fine-scale boundaries but are noise-prone, while larger windows smooth over local domain structure and may miss nested TADs.
- Li and Otsu thresholding are heuristic; neither is universal across cell types or species—practitioners must validate boundaries against orthogonal data (ChIP-seq, RNA-seq, ATAC-seq) or visual inspection.
- Insulation scores computed on raw (unnormalized) contact matrices are biased by sequencing depth and bin-wise biases; pre-processing with ICE, Knight–Ruiz, or other normalization is recommended but not enforced by the function.

## Evidence

- [other] Apply cooltools.insulation with a specified window size parameter to compute per-bin insulation scores and detect insulating boundaries using either Li or Otsu thresholding.: "Apply cooltools.insulation with a specified window size parameter to compute per-bin insulation scores and detect insulating boundaries using either Li or Otsu thresholding."
- [other] Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns.: "Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns."
- [other] Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*).: "Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*)."
- [readme] how to extract insulation profiles and call boundaries using insulation profile minima: "how to extract insulation profiles and call boundaries using insulation profile minima."
- [other] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced cooler format readily handles storage of high-resolution datasets"
