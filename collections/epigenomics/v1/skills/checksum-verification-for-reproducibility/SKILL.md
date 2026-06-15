---
name: checksum-verification-for-reproducibility
description: Use when you have executed a complex multi-step processing pipeline (e.g., ENCODE Hi-C uniform processing pipeline) and need to confirm that the generated output files match a known reference baseline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0080
  tools:
  - ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
  - Juicer
  - sha256sum / md5sum
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_juicer
    doi: 10.1016/j.cels.2016.07.002
    title: juicer
  dedup_kept_from: coll_juicer
schema_version: 0.2.0
---

# checksum-verification-for-reproducibility

## Summary

Validate that a bioinformatics pipeline produces output that is byte-for-byte identical to reference outputs by computing and comparing cryptographic checksums (file hashes). This skill ensures reproducibility of complex workflows like Hi-C map generation by detecting any divergence in pipeline output due to parameter changes, software versions, or computational environments.

## When to use

You have executed a complex multi-step processing pipeline (e.g., ENCODE Hi-C uniform processing pipeline) and need to confirm that the generated output files match a known reference baseline. Use this skill when reproducibility is a project requirement, when validating pipeline porting across compute platforms, or when comparing output from different pipeline versions or parameter sets against a trusted reference.

## When NOT to use

- Output files are expected to differ due to stochastic components (e.g., random initialization, sampling-based algorithms); checksums will never match.
- Pipeline is under active development or rapid iteration; reference checksums may be outdated or unavailable.
- You are validating functional correctness rather than byte-for-byte reproducibility; use differential analysis, statistical comparison, or schema validation instead.

## Inputs

- Output file from multi-step processing pipeline (e.g., .hic binary contact map file)
- Reference output file checksum (computed or provided by pipeline developers)
- Hash algorithm specification (e.g., SHA-256, MD5)

## Outputs

- Computed checksum string for generated output file
- Checksum comparison result (match/mismatch)
- Reproducibility validation report (pass/fail)

## How to apply

After running the pipeline (e.g., encode_hic_pipeline on FASTQ input to generate .hic binary files), compute the cryptographic hash (checksum) of the output file using a standard utility such as sha256sum or md5sum. Obtain or compute the corresponding checksum for the reference output file using the same hashing algorithm and on the same file format. Compare the two checksums byte-for-byte; if they match exactly, the pipeline has reproduced the reference output; if they differ, investigate pipeline parameters, software versions, input data provenance, and computational environment variables that may have caused divergence. Document the hashing algorithm and reference checksum as part of the pipeline validation record.

## Related tools

- **ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)** (Produces the .hic output file whose checksum is to be verified) — https://github.com/ENCODE-DCC/hic-pipeline
- **Juicer** (Underlying pipeline framework for generating Hi-C maps from FASTQ; reference checksums are typically derived from Juicer baseline runs) — https://github.com/aidenlab/juicer
- **sha256sum / md5sum** (GNU coreutils for computing cryptographic hashes of output files)

## Examples

```
sha256sum output.hic > output.hic.sha256 && diff output.hic.sha256 reference.hic.sha256 && echo 'Checksum verification passed'
```

## Evaluation signals

- Computed checksum matches the reference checksum exactly (byte-for-byte equality).
- Hash comparison is performed using the same hashing algorithm (SHA-256, MD5, etc.) on both generated and reference files.
- Checksum validation is documented with the algorithm name, reference value, and date of comparison.
- If checksums diverge, investigate and document the root cause (parameter changes, software version differences, environmental variables) and update reference checksums if the divergence is intentional.
- Validation passes for all intermediate and final output files specified by the pipeline's reference standard.

## Limitations

- Checksum comparison is sensitive to any byte-level change, including metadata, timestamps, or compression parameters; format equivalence does not guarantee checksum equality.
- Reference checksums may be unavailable for early-stage or rapidly evolving pipelines; the skill relies on the existence of a stable, documented reference output.
- Different compute environments (OS, hardware, CUDA version for GPU-accelerated steps, random number generator seeding) may produce outputs with different checksums even if functionally equivalent, particularly for floating-point calculations or GPU-dependent steps.
- Checksum verification does not validate biological correctness or quality of the output; it only confirms reproducibility against a baseline.

## Evidence

- [other] Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash.: "Validate the output Hi-C map file format (e.g., .hic binary format) and compute checksum or file hash."
- [other] Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness.: "Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness."
- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files"
