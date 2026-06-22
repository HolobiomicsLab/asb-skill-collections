---
name: json-schema-validation-for-dashboard
description: Use when after running the msfeast_pipeline notebook to generate dashboard_data.json from quantification tables, metadata, and spectral data. Use this skill to verify that the exported JSON contains all required fields and structure before attempting to load the file into msFeaST_Dashboard_bundle.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - msFeaST
  - msFeaST_Dashboard_bundle.html
  - msfeast_pipeline notebook
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae584
  all_source_dois:
  - 10.1093/bioinformatics/btae584
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-schema-validation-for-dashboard

## Summary

Validate that a JSON output file from mass spectrometry data processing conforms to the msFeaST dashboard data schema before loading it into the interactive visualization interface. This skill ensures data integrity and compatibility with the web-based exploration tool.

## When to use

After running the msfeast_pipeline notebook to generate dashboard_data.json from quantification tables, metadata, and spectral data. Use this skill to verify that the exported JSON contains all required fields and structure before attempting to load the file into msFeaST_Dashboard_bundle.html for interactive exploration.

## When NOT to use

- Input JSON file was not produced by the msfeast_pipeline notebook — use source validation instead.
- Dashboard bundle has not been downloaded yet — validation requires the schema definition embedded in msFeaST_Dashboard_bundle.html.
- Raw spectral data or quantification tables are being validated — this skill applies only to the aggregated JSON dashboard output, not intermediate data sources.

## Inputs

- dashboard_data.json (JSON text file output from msfeast_pipeline notebook)
- msFeaST dashboard schema (implicit specification embedded in dashboard bundle)

## Outputs

- Validation report (pass/fail status indicating schema conformance)
- Error log if schema violations are detected

## How to apply

Load the generated dashboard_data.json file and validate it against the msFeaST dashboard schema by checking for required fields and data types needed for interactive visualization. The validation confirms that the JSON structure can be successfully parsed by the dashboard bundle. This is a gate before visualization: if validation fails, the pipeline output is malformed or incomplete, and the dashboard will fail to load the data. Check that all metadata arrays, spectral features, and quantification values are present and correctly formatted. The validation is performed implicitly when attempting to load the data into the HTML dashboard via the 'select and load' interface — if the file does not conform to the schema, the dashboard will reject it or fail silently.

## Related tools

- **msFeaST_Dashboard_bundle.html** (Interactive dashboard that loads and validates the JSON file on import; acts as the execution environment where schema conformance is enforced) — github.com/kevinmildau/msFeaST
- **msfeast_pipeline notebook** (Generates the dashboard_data.json file that is validated by this skill) — github.com/kevinmildau/msFeaST

## Evaluation signals

- The dashboard successfully parses and loads the JSON file without errors or silent failures.
- All required fields for interactive visualization are present in the JSON structure.
- The data appears correctly in the dataview tab after loading, with no missing metadata, spectral features, or quantification values.
- No console errors or warnings are thrown by the dashboard bundle when the JSON is loaded.
- The JSON file size and structure match expected output from the pipeline (quantification table, metadata table, and spectral data integrated).

## Limitations

- Schema validation is implicit and occurs only when attempting to load the file into the dashboard bundle; no standalone validator tool is mentioned in the documentation.
- Error messages from the dashboard are not detailed — schema violations may be reported generically without specific field-level diagnostics.
- Schema definition is embedded in the HTML bundle and is not exposed as a separate, machine-readable artifact for external validation.
- Windows support for the msFeaST pipeline is still being worked on, which may affect reproducibility of the JSON output on that platform.

## Evidence

- [other] Validate that the generated JSON contains required fields for interactive visualization and can be loaded in the msFeaST Dashboard bundle.: "Validate that the generated JSON contains required fields for interactive visualization and can be loaded in the msFeaST Dashboard bundle."
- [readme] The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard.: "The jupyter-notebook pipeline produces the a text file in json format that can be interactively explored in the interactive dashboard."
- [readme] Open the html bundle in your browser and load the select and load the data. Changing to the dataview tab shows the now loaded data.: "Open the html bundle in your browser and load the select and load the data. Changing to the dataview tab shows the now loaded data."
- [readme] These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST.: "These notebooks contain a complete example of quantification table, metadata table, and spectral data processing required for msFeaST."
