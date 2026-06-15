---
name: untargeted-metabolomics-data-processing
description: Use when you have two separate LC-MS untargeted metabolomic feature tables (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - M2S
derived_from:
- doi: 10.1021/acs.analchem.1c03592
  title: m2s
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  dedup_kept_from: coll_m2s
schema_version: 0.2.0
---

# untargeted-metabolomics-data-processing

## Summary

Match corresponding untargeted metabolomic features across two LC-MS datasets using retention time and mass-to-charge ratio alignment. This skill bridges two independent feature tables to enable comparative metabolomics analysis by identifying and linking chemically identical or highly similar features.

## When to use

You have two separate LC-MS untargeted metabolomic feature tables (e.g., from different sample cohorts, instrument runs, or data processing pipelines) and need to establish one-to-one correspondences between features to perform downstream comparative analysis, statistical testing, or combined feature annotation.

## When NOT to use

- Input is already a single unified feature table or features are already matched across datasets
- Only one LC-MS dataset is available or comparative feature alignment is not the analysis goal
- Features lack reliable retention time or mass-to-charge ratio measurements (e.g., very low resolution or high noise)

## Inputs

- LC-MS untargeted metabolomic feature table 1 (retention time, m/z, intensity matrix)
- LC-MS untargeted metabolomic feature table 2 (retention time, m/z, intensity matrix)

## Outputs

- Matched feature table with feature correspondence links and matching scores
- Feature pairing indices or identifiers from both input datasets

## How to apply

Load both LC-MS untargeted metabolomic feature datasets (containing retention time and m/z values) into Matlab. Initialize the M2S package with both feature tables as input parameters. Execute the M2S matching algorithm, which identifies feature correspondences by computing similarity scores based on retention time proximity and mass-to-charge ratio alignment. The algorithm links features across datasets where their physicochemical signatures (RT and m/z) are sufficiently similar. Export the resulting matched feature table, which contains feature IDs or indices from both datasets, their correspondence links, and matching confidence scores. Validate the output by inspecting the matching score distribution and spot-checking representative matches against the original RT and m/z values.

## Related tools

- **M2S** (Matlab package executing the feature matching algorithm using retention time and m/z similarity) — https://github.com/rjdossan/M2S

## Evaluation signals

- Matching score distribution is unimodal and concentrated in the expected range (indicate by visual inspection of score histogram)
- Number of matched feature pairs is reasonable relative to the sizes of input feature tables (e.g., not zero or 100% of the smaller table)
- Spot-check: randomly selected matched pairs exhibit minimal retention time drift (within instrument calibration tolerance) and m/z error (within mass accuracy of the instrument)
- Matched features can be validated against independent chemical standards or orthogonal identification methods (e.g., MS/MS spectra, reference databases)
- Output table contains all required columns: feature IDs/indices from both datasets, matching scores, and linked RT and m/z values

## Limitations

- Matching accuracy depends on the quality and reproducibility of retention time measurements and m/z calibration across the two LC-MS runs; poorly calibrated instruments or drifting RT will reduce matching sensitivity
- The algorithm may fail or produce false matches when features have similar m/z but different chemical identity (isomers, isobars) or when RT variation exceeds expected instrument tolerance
- No guidance provided in the README or article on parameter tuning (e.g., RT tolerance window, m/z error threshold) for different instrumental platforms or metabolite classes

## Evidence

- [other] M2S is a Matlab package designed to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] The M2S algorithm identifies and links corresponding features across the two datasets based on retention time and mass-to-charge ratio similarity: "Execute the M2S matching algorithm to identify and link corresponding features across the two datasets based on retention time and mass-to-charge ratio similarity"
- [other] The workflow produces a matched feature table containing feature correspondences and matching scores as the primary output: "Generate and export the matched feature table containing feature correspondences and matching scores"
