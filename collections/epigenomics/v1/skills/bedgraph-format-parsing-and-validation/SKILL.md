---
name: bedgraph-format-parsing-and-validation
description: Use when you have generated or received bedGraph files from paired-end sequencing (via bedtools genomecov or similar) and need to verify they conform to UCSC bedGraph format before passing them to peak-calling tools like SEACR.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3192
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3169
  tools:
  - git
  - SEACR
  - bedtools bamtobed
  - bedtools genomecov
derived_from:
- doi: 10.1186/s13072-019-0287-4
  title: seacr
evidence_spans:
- Clone the SEACR repository
- github:FredHutch__SEACR
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_seacr
    doi: 10.1186/s13072-019-0287-4
    title: seacr
  dedup_kept_from: coll_seacr
schema_version: 0.2.0
---

# bedgraph-format-parsing-and-validation

## Summary

Parse and validate UCSC bedGraph files to ensure they meet format requirements for sparse chromatin profiling analysis, particularly for CUT&RUN peak-calling workflows. This skill detects malformed coordinates, missing signal fields, and zero-signal regions that must be filtered before downstream peak-calling.

## When to use

You have generated or received bedGraph files from paired-end sequencing (via bedtools genomecov or similar) and need to verify they conform to UCSC bedGraph format before passing them to peak-calling tools like SEACR. Use this when input bedGraphs have unknown provenance, were generated from custom pipelines, or have failed in downstream analysis.

## When NOT to use

- Input is already a peak-called BED file with enriched regions; parse as standard BED3 or BED6 instead.
- Input is a single-end BAM or fragment file where read pair structure is unknown; cannot reliably convert to density-based bedGraph without pair information.
- Input is a different wiggle format (e.g., bedWig, variableStep); requires format-specific parser.

## Inputs

- UCSC bedGraph file (tab-delimited: chr, start, end, signal)
- Paired-end BAM file (optional, for de novo bedGraph generation)
- Paired-end BED file with 5' and 3' read coordinates (optional)

## Outputs

- Validated UCSC bedGraph file with zero-signal lines removed
- Parsed bedGraph dataframe or table (for downstream analysis)
- Coordinate and signal validation report

## How to apply

Verify that bedGraph input adheres to UCSC bedGraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html), checking that each line contains four tab-delimited fields: chromosome, start coordinate, end coordinate, and signal value. Filter out any bedGraph lines containing zero signal, as SEACR and similar tools expect bedGraphs that omit regions with zero coverage. Validate coordinate ordering (start < end) and signal values as numeric. If converting from BAM files, follow the paired-end fragment workflow: convert to bedpe format with bedtools bamtobed, extract 5' and 3' termini coordinates, sort, and generate the bedGraph using bedtools genomecov with the -bg flag to produce density across read pairs rather than individual reads.

## Related tools

- **bedtools bamtobed** (Convert paired-end BAM to BEDPE format for fragment extraction) — https://bedtools.readthedocs.io/en/latest/
- **bedtools genomecov** (Generate bedGraph from fragment BED coordinates using -bg flag for density coverage) — https://bedtools.readthedocs.io/en/latest/
- **SEACR** (Peak-calling tool that requires zero-signal-filtered bedGraph input) — https://github.com/FredHutch/SEACR

## Examples

```
bedtools genomecov -bg -i fragments.bed -g my.genome > target.bedgraph && awk '$4 > 0' target.bedgraph > target.filtered.bedgraph
```

## Evaluation signals

- All lines conform to UCSC bedGraph format with exactly 4 tab-delimited fields per line
- No lines contain signal value of 0; all zero-coverage regions are omitted
- Chromosome names are consistent and recognized (e.g., chr1, chr2, chrX)
- Start coordinates are always < end coordinates; coordinates are non-negative integers
- Signal values are positive numeric (float or integer); no non-numeric or malformed entries
- File parses without syntax errors in bedGraph parsers (e.g., UCSC genome browser, SEACR input validation)

## Limitations

- bedGraph format assumes contiguous, non-overlapping regions within a chromosome; overlapping signal blocks may cause ambiguity in downstream interpretation.
- Conversion from BAM to bedGraph is sensitive to paired-end read quality, filtering, and fragment-size cutoffs (e.g., fragments >1000 bp should be filtered during conversion as shown in the README example).
- bedGraph represents only coverage/signal density; it does not capture base-pair-level quality scores, strand information, or individual read identity—those data are lost after conversion.
- Zero-signal filtering assumes sparse data; if background signal is present (non-zero across most regions), bedGraph may become very large and bedGraph-based thresholding in peak-calling may fail.
- Normalization between target and control bedGraphs must be performed before or after bedGraph generation; bedGraph format itself does not encode normalization metadata.

## Evidence

- [readme] UCSC bedGraph format requirement: "Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html) that omits regions containing 0 signal."
- [readme] Zero-signal filtering requirement: "Added a check to filter out any input bedgraph lines containing zero signal."
- [readme] Paired-end fragment density conversion workflow: "Bedgraph files should reflect density across *read pairs* rather than individual reads. If starting from BAM files, we recommend converting to paired end BED files using bedtools bamtobed with the"
- [readme] bedTools genomecov -bg flag requirement: "can be generated from *read pair* BED files (i.e. BED coordinates reflecting the 5' and 3' termini of each read pair) using bedtools genomecov with the "-bg" flag"
- [readme] Fragment-size filtering in BAM-to-bedGraph conversion: "awk '$1==$4 && $6-$2 < 1000 {print $0}' $sample.bed > $sample.clean.bed"
