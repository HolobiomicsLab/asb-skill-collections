---
name: repository-cloning-and-dependency-verification
description: Use when you have identified a published computational tool (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0492
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3169
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

# repository-cloning-and-dependency-verification

## Summary

Clone a scientific software repository from GitHub and verify that all required executable dependencies (shell scripts, R scripts, external tools) are present and properly configured for end-to-end execution on representative input data. This skill ensures that published computational workflows are reproducible before committing to full-scale analysis.

## When to use

You have identified a published computational tool (e.g., SEACR for CUT&RUN peak calling) available on GitHub and need to confirm that the source code is complete, executable scripts are present, required dependencies (R, Bedtools) are available in your environment, and the tool can process representative input files (e.g., CUT&RUN bedGraph files) to produce expected output (e.g., BED files of enriched regions) before running it on your experimental data.

## When NOT to use

- The tool is already installed and functioning in your environment via package manager or containerized distribution — verification is redundant.
- You are working with only pre-computed results and have no need to re-execute the source workflow.
- The repository is private or restricted and you lack access credentials to clone it.

## Inputs

- GitHub repository URL or clone path (e.g., FredHutch/SEACR)
- Representative input data file in tool-specified format (e.g., CUT&RUN bedGraph file omitting zero-signal regions)
- Tool README or documentation describing expected input format and required dependencies

## Outputs

- Cloned local repository directory with all source code and scripts
- Verification report confirming presence and executable status of shell and R scripts
- Tool-generated output file(s) in documented format (e.g., BED file of enriched regions with columns: chr, start, end, total signal, max signal, max signal region)

## How to apply

First, clone the target repository using `git clone` to obtain all source code and scripts. Second, inspect the cloned directory structure to verify that executable shell scripts (e.g., SEACR_1.3.sh) and R scripts are present and have executable permissions set. Third, confirm that all external dependencies listed in the README (e.g., R, Bedtools) are installed and available in your PATH. Fourth, prepare a minimal test input file conforming to the tool's documented input format (e.g., a small CUT&RUN bedGraph file that omits zero-signal regions). Fifth, execute the tool end-to-end using the prescribed invocation pattern (e.g., `bash SEACR_1.3.sh target.bedgraph control.bedgraph norm stringent output`). Finally, verify that the expected output file is produced, contains the documented output structure (e.g., BED format with chr, start, end, total signal, max signal, max signal region columns), and exhibits reasonable coordinate ranges and signal values.

## Related tools

- **git** (clone the GitHub repository to obtain source code and scripts)
- **R** (required dependency for SEACR statistical peak-calling logic; must be available in PATH) — https://www.r-project.org
- **Bedtools** (required dependency for bedgraph manipulation and genomic interval operations in SEACR; must be available in PATH) — https://bedtools.readthedocs.io/en/latest/
- **SEACR** (target tool being cloned and verified; shell script that orchestrates peak calling on CUT&RUN bedGraph input) — https://github.com/FredHutch/SEACR

## Examples

```
bash SEACR_1.3.sh target.bedgraph IgG.bedgraph norm stringent output
```

## Evaluation signals

- The cloned directory contains the expected shell script (e.g., SEACR_1.3.sh) with executable permissions (verified via `ls -la` or `test -x`)
- All documented external dependencies (R, Bedtools) are present in PATH and can be invoked (verified via `which R` and `which bedtools`)
- The tool executes without error on the test input file and produces an output file with the documented name pattern (e.g., `output.stringent.bed` or `output.relaxed.bed`)
- The output file conforms to the documented schema: BED format with 6 columns (chr, start, end, total signal, max signal, max signal region), coordinates are numeric and sensible, and signal values are non-negative numbers
- The output region coordinates do not exceed chromosome bounds and contain fewer total regions than the input bedGraph to confirm filtering/merging was applied

## Limitations

- The README documents that input bedGraph files must omit regions containing zero signal; if your input includes zero-signal lines, SEACR v1.3 will filter them, but earlier versions may fail or produce incorrect results.
- SEACR requires paired-end sequencing data represented as read pairs (fragments), not individual reads; input BAM files must be converted using documented bedtools commands (bamtobed -bedpe, genomecov -bg) before use.
- Normalization of control data to target data (the 'norm' option) is recommended; using 'non' normalization requires prior external normalization (e.g., via spike-in) to avoid spurious thresholds.
- The tool depends on R and Bedtools being available in PATH; Docker or conda environments may be required if these are not installed system-wide.
- Peak-calling thresholds are sensitive to sequencing depth and noise profile; relaxed vs. stringent mode selection affects sensitivity/specificity trade-off and may require benchmarking on positive control regions.

## Evidence

- [readme] Required dependencies and invocation syntax: "It requires R (https://www.r-project.org) and Bedtools (https://bedtools.readthedocs.io/en/latest/) to be available in your path, and it requires bedgraphs from paired-end sequencing as input"
- [readme] Input format specification: "Field 1: Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html) that omits regions containing 0 signal."
- [readme] Output format and structure: "Output file: <output prefix>.stringent.bed OR <output prefix>.relaxed.bed (BED file of enriched regions); Output data structure: <chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>"
- [readme] Version-specific bug fix affecting zero-signal handling: "v1.3: Added a check to filter out any input bedgraph lines containing zero signal."
- [readme] Executable invocation example: "bash SEACR_1.3.sh target.bedgraph IgG.bedgraph norm stringent output; Calls enriched regions in target data using normalized IgG control track with stringent threshold"
