---
name: bam-to-fragment-file-conversion
description: Use when when you have coordinate-sorted BAM files from single-cell ATAC-seq experiments (e.g., 10X Genomics scATAC-seq) and need to generate a compressed fragment file for efficient downstream analysis. Use this step before matrix generation, clustering, or peak calling in SnapATAC2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - SnapATAC2
  - Python
  - Rust
  - precellar
  - samtools
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# BAM-to-fragment-file conversion

## Summary

Convert coordinate-sorted BAM files into compressed fragment files (BED.gz or .zst format) containing fragment coordinates, cell barcodes, and quality metrics. This preprocessing step is essential for downstream single-cell ATAC-seq analysis in SnapATAC2.

## When to use

When you have coordinate-sorted BAM files from single-cell ATAC-seq experiments (e.g., 10X Genomics scATAC-seq) and need to generate a compressed fragment file for efficient downstream analysis. Use this step before matrix generation, clustering, or peak calling in SnapATAC2.

## When NOT to use

- Input BAM file is not coordinate-sorted; use samtools sort -c to validate or re-sort first.
- Fragment file already exists and has been validated; re-running is redundant unless BAM has been re-aligned.
- Working with RNA-seq or other modalities that do not generate fragment-level data (use pp.import_fragments for pre-existing fragment files instead).

## Inputs

- coordinate-sorted BAM file
- BAM file with cell barcode information in header (for 10X or tagged BAM)

## Outputs

- compressed fragment file (BED.gz or .zst format)
- fragment coordinates with cell barcodes and quality metrics

## How to apply

Load the coordinate-sorted BAM file and invoke pp.make_fragment_file with source='10x' if the input is a 10X BAM file, or with default settings for standard BAM inputs. The function processes alignments, extracts fragment coordinates (chromosome, start, end), assigns cell barcodes from the BAM header, and computes quality metrics including duplication rate. Output is generated in compressed format (BED.gz or zst) with standard BED fields plus barcode and count columns. Validate output by confirming the file is non-empty, contains properly formatted BED columns, and that QC metrics (duplication rate, read counts per cell) are accessible for downstream QC decisions.

## Related tools

- **SnapATAC2** (Python/Rust framework providing pp.make_fragment_file function for BAM-to-fragment conversion with built-in quality metrics and barcode extraction) — https://github.com/scverse/SnapATAC2
- **precellar** (Alternative universal preprocessing package that automates BAM-to-fragment conversion for multiple single-cell genomics platforms via alignment and fragment file generation) — https://github.com/regulatory-genomics/precellar
- **samtools** (Utility for BAM file validation, sorting, and inspection before fragment file conversion)

## Examples

```
import snapatac2 as sa; sa.pp.make_fragment_file('sorted.bam', output='fragments.tsv.zst', source='10x')
```

## Evaluation signals

- Output file is non-empty and has expected file size relative to input BAM (typically 10–30% of BAM size after compression).
- Fragment file contains all mandatory BED format fields: chromosome, start position, end position, cell barcode, and read count (5 columns minimum).
- QC metrics (duplication rate, total fragment count, fragments per cell) are computed and accessible; median fragments per cell is > 0.
- Barcode distribution across fragments is non-uniform and reflects expected cell count (e.g., 500–10,000 unique barcodes for 10X experiment).
- File integrity check: fragment file can be read back into SnapATAC2 using pp.import_fragments without errors; no corrupted records.

## Limitations

- Requires BAM file to be coordinate-sorted; name-sorted or unsorted BAM will produce incorrect or incomplete output.
- Quality metrics (duplication rate, mapping quality) depend on BAM flags and tags being correctly set during alignment; unreliable if input BAM is from non-standard pipelines.
- Performance scales linearly with BAM file size; very large BAM files (>100 GB) may require sufficient disk space and RAM for intermediate processing.
- Cell barcode extraction assumes standard barcoding convention (e.g., 10X CB tag in BAM); non-standard barcode formats or missing tags will result in lost or misassigned barcodes.

## Evidence

- [intro] BAM-to-fragment-file conversion is a preprocessing step in SnapATAC2: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [methods] pp.make_fragment_file is the primary function for converting BAM to fragment files: "BAM/Fragment file processing with pp.make_fragment_file, pp.import_fragments"
- [other] Output should be validated as compressed BED format with expected fields: "Generate fragment file output in compressed format (BED.gz or zst) containing fragment coordinates, cell barcodes, and quality metrics."
- [other] Workflow includes QC metric computation and file validation: "Verify output file integrity and confirm QC metrics (duplication rate, read counts) are computed and accessible."
- [other] 10X BAM files require source parameter specification: "Invoke pp.make_fragment_file with source='10x' if the input is a 10X BAM file, or with default settings for standard BAM inputs."
