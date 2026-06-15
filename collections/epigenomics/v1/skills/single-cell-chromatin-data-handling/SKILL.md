---
name: single-cell-chromatin-data-handling
description: Use when after calling peaks and annotating cells in an ArchR project, when you need to perform trajectory analysis using STREAM or other external tools that require a peak-by-cell matrix in a specific tabular format (CSV or TSV) rather than native ArchR objects.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ArchR
  - STREAM
derived_from:
- doi: 10.1038/s41588-021-00790-6
  title: archr
evidence_spans:
- ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_archr
    doi: 10.1038/s41588-021-00790-6
    title: archr
  dedup_kept_from: coll_archr
schema_version: 0.2.0
---

# single-cell-chromatin-data-handling

## Summary

Export peak-by-cell matrices from ArchR processed scATAC-seq projects into formats compatible with trajectory analysis tools such as STREAM. This skill bridges chromatin accessibility data with downstream trajectory inference by standardizing matrix representation and format.

## When to use

After calling peaks and annotating cells in an ArchR project, when you need to perform trajectory analysis using STREAM or other external tools that require a peak-by-cell matrix in a specific tabular format (CSV or TSV) rather than native ArchR objects.

## When NOT to use

- Input data are already in STREAM-native format or another trajectory tool format; re-exporting will cause redundant processing.
- Peak calls have not yet been performed on the ArchR project; missing peak annotations will result in an empty or malformed matrix.
- Using trajectory tools other than STREAM that have native ArchR support (monocle3, Slingshot); ArchR provides direct integration functions for these.

## Inputs

- ArchR project object (processed with peak calls and cell annotations)
- Peak-by-cell accessibility matrix (internal to ArchR project)

## Outputs

- STREAM-compatible peak-by-cell matrix file (CSV or TSV format)
- Peak identifiers and cell barcodes in STREAM-expected tabular layout

## How to apply

Load a processed ArchR project object containing peak calls and cell annotations. Call the exportPeakMatrixForSTREAM function on the ArchR project to generate a peak-by-cell matrix formatted for STREAM compatibility. Write the resulting matrix to a file in STREAM-compatible format (typically CSV or TSV). The function handles matrix transposition and formatting internally; the user need only specify the output file path. This enables seamless integration with trajectory analysis workflows while preserving the peak-cell accessibility patterns derived from scATAC-seq analysis.

## Related tools

- **ArchR** (scATAC-seq processing, peak calling, and matrix export via exportPeakMatrixForSTREAM function) — https://github.com/GreenleafLab/ArchR
- **STREAM** (Trajectory analysis tool that accepts the exported peak matrix for cell state inference)
- **R** (Programming environment for executing ArchR functions and file I/O operations)

## Examples

```
exportPeakMatrixForSTREAM(ArchRProj = proj, outputFile = "peaks_for_stream.csv")
```

## Evaluation signals

- Output file exists and is readable as CSV or TSV with consistent row (peak) and column (cell) structure.
- Peak identifiers and cell barcodes in the exported matrix match those in the original ArchR project.
- Matrix dimensions (peaks × cells) are non-empty and consistent with the peak calls and cell annotations in the input project.
- STREAM successfully ingests the exported matrix without parsing or format errors.
- Accessibility values in the matrix are numeric, non-negative, and fall within the expected range for the scATAC-seq assay (e.g., 0–1 for normalized counts or log-transformed values).

## Limitations

- exportPeakMatrixForSTREAM is specific to STREAM compatibility; users requiring export for other trajectory tools must use tool-specific functions or manually format the matrix.
- The export assumes peaks have been called and cells have been annotated in the ArchR project; incomplete or missing annotation data will propagate to the output file.
- No changelog was provided in the source material, limiting visibility into version-specific behavior or recent bug fixes.

## Evidence

- [intro] ArchR enables export of peak matrix compatible with STREAM via exportPeakMatrixForSTREAM function: "ArchR now enables export of a peak matrix that is compatible with STREAM! See updates with exportPeakMatrixForSTREAM"
- [other] Workflow involves loading project, calling export function, and writing matrix to file: "Load a processed ArchR project object containing peak calls and cell annotations. 2. Call exportPeakMatrixForSTREAM on the ArchR project to generate a peak-by-cell matrix formatted for STREAM"
- [readme] ArchR is full-featured R package for scATAC-seq: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
- [readme] ArchR supports direct trajectory analysis with monocle3 and Slingshot: "ArchR now directly supports both monocle3 and Slingshot based trajectory analysis!"
