---
name: feature-metadata-annotation
description: Use when you have processed mass spectrometry data consisting of three separate tables (quantification features, sample metadata, and spectral annotations) and need to combine them into a single, queryable artifact that preserves relationships between features, samples, and their chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3382
  tools:
  - msFeaST
  - jupyter-notebook
  - msFeaST Dashboard bundle
derived_from:
- doi: 10.1093/bioinformatics/btae584
  title: msFeaST
evidence_spans:
- github.com__kevinmildau__msFeaST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msfeast_cq
    doi: 10.1093/bioinformatics/btae584
    title: msFeaST
  dedup_kept_from: coll_msfeast_cq
schema_version: 0.2.0
---

# feature-metadata-annotation

## Summary

Integrate quantification tables, metadata tables, and spectral data into a unified JSON schema for interactive mass spectrometry feature exploration. This skill bridges raw multi-modal mass spec outputs into a format suitable for browser-based visualization and downstream statistical analysis.

## When to use

You have processed mass spectrometry data consisting of three separate tables (quantification features, sample metadata, and spectral annotations) and need to combine them into a single, queryable artifact that preserves relationships between features, samples, and their chemical properties for interactive exploration or statistical workflows.

## When NOT to use

- Input quantification table is already in JSON format or pre-processed into a single combined object.
- Spectral data is unavailable or only MS1 precursor m/z is known without fragmentation spectra.
- Sample metadata cannot be reliably linked to quantification table rows by sample identifier.

## Inputs

- Quantification table (TSV/CSV: features × samples with abundance values)
- Metadata table (TSV/CSV: samples × descriptors with treatment, batch, and replicate information)
- Spectral data (mzML or equivalent format containing MS1 and MS/MS spectra with m/z and retention time)

## Outputs

- dashboard_data.json (JSON text file with feature, metadata, and spectral annotations in unified schema)
- Interactive visualization artifact compatible with msFeaST Dashboard bundle

## How to apply

Execute the msfeast_pipeline Jupyter notebook with your quantification table (feature abundances × samples), metadata table (sample descriptors), and spectral data (m/z, retention time, MS/MS spectra) as inputs. The pipeline processes these three sources to produce a JSON text file conforming to the dashboard data schema, which embeds feature identifiers, sample annotations, and spectral metadata in a hierarchical structure. Validate that the generated JSON contains all required fields: feature-level data (m/z, RT, spectral references), sample-level metadata (treatment, batch, replicate), and abundance values. The output JSON is then loadable into the msFeaST Dashboard bundle for interactive visualization or can be parsed programmatically for downstream analysis.

## Related tools

- **msFeaST** (Python module that executes data integration pipeline to unify quantification, metadata, and spectral tables into JSON schema) — https://github.com/kevinmildau/msFeaST
- **jupyter-notebook** (Interactive environment hosting msfeast_pipeline_mushroom_type_comparison.ipynb for running feature-metadata integration with user-defined file paths)
- **msFeaST Dashboard bundle** (Browser-based visualization tool (HTML/JavaScript) that loads and renders the output JSON for interactive feature exploration) — https://github.com/kevinmildau/msFeaST

## Examples

```
conda activate msfeast_environment; jupyter-notebook; # then open msfeast_pipeline_mushroom_type_comparison.ipynb, update data filepaths to your quantification_table.csv, metadata_table.csv, spectral_data.mzML, and execute all cells to generate dashboard_data.json
```

## Evaluation signals

- Generated JSON parses without errors and can be loaded into msFeaST Dashboard bundle without schema validation failures.
- JSON structure contains all three data layers: feature identifiers with m/z and retention time, sample metadata fields, and quantification abundance values accessible by feature and sample keys.
- Row/column counts in JSON match input quantification table dimensions (n features × m samples) with no data loss or duplication.
- Dashboard dataview tab successfully displays loaded data with searchable features, filterable metadata, and interactive spectral visualization.
- Spot-check: manual verification that 3–5 randomly selected features have correct abundance values, metadata linkages, and associated spectral annotations from input sources.

## Limitations

- msFeaST pre-processing and pipeline workflow has been tested on macOS and Linux; Windows support is currently being worked on.
- R installation within conda environment may experience path caching issues if rscript is invoked before conda R installation; workaround requires terminal closure and re-activation of the conda environment.
- Interactive dashboard requires a desktop web browser (Firefox, Chrome, Edge, Safari); mobile or headless environments are not supported.
- Spectral data must be in mzML format or compatible mass spec output; other formats require pre-conversion.
- No changelog is available; undocumented schema changes between versions may cause backward compatibility issues with older dashboard_data.json files.

## Evidence

- [readme] quantification table, metadata table, and spectral data processing: "complete example of quantification table, metadata table, and spectral data processing"
- [other] JSON schema validation and dashboard loading: "Validate that the generated JSON contains required fields for interactive visualization and can be loaded in the msFeaST Dashboard bundle."
- [readme] pipeline output format: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard"
- [readme] three-table integration workflow: "download the *msFeaST_Dashboard_bundle.html* and the ready made data from notebooks\data\omsw_pleurotus_ms2deepscore\dashboard_data.json"
- [readme] user parameterization for custom data: "To make use of your own data, change the data filepath arguments to your own data file location and run the pipeline."
