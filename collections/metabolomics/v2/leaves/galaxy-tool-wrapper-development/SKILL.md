---
name: galaxy-tool-wrapper-development
description: Use when you have a working R package that performs established preprocessing,
  analysis, or statistical workflows on formatted tabular data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - Galaxy
  - ionflow
  - ionflow (IonFlow R package)
  - planemo
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-021-01841-z
  title: IonFlow
evidence_spans:
- based on the modification of R package
- Galaxy tool for processing and analysis
- github.com__wanchanglin__ionflow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ionflow_cq
    doi: 10.1007/s11306-021-01841-z
    title: IonFlow
  dedup_kept_from: coll_ionflow_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-021-01841-z
  all_source_dois:
  - 10.1007/s11306-021-01841-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# galaxy-tool-wrapper-development

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Wrapping a specialized R package as a Galaxy tool exposes domain-specific analysis functionality (e.g., ionomics data processing) to Galaxy's workflow and interface layer, enabling reproducible, parameterized execution within a standardized bioinformatics platform.

## When to use

You have a working R package that performs established preprocessing, analysis, or statistical workflows on formatted tabular data (e.g., ion concentrations, metabolite abundances), and you want to integrate it into Galaxy so that non-expert users can invoke it via GUI, batch it in workflows, and track provenance. Use this skill when the R package source is stable, documented, and requires parameter exposure (e.g., outlier thresholds, batch correction method, output options).

## When NOT to use

- The R package has complex external dependencies (e.g., Python, compiled C libraries, network access) that cannot be containerized or declared in Galaxy tool_conf.xml — consider a Docker or Conda wrapper instead.
- The R package output format is non-deterministic, binary, or undocumented — Galaxy tools require precise output schema declaration.
- The package is under active development with frequent breaking API changes — wait for stable release or major version number.

## Inputs

- R package source code (from canonical repository, e.g., GitHub)
- Representative test datasets in Galaxy-compatible tabular format (e.g., ion concentration matrices with sample identifiers and batch labels)
- Parameter specifications (outlier detection thresholds, batch correction method, output options)

## Outputs

- Galaxy tool XML wrapper file (e.g., ionflow.xml)
- Test data directory for Galaxy validation
- Validated, executable Galaxy tool registered in tool_conf.xml or Galaxy Tool Shed

## How to apply

Clone or obtain the source R package (e.g., from GitHub). Create a Galaxy tool XML wrapper that declares input ports (data formats, sample metadata, control parameters), command-line invocation of the R package functions, and output file declarations. Map Galaxy data types (e.g., tabular ionomics datasets with ion columns and replicate rows) to R function arguments via the XML port bindings. Test the wrapper locally using representative ionomics or metabolomics datasets to verify that parameter passing, function execution, and output file generation succeed. Validate wrapper syntax and Galaxy compliance using planemo lint and the Galaxy test harness. Once validated, register the tool in Galaxy's tool_conf.xml or contribute to the Galaxy Tool Shed for centralized discovery.

## Related tools

- **R** (Core execution engine; the wrapped package is invoked via R command-line with arguments passed from Galaxy XML port bindings)
- **Galaxy** (Platform and interface layer that exposes the R tool as a GUI component, workflow node, and traceable job; manages parameter validation and data routing) — https://github.com/galaxyproject/galaxy
- **ionflow (IonFlow R package)** (Domain-specific package providing preprocessing (outlier detection, batch correction), exploratory analysis, clustering, and network analysis on ionomics data) — https://github.com/AlinaPeluso/MetaboFlow
- **planemo** (Galaxy tool development and testing utility; used to lint XML syntax and run automated test harness against wrapper)

## Examples

```
devtools::install_github("AlinaPeluso/MetaboFlow", subdir="IonFlow"); library(IonFlow); pre_proc <- PreProcessing(data=IonData, stdev=pre_defined_sd)
```

## Evaluation signals

- planemo lint returns no errors or only acceptable warnings (e.g., unused input fields)
- Test harness executes the wrapped tool against representative ionomics data (e.g., yeast ion concentrations from 1454 knockouts) and produces output files matching expected schema (e.g., cleaned dataset, outlier statistics table)
- Parameter passing verified: outlier thresholds (e.g., Q1 − 3×IQ, Q3 + 3×IQ) and batch correction method (e.g., median-centering on log-scale) produce deterministic, reproducible results across repeated invocations
- Output file format matches Galaxy data type declaration (e.g., tabular output matches Galaxy's 'tabular' or 'csv' type); file headers and column order are stable
- Galaxy GUI renders all declared input ports correctly, with appropriate validation messages for invalid parameters (e.g., negative thresholds)

## Limitations

- No changelog available in the source repository — breaking changes or deprecated functions may not be documented; test new versions thoroughly before deployment.
- Complex R package dependencies may require system-level libraries that are difficult to containerize or isolate in shared Galaxy environments.
- Large ionomics datasets (thousands of samples, 14+ ion species) may exceed Galaxy's default timeout or memory constraints; consider job resource requests in the XML wrapper.
- Galaxy tool wrappers expose only command-line parameters; advanced R package functionality (e.g., interactive visualization, dynamic parameter discovery) may not be fully representable in XML.

## Evidence

- [intro] IonFlow is a Galaxy tool for processing and analysis of ionomics data: "Galaxy tool for processing and analysis of ionomics data"
- [readme] The wrapper is based on modification of the IonFlow R package: "Galaxy tool for processing and analysis of ionomics data , based on the modification of R package IonFlow"
- [other] Define Galaxy tool XML specifying input parameters, R command invocation, and output declarations: "Define the Galaxy tool XML wrapper specifying input parameters (data formats, analysis options), command-line invocation of R and the ionflow package functions, and output file declarations."
- [other] Map Galaxy data types to R function arguments: "Implement input/output port bindings in the XML to map Galaxy data types (e.g., tabular ionomics datasets) to R function arguments."
- [other] Validation uses planemo lint and Galaxy test harness: "Validate wrapper syntax and Galaxy compliance using planemo lint and test harness."
- [readme] Preprocessing section receives raw ion concentration data and produces cleaned dataset: "The pre-processing section is required first as it produces in output the cleaned dataset to be used in the other sections."
