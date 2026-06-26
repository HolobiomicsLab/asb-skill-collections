---
name: clustered-peak-output-formatting
description: Use when after peak clustering has been completed in pyINETA (i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - PyINETA
  - Python
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
- pyINETA is a Python package
- python run_pyineta.py <options>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03966
  all_source_dois:
  - 10.1021/acs.analchem.4c03966
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# clustered-peak-output-formatting

## Summary

Export clustered peak networks from pyINETA's clustering module into formats compatible with downstream metabolite matching and database lookup. This skill standardizes peak-to-cluster assignments and metadata for seamless integration with the matching and finding modules.

## When to use

After peak clustering has been completed in pyINETA (i.e., after peaks have been grouped into networks based on spectral similarity and co-occurrence patterns) and you need to prepare the clustered data for matching against a simulated INADEQUATE metabolite database or other downstream analysis steps.

## When NOT to use

- Peak clustering has not yet been performed; use peak picking output directly instead.
- Peaks have not been grouped into networks; output formatting assumes valid cluster assignments exist.
- You intend to perform further clustering refinement; export only after final clustering decisions are made.

## Inputs

- Clustered peak assignments (peak identifiers with cluster membership labels)
- Peak attributes from clustering output (chemical shifts, intensities, co-occurrence patterns)
- Peak-to-cluster mapping data structure from pyINETA.clustering module

## Outputs

- Formatted peak-cluster mapping file (e.g., CSV with peak ID, cluster ID, and peak attributes)
- Clustered peak data compatible with pyINETA matching module input format
- Cluster network metadata documentation

## How to apply

After applying pyINETA's clustering algorithm to group picked peaks into networks, generate a mapping file that documents peak-to-cluster assignments, with each peak assigned a unique cluster identifier. Export the clustered peak data in a structured format (e.g., CSV or tabular format compatible with pyINETA's matching module input specification) that preserves peak attributes (chemical shifts, intensities, cluster membership) and maintains the data schema required by downstream modules. Validate that all peaks from the input clustering step appear in the output and that cluster identifiers are consistent and traceable. The export format must be compatible with the matching module's input interface to ensure uninterrupted workflow execution.

## Related tools

- **PyINETA** (Source framework providing clustering module (pyineta.clustering) and matching module input specification for formatted output) — https://github.com/edisonomics/PyINETA
- **Python** (Implementation language for data serialization, format conversion, and output file generation)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s cluster -o output_folder
```

## Evaluation signals

- All peaks from the clustering input appear in the output mapping with valid cluster identifiers and no missing entries.
- Cluster identifiers are unique, consistent, and traceable across the output file.
- Peak attributes (chemical shifts, intensities) are preserved and match the input values from the clustering module.
- Output file format matches the input schema expected by the pyINETA matching module (e.g., column names, data types, delimiters).
- Downstream matching module accepts the formatted output without schema validation errors.

## Limitations

- Output format is specific to pyINETA's matching module specification; reformatting may be required for use with external matching tools.
- No changelog or versioning guidance is provided; format compatibility across pyINETA versions is not documented.
- The skill assumes clustering has already assigned cluster identifiers; malformed or missing cluster assignments will propagate to the output.

## Evidence

- [other] Export the clustered peak data in a format compatible with downstream matching and finding modules.: "Export the clustered peak data in a format compatible with downstream matching and finding modules."
- [other] Assign each peak a cluster identifier and generate a mapping file documenting peak-to-cluster assignments.: "Assign each peak a cluster identifier and generate a mapping file documenting peak-to-cluster assignments."
- [readme] It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra.: "filter these picked peaks to identify networks of peaks (ideally) coming from the same compound which it then matches to a simulated INADEQUATE database"
- [other] pyINETA implements a clustering module that filters picked peaks to identify networks of peaks from the same compound, operating as a downstream step after peak picking and before matching to metabolite databases.: "clustering module that filters picked peaks to identify networks of peaks from the same compound, operating as a downstream step after peak picking and before matching"
