---
name: genomic-coordinate-conversion
description: Use when you need to map computed per-bin metrics (insulation scores, boundary calls, contact frequencies) back to genomic coordinates for export to BED/GFF format, cross-reference with external annotations, or validate that computed features fall within expected genomic ranges.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3086
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3674
  tools:
  - cooler
  - cooltools
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

# genomic-coordinate-conversion

## Summary

Convert genomic coordinates between reference frames or extract region-specific Hi-C data by mapping bin indices to genomic intervals. This skill is essential when working with cooler files where bin-level analyses (e.g., insulation scores, contact frequencies) must be linked back to genomic positions for visualization, validation, or downstream annotation.

## When to use

You need to map computed per-bin metrics (insulation scores, boundary calls, contact frequencies) back to genomic coordinates for export to BED/GFF format, cross-reference with external annotations, or validate that computed features fall within expected genomic ranges. Specifically, when cooltools.insulation or similar functions return bin-indexed DataFrames that lack explicit chromosome and position columns.

## When NOT to use

- Input metrics are already in genomic coordinate space (chrom, start, end columns present and validated)
- You are working with raw contact matrices and have not yet computed per-bin features
- Coordinate mapping is not required for your downstream analysis (e.g., pure contact frequency correlation studies)

## Inputs

- cooler file (.cool or .mcool) containing Hi-C contact matrix and bin table
- pandas DataFrame with per-bin metrics indexed by bin ID (e.g., from cooltools.insulation output)
- cooler bin table (chrom, start, end, weight, etc.)

## Outputs

- pandas DataFrame with genomic coordinates (chrom, start, end) and annotated metrics (e.g., insulation_score, is_boundary)
- BED-format file for visualization or downstream analysis
- validated coordinate table with numeric value ranges and schema checks

## How to apply

After computing per-bin metrics from a cooler file, extract the bin table (which contains chrom, start, end columns) and merge or join it with your metric output on bin index. The cooler API provides direct access to the bin table via the cooler object's `.bins()` method, which returns a pandas DataFrame indexed by bin ID. Join this bin table with your insulation scores or boundary annotations by index to recover genomic coordinates. Validate the join by checking that row counts match, that all required columns (region1, region2, chrom, start, end) are present, and that coordinate values are numeric and within expected chromosome boundaries. Export the merged result as a BED-format file for downstream visualization or comparison with known domain structures.

## Related tools

- **cooler** (Provides bin table and cooler file I/O; bin table contains chrom, start, end coordinates used to map bin indices to genomic positions) — https://github.com/open2c/cooler
- **cooltools** (Computes per-bin metrics (insulation scores, boundary calls) that must be mapped back to genomic coordinates via the cooler bin table) — https://github.com/open2c/cooltools
- **pandas** (DataFrame join/merge operations to associate bin indices with genomic coordinates and export to tabular formats)

## Examples

```
import cooler; import pandas as pd; c = cooler.Cooler('sample.cool'); bins = c.bins()[:]; insulation = pd.read_csv('insulation_scores.tsv', sep='\t'); merged = insulation.merge(bins[['chrom', 'start', 'end']], left_on='bin1_id', right_index=True); merged.to_csv('insulation_with_coords.bed', sep='\t', index=False, columns=['chrom', 'start', 'end', 'insulation_score', 'is_boundary_10kb'])
```

## Evaluation signals

- Row count of output DataFrame matches input metric DataFrame (no rows lost during join)
- All required columns present: chrom (string), start (int), end (int), insulation_score or equivalent metric (float), is_boundary or annotation field (boolean or categorical)
- Genomic coordinates are monotonically increasing within each chromosome; start < end for all rows
- No NaN or null values in chrom, start, end, or critical metric columns
- BED-format export is valid: tab-separated, chrom field matches reference genome (e.g., 'chr1', 'chr2'), start and end are non-negative integers, and optional name/score fields are present when applicable

## Limitations

- Coordinate conversion depends on the cooler file's bin table being correctly formatted and matching the reference genome; mismatched or corrupted bin tables will produce invalid coordinates
- Bin-to-coordinate mapping is one-to-one; if the cooler file uses variable-width bins or multi-resolution storage, additional logic may be required to select the appropriate resolution
- Export to BED format does not preserve all metrics; if downstream analysis requires multiple numeric fields, use TSV or GFF instead
- The cooler bin table weight column may contain NaN for bad bins; these should be filtered or masked before export for visualization to avoid spurious boundaries

## Evidence

- [other] cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features: "Cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features."
- [other] Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns: "Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns."
- [other] Convert the annotated boundaries to BED format for visualization and downstream analysis: "Convert the annotated boundaries to BED format for visualization and downstream analysis."
- [other] Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*): "Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*)."
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets"
