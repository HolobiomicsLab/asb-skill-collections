---
name: hi-c-map-artifact-validation
description: Use when after executing the Juicer pipeline on raw Hi-C FASTQ files, to confirm that the pipeline has generated the expected .hic output artifact and that the contact matrix construction and normalization steps completed without error.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - Juicer
  - Juicer Tools
  - ENCODE Hi-C uniform processing pipeline
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

# hi-c-map-artifact-validation

## Summary

Verification that a Juicer Hi-C processing pipeline has completed successfully and produced a valid .hic output file containing processed Hi-C contact map data. This skill ensures the pipeline's contact matrix construction, normalization, and artifact generation steps have executed correctly before downstream analysis.

## When to use

After executing the Juicer pipeline on raw Hi-C FASTQ files, to confirm that the pipeline has generated the expected .hic output artifact and that the contact matrix construction and normalization steps completed without error.

## When NOT to use

- Input data are already in .hic format (pre-processed contact maps)
- The pipeline stage parameter is set to 'early' (early exit requested)
- Raw FASTQ files have not yet been processed through the alignment and contact matrix construction stages

## Inputs

- FASTQ raw Hi-C sequencing data files
- reference genome file
- restriction enzyme site file
- Juicer pipeline execution logs

## Outputs

- .hic file (processed Hi-C contact map artifact)
- validation status report
- contact matrix statistics

## How to apply

After the Juicer pipeline execution completes, verify the presence and integrity of the .hic output file in the designated output directory. Check that the pipeline's log files indicate successful completion of all stages: read alignment, contact matrix construction, and normalization. Confirm that the .hic file is a valid Java serialized object by attempting to load it with Juicer Tools' viewing or analysis commands. Validate that the contact matrix dimensions match the reference genome's chromosome structure and that normalized contact frequencies are present across expected resolution scales (kilobase resolution).

## Related tools

- **Juicer** (Pipeline orchestration and Hi-C map generation from raw FASTQ data) — https://github.com/aidenlab/juicer
- **Juicer Tools** (Command-line utility for validating, viewing, and analyzing .hic contact map files) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline** (Cloud-based Juicer wrapper using Cromwell/Caper for production Hi-C processing) — https://github.com/ENCODE-DCC/hic-pipeline

## Examples

```
After pipeline execution completes, inspect the output: `ls -lh [topDir]/aligned/*.hic && java -jar juicer_tools.jar dump [topDir]/aligned/merged_nodups.hic 1 1 BP 100000 output.txt` to verify the .hic file exists and contains valid contact matrices.
```

## Evaluation signals

- Presence and non-zero file size of .hic output file in [topDir]/aligned or designated output directory
- Pipeline log files report successful completion of 'final' and 'postproc' stages without error messages
- Juicer Tools can successfully load and read the .hic file without I/O or serialization errors
- Contact matrix dimensions correspond to reference genome chromosomes and total contact counts are consistent with input sequencing depth
- .hic file header contains valid normalization vectors and resolution metadata (kilobase-scale contact frequency arrays)

## Limitations

- Validation only confirms artifact generation; it does not assess biological quality or detect artifacts from library preparation issues (e.g., low ligation efficiency, high chimera rates)
- The pipeline requires a cluster or multi-core environment (ideally ≥4 cores and ≥64 GB RAM); single-CPU execution is supported but significantly slower
- CUDA-based peak calling (HiCCUPS) requires an NVIDIA GPU; CPU-only deployments require alternate peak-calling workflows
- AWS scripts in the main repository are deprecated; cloud execution should use the ENCODE dockerized pipeline instead

## Evidence

- [other] Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map.: "Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map."
- [other] Juicer includes a pipeline that generates Hi-C maps from fastq raw data files as input, producing processed Hi-C map artifacts.: "Juicer includes a pipeline that generates Hi-C maps from fastq raw data files as input, producing processed Hi-C map artifacts."
- [readme] pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps: "pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps"
- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data: "Juicer is a platform for analyzing kilobase resolution Hi-C data"
- [readme] Juicer consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools.: "Juicer consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools."
