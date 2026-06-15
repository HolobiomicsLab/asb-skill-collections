---
name: bed-format-generation-from-dataframe
description: Use when you have extracted quantitative genomic features (e.g., insulation scores, boundary annotations) as a pandas DataFrame with bin coordinates and boolean or numeric columns, and need to export them as BED format for visualization in genome browsers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3168
  - http://edamontology.org/topic_0622
  tools:
  - pandas
  - cooler
  - cooltools.insulation
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

# BED-format generation from dataframe

## Summary

Convert a pandas DataFrame containing genomic coordinates and annotations (such as insulation scores and boundary calls from Hi-C analysis) into BED format for downstream visualization and analysis. This skill bridges computational feature extraction and standard genome browser interchange.

## When to use

You have extracted quantitative genomic features (e.g., insulation scores, boundary annotations) as a pandas DataFrame with bin coordinates and boolean or numeric columns, and need to export them as BED format for visualization in genome browsers (e.g., IGV, UCSC) or for intersection with other genomic interval datasets.

## When NOT to use

- Input data is not a pandas DataFrame or does not contain coordinate columns (chrom, start, end).
- Feature columns are already in a compressed or binary format (e.g., HDF5, bigBed) — convert back to text-based BED only if re-annotation is needed.
- Coordinates are already 1-based (use conversion or validation to confirm 0-based half-open convention before writing).

## Inputs

- pandas DataFrame with bin coordinates (chrom, chromStart, chromEnd columns)
- Feature columns (e.g., is_boundary_*, insulation_score, numeric or boolean annotations)

## Outputs

- BED-format text file (.bed) with tab-delimited columns: chrom, chromStart, chromEnd, [name], [score], [strand]
- Validated BED file suitable for genome browser visualization and downstream analysis

## How to apply

Start with a pandas DataFrame containing at minimum three columns: region/bin start coordinate, region/bin end coordinate, and a feature column (e.g., boolean is_boundary flag or numeric insulation score). Select or rename columns to align with BED format requirements (chrom, chromStart, chromEnd, and optional name/score/strand fields). Convert numeric or boolean feature columns to appropriate score values (e.g., 1/0 for boundaries or scaled insulation values). Write the DataFrame to a tab-delimited text file with .bed extension, ensuring coordinates are 0-based half-open intervals as per BED specification. Validate the output by checking that (1) row count matches input, (2) coordinate columns are numeric and properly ordered, (3) file is tab-delimited, and (4) the file can be loaded into a genome browser or validated with bedtools.

## Related tools

- **pandas** (DataFrame creation, manipulation, and export to delimited text)
- **cooler** (Source of Hi-C bin coordinates and metadata for DataFrame construction) — https://github.com/open2c/cooler
- **cooltools.insulation** (Produces the insulation score and is_boundary columns that populate the DataFrame) — https://github.com/open2c/cooltools

## Examples

```
df.to_csv('boundaries.bed', sep='\t', columns=['chrom', 'start', 'end', 'is_boundary'], index=False, header=False)
```

## Evaluation signals

- Output file exists and has .bed extension.
- Row count in BED file matches input DataFrame after filtering (if applicable).
- File is valid tab-delimited text with no extra whitespace or inconsistent delimiter.
- First three columns (chrom, chromStart, chromEnd) are present and correctly formatted; numeric coordinates are properly ordered and in 0-based half-open intervals.
- Optional score or name columns contain expected values and data types (e.g., boolean columns converted to 0/1, numeric insulation scores within expected range).
- BED file can be successfully loaded into a genome browser (e.g., IGV, UCSC) or validated with bedtools without format errors.

## Limitations

- BED format does not natively support multi-value features; if the DataFrame contains multiple annotation columns, only a subset can be represented in a single BED file (score is typically a single numeric field).
- Large DataFrames (millions of rows) may produce very large BED files; consider compression or splitting by chromosome.
- No built-in support for complex feature relationships; if annotations require hierarchical or relational structure, consider GFF3 or other formats.
- Conversion assumes coordinates are already validated and in the expected reference genome; no automatic coordinate lift-over or validation is provided.

## Evidence

- [other] Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns.: "Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns."
- [other] Convert the annotated boundaries to BED format for visualization and downstream analysis.: "Convert the annotated boundaries to BED format for visualization and downstream analysis."
- [other] Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*).: "Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*)."
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced cooler format readily handles storage of high-resolution datasets"
- [readme] how to extract insulation profiles and call boundaries using insulation profile minima: "how to extract insulation profiles and call boundaries using insulation profile minima"
