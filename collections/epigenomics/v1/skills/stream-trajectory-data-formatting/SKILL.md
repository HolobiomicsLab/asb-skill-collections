---
name: stream-trajectory-data-formatting
description: Use when you have completed peak calling and cell annotation in ArchR and want to perform trajectory inference or visualization in STREAM. Apply it specifically when your analysis goal requires STREAM's specialized trajectory reconstruction methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3295
  tools:
  - R
  - STREAM
  - ArchR
derived_from:
- doi: 10.1038/s41588-021-00790-6
  title: archr
evidence_spans:
- ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data
- ArchR now enables export of a peak matrix that is compatible with STREAM
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

# Reconstruct peak matrix export for STREAM compatibility via exportPeakMatrixForSTREAM

## Summary

Export a peak-by-cell matrix from ArchR in a format compatible with STREAM trajectory analysis tool. This skill enables interoperability between ArchR's scATAC-seq processing and STREAM's trajectory inference, allowing users to leverage STREAM's visualization and analysis capabilities on ArchR-processed peak data.

## When to use

Use this skill when you have completed peak calling and cell annotation in ArchR and want to perform trajectory inference or visualization in STREAM. Apply it specifically when your analysis goal requires STREAM's specialized trajectory reconstruction methods (e.g., elastic principal graphs, branching structure inference) on single-cell ATAC-seq peak data.

## When NOT to use

- If your downstream trajectory tool is monocle3 or Slingshot — ArchR directly supports these via getMonocleTrajectories and addSlingShotTrajectories, without export overhead.
- If you need to preserve full dimensionality reduction or embedding information — STREAM export focuses only on the peak matrix; trajectory-specific embeddings from ArchR are not exported.
- If your peak matrix is already in a STREAM-compatible format from another source — re-exporting introduces redundant processing.

## Inputs

- ArchR project object (processed with peak calls and cell annotations)
- Peak-by-cell accessibility matrix (internal ArchR representation)

## Outputs

- Peak-by-cell matrix in CSV or TSV format compatible with STREAM
- Matrix with peaks as rows and cells as columns

## How to apply

Load a processed ArchR project object containing peak calls and cell annotations. Call the exportPeakMatrixForSTREAM function on the ArchR project to generate a peak-by-cell matrix formatted for STREAM compatibility. The function produces output in CSV or TSV format that conforms to STREAM's expected matrix structure (peaks as rows, cells as columns, binary or accessibility values as matrix entries). Write the resulting matrix to a file and validate that the output dimensions match your peak and cell counts before importing into STREAM. The export preserves the peak-level and cell-level metadata necessary for downstream trajectory analysis.

## Related tools

- **ArchR** (Generates processed peak-by-cell matrix from scATAC-seq data and exports via exportPeakMatrixForSTREAM function) — https://github.com/GreenleafLab/ArchR
- **STREAM** (Downstream trajectory analysis tool that accepts the exported peak matrix for elastic principal graph inference and trajectory visualization)
- **R** (Environment in which ArchR and exportPeakMatrixForSTREAM are executed)

## Examples

```
exportPeakMatrixForSTREAM(ArchRProj = proj, outputFile = "./peak_matrix_for_stream.csv")
```

## Evaluation signals

- Output file exists and is readable in CSV or TSV format with expected dimensions (number of peaks × number of cells).
- Matrix values are consistent with peak accessibility representation (binary or numeric accessibility scores); no missing or NaN values in core data.
- Cell and peak identifiers in the matrix match those in the original ArchR project object.
- File can be successfully imported into STREAM without parse errors or format mismatches.
- Row and column counts in exported matrix align with peak call and cell annotation counts from the ArchR project.

## Limitations

- Export focuses on peak-by-cell matrix only; trajectory-aware metadata, cell-type annotations, and dimensionality reductions computed in ArchR are not automatically exported.
- STREAM export is a one-way conversion; modifications made in STREAM cannot be re-imported into ArchR.
- Large projects (millions of peaks or cells) may produce very large CSV/TSV files; memory and disk constraints may apply.
- The function assumes a standard ArchR project structure; non-standard or corrupted projects may fail export silently or produce malformed output.

## Evidence

- [intro] ArchR enables export of a peak matrix that is compatible with STREAM through the exportPeakMatrixForSTREAM function.: "ArchR enables export of a peak matrix that is compatible with STREAM through the exportPeakMatrixForSTREAM function"
- [intro] Workflow steps for the skill include loading ArchR project, calling exportPeakMatrixForSTREAM, and writing to STREAM-compatible format.: "Load a processed ArchR project object containing peak calls and cell annotations. 2. Call exportPeakMatrixForSTREAM on the ArchR project to generate a peak-by-cell matrix formatted for STREAM"
- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data"
- [readme] ArchR now enables export of a peak matrix compatible with STREAM.: "ArchR now enables export of a peak matrix that is compatible with STREAM! See updates with exportPeakMatrixForSTREAM"
