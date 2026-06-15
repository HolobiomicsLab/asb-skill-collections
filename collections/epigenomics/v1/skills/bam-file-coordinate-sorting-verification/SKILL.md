---
name: bam-file-coordinate-sorting-verification
description: Use when before invoking pp.make_fragment_file on a BAM file from alignment or external sources, especially when the BAM's sort order is unknown or when integrating BAM files from multiple sequencing platforms (10X, standard genomics pipelines, or custom aligners) into a unified SnapATAC2 analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3402
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0080
  tools:
  - SnapATAC2
  - Python
  - Rust
  - samtools
  - precellar
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

# BAM file coordinate sorting verification

## Summary

Verify that input BAM files are coordinate-sorted before preprocessing with SnapATAC2's pp.make_fragment_file, ensuring compatibility with fragment file generation and correct output of chromatin accessibility data.

## When to use

Before invoking pp.make_fragment_file on a BAM file from alignment or external sources, especially when the BAM's sort order is unknown or when integrating BAM files from multiple sequencing platforms (10X, standard genomics pipelines, or custom aligners) into a unified SnapATAC2 analysis.

## When NOT to use

- Input is already a fragment file (BED.gz, .zst, or TSV) — coordinate sorting verification is only needed for BAM inputs.
- Using preprocessing pipelines that auto-sort BAM files internally (e.g., precellar) — verify documentation first.
- Input BAM is from a tool that streams coordinate-sorted output by design — may skip explicit verification if tool documentation guarantees sort order.

## Inputs

- BAM file (aligned single-cell ATAC-seq reads with optional cell barcodes in tags)
- SAM/BAM header or file metadata indicating current sort order

## Outputs

- Confirmation of coordinate sort order (e.g., samtools view header output or sort validation report)
- Re-sorted BAM file (if input was unsorted or query-name sorted)

## How to apply

Check BAM file headers using standard tools (samtools view -H) to confirm the @HD line contains SO:coordinate, or verify coordinate sort order by spot-checking that genomic positions increase monotonically across reads. If the BAM is unsorted or sorted by read name (SO:queryname), re-sort it using samtools sort -o output.bam input.bam before passing to pp.make_fragment_file. The pp.make_fragment_file function expects coordinate-sorted input and will produce compressed fragment files (BED.gz or .zst format) containing fragment coordinates, cell barcodes, and quality metrics only when the input is correctly ordered; misalignment of input sort order will compromise fragment boundary detection and barcode grouping.

## Related tools

- **SnapATAC2** (pp.make_fragment_file function requires coordinate-sorted BAM input to generate compressed fragment files) — https://github.com/scverse/SnapATAC2
- **samtools** (Verification of BAM header sort order and re-sorting coordinate-unsorted BAM files)
- **precellar** (Alternative preprocessing pipeline that automates BAM-to-fragment conversion with internal sort handling) — https://github.com/regulatory-genomics/precellar

## Examples

```
samtools view -H input.bam | grep '@HD' | grep 'SO:coordinate'; samtools sort -o sorted.bam input.bam
```

## Evaluation signals

- BAM header @HD line explicitly contains SO:coordinate tag (or is absent, defaulting to coordinate order per SAM specification).
- Spot-check of ~100 reads shows genomic positions (RNAME:POS pairs) are in non-decreasing order across the file.
- pp.make_fragment_file succeeds without errors and produces non-empty compressed output file (BED.gz or .zst) with expected fields: chrom, start, end, barcode, count.
- Output fragment file contains the expected number of unique cell barcodes and non-zero duplication rates (indicating valid barcode-to-fragment mapping).
- QC metrics reported by pp.make_fragment_file (read counts, duplication rates) match expected ranges for the input dataset.

## Limitations

- BAM files from certain legacy aligners may lack @HD headers; in such cases, coordinate sort order must be inferred from read position sampling.
- Re-sorting very large BAM files (>100 GB) may consume significant disk space and compute time; consider streaming approaches or split-process strategies for production scale.
- Some single-cell platforms (e.g., precellar examples) abstract BAM sorting into internal workflows; explicit verification may be redundant if upstream tool documentation guarantees coordinate-sorted output.
- BAM files with custom or non-canonical chromosome naming may pass sort verification but fail downstream if chromosome names don't match the reference genome used in pp.make_fragment_file.

## Evidence

- [methods] coordinate-sorted BAM file as input to pp.make_fragment_file: "Load the coordinate-sorted BAM file as input to pp.make_fragment_file."
- [intro] pp.make_fragment_file converts BAM to compressed fragment file: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [methods] SnapATAC2 fragment file processing workflow: "BAM/Fragment file processing with pp.make_fragment_file, pp.import_fragments"
- [other] Fragment file output format and metrics: "Generate fragment file output in compressed format (BED.gz or zst) containing fragment coordinates, cell barcodes, and quality metrics."
- [readme] precellar automates BAM to fragment preprocessing: "output='fragments.tsv.zst', output_type='fragment'"
