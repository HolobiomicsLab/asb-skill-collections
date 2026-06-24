---
name: file-format-export-and-validation
description: Use when after executing MassQL queries on mass spectrometry data that
  produce tabulated results (e.g., MS1 or MS2 scan metadata, peak intensities, retention
  times), and you need to persist those results for archival, sharing, or downstream
  statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MassQL
  - MassQLab
  - pandas
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massqlab_cq
    doi: 10.1002/rcm.10132
    title: MassQLab
  dedup_kept_from: coll_massqlab_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.10132
  all_source_dois:
  - 10.1002/rcm.10132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-export-and-validation

## Summary

Serialize mass spectrometry query results to persistent storage in multiple formats (CSV and image) and verify output integrity. This skill ensures that tabulated results from mass spectrometry queries are durably stored and remain accessible for downstream analysis and visualization.

## When to use

After executing MassQL queries on mass spectrometry data that produce tabulated results (e.g., MS1 or MS2 scan metadata, peak intensities, retention times), and you need to persist those results for archival, sharing, or downstream statistical analysis. Specifically, use this skill when in-memory result tables must be written to disk in both human-readable (CSV) and visual (image) forms for reproducibility.

## When NOT to use

- Input is unstructured (e.g., raw binary spectra, unprocessed mzML)—use MassQL query execution first.
- Results are already serialized in target formats (CSV and images present)—skip to validation step.
- Output must remain in memory for real-time interactive exploration—use in-memory visualization instead.

## Inputs

- tabulated query results (in-memory DataFrame or intermediate format from MassQL query execution)
- output directory path (string)
- result metadata (e.g., query name, file source, data type: MS1 or MS2)

## Outputs

- CSV file containing tabulated results with metadata columns
- PNG or raster image file(s) visualizing the results
- validation log confirming file write success and size checks

## How to apply

Load the tabulated query results returned by the MassQL query engine into memory. Serialize the results table to CSV format using a CSV writer (e.g., pandas.DataFrame.to_csv or equivalent), specifying the output directory path. Simultaneously generate visualization image(s) from the tabulated results—the plot type and structure are determined by result shape and content (e.g., peak traces for MS1 analysis, scan intensity plots for MS2 data). Save visualization(s) as PNG or equivalent raster format to the same output directory. Finally, verify that both CSV and image files are written with correct format, non-zero file size, and match expected schema before marking the export complete.

## Related tools

- **MassQL** (produces tabulated query results that are serialized by this skill) — https://github.com/mwang87/MassQueryLanguage
- **MassQLab** (orchestrates MassQL query execution and invokes result export and validation for MS1 and MS2 outputs) — https://github.com/JohnsonDylan/MassQLab
- **pandas** (provides DataFrame.to_csv() and DataFrame manipulation for serialization)

## Examples

```
results_df.to_csv('ms1_raw_df.csv'); plt.figure(); plt.plot(results_df['rt'], results_df['intensity']); plt.savefig('ms1_traces.png', dpi=100); os.path.getsize('ms1_raw_df.csv') > 0 and os.path.getsize('ms1_traces.png') > 0
```

## Evaluation signals

- CSV file exists at output path with correct filename and non-zero file size (>0 bytes).
- CSV file contains expected columns matching query result schema (e.g., scan number, m/z, retention time, intensity).
- Image file exists at output path with correct raster format (PNG) and non-zero file size.
- Image visualization matches tabulated data: axis ranges, plot type (e.g., line traces, heatmaps), and color scales correspond to result content.
- File timestamps and permissions confirm successful write operation (no I/O errors, writable output directory).

## Limitations

- Export assumes results fit in memory; very large result sets may require batching or chunking strategies not detailed here.
- Image format and visualization layout are determined heuristically by result structure; highly non-standard query results may produce unintuitive or unreadable plots.
- No built-in deduplication or merging of results across multiple query files; each query produces independent CSV and image outputs.
- CSV export does not preserve plot styling or color mapping; image export alone preserves full visualization fidelity.

## Evidence

- [other] MassQLab exports tabulated query results through a two-format serialization mechanism: results are saved as both images and CSV files.: "MassQLab exports tabulated query results through a two-format serialization mechanism: results are saved as both images and CSV files."
- [other] Serialize results table to CSV format using a CSV writer (e.g. pandas.DataFrame.to_csv or equivalent). Generate visualization image(s) from the tabulated results (format and plot type determined by result structure). Save visualization(s) as image file(s) (PNG or equivalent raster format).: "Serialize results table to CSV format using a CSV writer (e.g. pandas.DataFrame.to_csv or equivalent). Generate visualization image(s) from the tabulated results (format and plot type determined by"
- [readme] Results are tabulated and saved as images and csv files: "Results are tabulated and saved as images and csv files"
- [other] Verify both CSV and image files are written to the designated output directory with correct format and non-zero size.: "Verify both CSV and image files are written to the designated output directory with correct format and non-zero size."
