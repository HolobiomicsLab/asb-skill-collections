---
name: scatac-seq-peak-matrix-export
description: Use when after completing peak calling and cell annotation in an ArchR project, when you intend to perform trajectory analysis using STREAM rather than ArchR's native monocle3 or Slingshot integrations, or when you need to share peak-by-cell matrices with collaborators using STREAM pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0769
  tools:
  - R
  - ArchR
  - STREAM
  - monocle3
  - Slingshot
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

# scatac-seq-peak-matrix-export

## Summary

Export a peak-by-cell accessibility matrix from a processed ArchR project into STREAM-compatible format for downstream trajectory analysis. This skill bridges scATAC-seq peak quantification and external trajectory inference tools.

## When to use

After completing peak calling and cell annotation in an ArchR project, when you intend to perform trajectory analysis using STREAM rather than ArchR's native monocle3 or Slingshot integrations, or when you need to share peak-by-cell matrices with collaborators using STREAM pipelines.

## When NOT to use

- Your downstream analysis uses monocle3 or Slingshot, which ArchR directly supports via addMonocleTrajectory or addSlingShotTrajectories without intermediate export.
- You require gene expression matrices rather than chromatin accessibility; use addGeneExpressionMatrix instead.
- Your peak matrix has already been exported or you are working with pre-computed accessibility matrices from external sources.

## Inputs

- ArchR project object (containing peak calls and cell annotations)
- Cell metadata with trajectory or treatment information

## Outputs

- Peak-by-cell matrix in STREAM-compatible format (CSV or TSV)
- Matrix with peaks as rows and cells as columns

## How to apply

Load a processed ArchR project object containing peak calls and cell metadata annotations. Call the exportPeakMatrixForSTREAM function on the ArchR project to generate a peak-by-cell matrix formatted for STREAM compatibility. The function outputs a matrix where rows represent peaks (genomic loci) and columns represent single cells, with binary or continuous accessibility values. Write the resulting matrix to a file in STREAM-compatible format (typically CSV or TSV). Verify the output matrix dimensions match your expected peak and cell counts, and confirm the file format matches STREAM's input requirements.

## Related tools

- **ArchR** (Primary R package for scATAC-seq processing; provides the exportPeakMatrixForSTREAM function to generate STREAM-compatible peak matrices.) — https://github.com/GreenleafLab/ArchR
- **STREAM** (Downstream trajectory analysis tool that accepts peak-by-cell matrices exported from ArchR.)
- **monocle3** (Alternative trajectory analysis tool directly supported by ArchR; use if STREAM export is not needed.)
- **Slingshot** (Alternative trajectory analysis tool directly supported by ArchR; use if STREAM export is not needed.)

## Examples

```
exportPeakMatrixForSTREAM(ArchRProject = archr_proj, outputFile = 'peaks_by_cells_stream.csv')
```

## Evaluation signals

- Output matrix dimensions match the number of peaks called and number of cells in the ArchR project.
- File format is valid CSV or TSV with proper delimiters and no truncation.
- Matrix contains only numeric values (binary or continuous accessibility scores); no missing values in cell or peak identifiers.
- Peak identifiers follow genomic coordinate format (e.g., chr:start-end) consistent with the input ArchR project.
- Cell identifiers in the matrix match the cell barcodes in the ArchR project metadata.

## Limitations

- The skill is specific to STREAM compatibility; other trajectory tools may require different export formats or matrix structures.
- No changelog documentation is available to confirm version-specific behavior or recent API changes.
- The function assumes peaks have already been called and annotated in the ArchR project; incomplete peak calling will produce incomplete matrices.
- Large projects (>1 million cells or >100k peaks) may require substantial memory and disk space for the exported matrix file.

## Evidence

- [other] ArchR enables export of a peak matrix that is compatible with STREAM through the exportPeakMatrixForSTREAM function.: "ArchR enables export of a peak matrix that is compatible with STREAM through the exportPeakMatrixForSTREAM function."
- [readme] ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data.: "ArchR is a full-featured R package for processing and analyzing single-cell ATAC-seq data."
- [other] Load a processed ArchR project object containing peak calls and cell annotations, call exportPeakMatrixForSTREAM to generate a peak-by-cell matrix formatted for STREAM compatibility, and write the resulting matrix to a file in STREAM-compatible format.: "Load a processed ArchR project object containing peak calls and cell annotations. 2. Call exportPeakMatrixForSTREAM on the ArchR project to generate a peak-by-cell matrix formatted for STREAM"
- [readme] ArchR now enables export of a peak matrix that is compatible with STREAM with the exportPeakMatrixForSTREAM function.: "Additionally ArchR now enables export of a peak matrix that is compatible with STREAM!\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;See updates with exportPeakMatrixForSTREAM"
