---
name: end-to-end-bioinformatics-pipeline-testing
description: Use when after cloning or installing a peak-calling or genomic analysis tool from a repository, before using it on production data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - git
  - SEACR
  - R
  - Bedtools
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

# end-to-end-bioinformatics-pipeline-testing

## Summary

Verify that a cloned bioinformatics tool (shell and R scripts) executes correctly from start to finish on real or representative input data, producing valid output with correct structure and coordinate ranges. This skill validates both tool availability and computational correctness before integration into larger analyses.

## When to use

After cloning or installing a peak-calling or genomic analysis tool from a repository, before using it on production data. Triggers include: (1) first deployment of the tool in a new environment, (2) version upgrade or bug-fix release, (3) uncertainty about whether dependencies (R, Bedtools) are correctly installed in your PATH, or (4) need to confirm the tool accepts your input bedgraph format and produces the expected BED region output.

## When NOT to use

- Input bedgraph file contains individual reads rather than read-pair density; convert to fragment-level bedgraph first using bedtools genomecov on paired-end BED files.
- Required dependencies (R, Bedtools) are not installed or not in PATH; install and configure them before running end-to-end test.
- Input bedgraph includes zero-signal regions; SEACR expects bedgraph files that omit regions with 0 signal, so preprocess to remove them.

## Inputs

- Paired-end CUT&RUN bedgraph file in UCSC bedgraph format (omitting zero-signal regions)
- Control (IgG) bedgraph file or numeric threshold between 0 and 1
- Cloned or installed SEACR repository with shell and R scripts

## Outputs

- BED file of enriched regions (<output prefix>.stringent.bed or <output prefix>.relaxed.bed)
- Six-column BED with fields: chromosome, start, end, total signal, max signal, max signal region

## How to apply

Clone the tool repository and verify that executable shell and R scripts are present with correct permissions. Prepare a minimal test bedgraph file in UCSC bedgraph format (omitting zero-signal regions) that represents paired-end CUT&RUN sequencing density. Execute the pipeline end-to-end using both required input modes: (a) with a control bedgraph and normalization flag ('norm' or 'non'), and (b) optionally with a numeric threshold (0–1 range) to select top fraction of peaks by signal. Verify the output BED file is produced at the specified prefix, contains valid genomic coordinates (chr, start, end), and includes the six expected fields (chromosome, start, end, total signal, max signal, max signal region). Check that region coordinates are non-negative, start ≤ end, and signal values are numeric and reasonable for your peak height expectations.

## Related tools

- **SEACR** (Peak-calling shell script that processes bedgraph input, applies sparse enrichment thresholds, and outputs BED regions) — https://github.com/FredHutch/SEACR
- **R** (Required runtime for SEACR's R scripts performing threshold calculation and signal analysis) — https://www.r-project.org
- **Bedtools** (Prerequisite utility for bedgraph manipulation and coordinate conversion) — https://bedtools.readthedocs.io/en/latest/
- **git** (Version control system for cloning the SEACR repository from GitHub)

## Examples

```
bash SEACR_1.3.sh target.bedgraph IgG.bedgraph norm stringent output
```

## Evaluation signals

- Output BED file is created at the expected prefix location with correct suffix (.stringent.bed or .relaxed.bed).
- Output BED file contains exactly six tab-delimited columns: chromosome, start coordinate, end coordinate, total signal (numeric), max signal (numeric), max signal region (coordinate range).
- All region start and end coordinates are non-negative integers with start ≤ end, and chromosomes match the input bedgraph.
- Signal values (columns 4–5) are positive real numbers reflecting bedgraph intensity, not NaN or infinite values.
- End-to-end execution completes without R or shell errors; script exits with status 0.

## Limitations

- SEACR requires R and Bedtools to be available in the system PATH; if either is missing or misconfigured, the shell script will fail silently or with cryptic dependency errors.
- Input bedgraph must omit zero-signal regions; inclusion of zero-signal lines may cause incorrect threshold calculation or filtering.
- The tool filters out bedgraph lines containing zero signal and filters signal blocks composed of very few bedgraph lines; extremely sparse datasets may produce few or no peaks even with relaxed threshold.
- Control bedgraph normalization ('norm' flag) assumes that experimental and control data have comparable library complexity; if they differ markedly in depth or composition, normalization may fail or produce spurious thresholds.

## Evidence

- [other] Clone the FredHutch/SEACR repository and verify scripts: "Clone the FredHutch/SEACR repository from GitHub using git. Verify that shell scripts and R scripts are present in the cloned repository and have executable permissions set."
- [other] Prepare minimal test input: "Prepare a minimal CUT&RUN bedGraph input file meeting SEACR format requirements."
- [other] Execute end-to-end and verify output: "Execute SEACR end-to-end on the test bedGraph input using the cloned scripts. Verify that the peaked-regions output file is produced and contains valid region coordinates."
- [readme] Input format and dependencies: "It requires R (https://www.r-project.org) and Bedtools (https://bedtools.readthedocs.io/en/latest/) to be available in your path, and it requires bedgraphs from paired-end sequencing as input"
- [readme] Output structure definition: "<chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>"
- [readme] Bedgraph format requirement: "Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html) that omits regions containing 0 signal."
- [readme] Zero-signal filtering in v1.3: "Added a check to filter out any input bedgraph lines containing zero signal."
