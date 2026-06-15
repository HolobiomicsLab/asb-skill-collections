---
name: shell-script-executability-validation
description: Use when you have cloned a bioinformatics repository (e.g., FredHutch/SEACR) and need to confirm that its shell and R scripts are executable and will run successfully on your input data (e.g., CUT&RUN bedGraph files) before investing time in a full analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
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

# shell-script-executability-validation

## Summary

Verify that shell scripts within a cloned bioinformatics repository have correct permissions, dependencies, and can execute end-to-end on canonical input data to produce valid output. This skill validates the reproducibility of a computational workflow before relying on it for analysis.

## When to use

You have cloned a bioinformatics repository (e.g., FredHutch/SEACR) and need to confirm that its shell and R scripts are executable and will run successfully on your input data (e.g., CUT&RUN bedGraph files) before investing time in a full analysis. Use this when the documentation is incomplete or untested, or when you need to audit an inherited workflow.

## When NOT to use

- You are auditing code logic or algorithmic correctness beyond execution — this skill only validates end-to-end runtime, not statistical validity or method soundness.
- Input data is already pre-processed and integrated into a larger pipeline — use this skill on isolated workflows only.
- The repository provides pre-built binaries or Docker images; validation of binary executables and containers requires different QA practices.

## Inputs

- cloned repository directory (via git clone)
- minimal test input file conforming to tool's documented format (e.g., bedGraph with zero-signal rows omitted)
- tool dependencies (R, Bedtools, or equivalents named in README)

## Outputs

- validated shell scripts with executable permissions confirmed
- output BED file(s) conforming to documented schema
- execution logs (stdout/stderr) confirming no errors

## How to apply

Clone the target repository using git. Inspect the cloned directory for shell scripts (.sh) and verify that execute permissions are set (chmod +x if needed). Prepare a minimal canonical input file that meets the tool's documented format requirements (e.g., a bedGraph file with chr, start, end, signal columns for SEACR). Execute the script end-to-end with the test input using the documented command-line syntax, capturing stdout and stderr. Verify that the expected output files are produced (e.g., .relaxed.bed or .stringent.bed) and that their structure matches the documented schema (e.g., chr, start, end, total signal, max signal, max signal region for SEACR). If execution succeeds and output schema is valid, the workflow is reproducible.

## Related tools

- **git** (Clone the source repository to a local working directory)
- **SEACR** (Target peak-calling shell script to be validated for executability and end-to-end operation on CUT&RUN bedGraph input) — https://github.com/FredHutch/SEACR
- **R** (Required runtime dependency invoked by SEACR shell script for statistical analysis of enriched regions) — https://www.r-project.org
- **Bedtools** (Required utility for bedGraph processing and format conversion, invoked within SEACR workflow) — https://bedtools.readthedocs.io/en/latest/

## Examples

```
bash SEACR_1.3.sh target.bedgraph 0.01 non stringent output
```

## Evaluation signals

- Shell scripts exist in the cloned repository and have executable permissions (ls -l shows 'x' flag)
- Script executes without runtime errors or missing-dependency exceptions when invoked with canonical test input
- Output file(s) are produced with the documented filename suffix (e.g., .relaxed.bed or .stringent.bed)
- Output file(s) conform to the documented BED schema: exactly 6 tab-separated columns (chr, start, end, total signal, max signal, max signal region) with no missing or malformed rows
- Coordinate ranges in output are valid (start < end, coordinates are non-negative integers)

## Limitations

- This skill validates reproducibility of shell execution, not the statistical or biological validity of results — false peaks or incorrect enrichment thresholds will pass validation if the script runs without error.
- Validation on a minimal test dataset does not guarantee performance on large or complex real-world data; memory exhaustion, numeric overflow, or timeout failures may emerge at scale.
- Dependencies must be pre-installed and in PATH (R, Bedtools); the skill does not validate dependency versions or cross-platform compatibility.
- The skill detects bugs in line 166/168 (misreported terminal coordinates) or filtering logic only if the output schema or coordinates are inspected; silent numeric errors may be missed.

## Evidence

- [readme] It requires R (https://www.r-project.org) and Bedtools (https://bedtools.readthedocs.io/en/latest/) to be available in your path, and it requires bedgraphs from paired-end sequencing as input: "It requires R (https://www.r-project.org) and Bedtools (https://bedtools.readthedocs.io/en/latest/) to be available in your path, and it requires bedgraphs from paired-end sequencing as input"
- [other] Verify that shell scripts and R scripts are present in the cloned repository and have executable permissions set.: "Verify that shell scripts and R scripts are present in the cloned repository and have executable permissions set."
- [readme] Field 1: Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html) that omits regions containing 0 signal.: "Field 1: Target data bedgraph file in UCSC bedgraph format (https://genome.ucsc.edu/goldenpath/help/bedgraph.html) that omits regions containing 0 signal."
- [readme] <chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>: "<chr>	<start>	<end>	<total signal>	<max signal>	<max signal region>"
- [other] Execute SEACR end-to-end on the test bedGraph input using the cloned scripts. Verify that the peaked-regions output file is produced and contains valid region coordinates.: "Execute SEACR end-to-end on the test bedGraph input using the cloned scripts. Verify that the peaked-regions output file is produced and contains valid region coordinates."
