---
name: tool-parameter-specification-and-validation
description: Use when you have a working R package (e.g., IonFlow for ionomics data analysis) that performs well in standalone R environments, but need to expose it as a reusable Galaxy tool so that non-expert users can invoke it without writing R code, while preserving parameter semantics and validating input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0091
  tools:
  - R
  - ionflow
  - Galaxy
  - ionflow (IonFlow R package)
  - planemo
derived_from:
- doi: 10.1007/s11306-021-01841-z
  title: IonFlow
evidence_spans:
- based on the modification of R package
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
---

# Tool Parameter Specification and Validation

## Summary

Define and validate input/output parameter mappings between a domain-specific R package and a Galaxy tool wrapper via XML schema, ensuring correct type coercion, parameter passing, and compliance with Galaxy execution standards. This skill bridges package APIs and workflow systems by translating R function signatures into Galaxy-compatible declarative tool definitions.

## When to use

You have a working R package (e.g., IonFlow for ionomics data analysis) that performs well in standalone R environments, but need to expose it as a reusable Galaxy tool so that non-expert users can invoke it without writing R code, while preserving parameter semantics and validating input data types (e.g., tabular ionomics datasets with specific column structures and measurement units).

## When NOT to use

- The R package already has an official Galaxy wrapper in the Galaxy Tool Shed; use the existing tool instead of recreating it.
- Input data is not tabular or does not conform to the package's expected structure (e.g., raw spectral data that requires upstream preprocessing outside the package's scope).
- The R package has undocumented or highly variable parameter semantics that cannot be reliably exposed as fixed Galaxy input ports without manual user intervention.

## Inputs

- R package source code (e.g., IonFlow R package from github.com/AlinaPeluso/MetaboFlow)
- Galaxy XML tool template (or starter template)
- Representative test datasets (e.g., ion concentration tables in tabular format with replicates, batch identifiers, and known outliers)
- R function signature and argument documentation

## Outputs

- Galaxy tool XML wrapper (.xml file) with input/output port declarations and command-line invocation
- Test harness outputs (e.g., planemo test results, validation logs)
- Validated Galaxy tool ready for deployment in Galaxy tool_conf.xml

## How to apply

Create a Galaxy tool XML wrapper that declares input ports (mapping Galaxy data types such as tabular or csv to R function arguments), command-line invocation (e.g., `Rscript` with package function calls), and output file declarations. Bind Galaxy data types to R function parameters by specifying format converters and argument position; for ionomics workflows, map tabular ion-concentration inputs to data frame arguments. Test the wrapper locally against the R package using representative test datasets (e.g., ICP-MS ion concentration tables with known outliers and batch effects) to verify parameter passing, function execution, and output file generation. Validate wrapper syntax and Galaxy compliance using `planemo lint` and run test harnesses to confirm input/output round-trip integrity and absence of type coercion errors.

## Related tools

- **R** (Execution engine for package functions invoked by the Galaxy tool wrapper via command-line Rscript)
- **Galaxy** (Workflow platform that executes the tool wrapper and manages input/output data types and staging) — https://github.com/galaxyproject/galaxy
- **ionflow (IonFlow R package)** (Domain-specific package whose functions are wrapped and invoked for ionomics data processing) — https://github.com/AlinaPeluso/MetaboFlow
- **planemo** (Linting and testing harness to validate Galaxy tool XML syntax and compliance)

## Examples

```
devtools::install_github("AlinaPeluso/MetaboFlow", subdir="IonFlow"); library(IonFlow); pre_proc <- PreProcessing(data=IonData, stdev=pre_defined_sd)
```

## Evaluation signals

- planemo lint reports no schema violations or critical errors in the Galaxy tool XML wrapper
- Test harness successfully executes the wrapped tool against representative ionomics datasets (e.g., ion concentration tables with 1454 samples and 14 ion species) and produces output files with expected structure and statistics
- Parameter values and data types are correctly passed from Galaxy inputs to R function arguments, verified by comparing R standalone execution output with Galaxy wrapper output (bit-level or statistical equivalence)
- Output files conform to expected Galaxy data types (e.g., tabular format with proper headers) and contain no null or truncated values
- Tool wrapper can be successfully registered in Galaxy tool_conf.xml and appears in the Galaxy UI without runtime errors

## Limitations

- No changelog found in the ionflow repository, making it difficult to track breaking changes or parameter evolution between versions.
- The wrapper assumes the R package is correctly installed in the Galaxy environment; dependency management and R library versions are not automatically validated by the wrapper itself.
- Complex or conditional parameter dependencies (e.g., 'if mode=A then parameter X is required') are not easily expressed in declarative Galaxy XML and may require Galaxy conditional workflows or custom validation logic.
- Large ionomics datasets may encounter Galaxy resource limits (memory, execution timeout) depending on cluster configuration; the wrapper does not automatically tune R memory or parallelization parameters.

## Evidence

- [other] Define the Galaxy tool XML wrapper specifying input parameters (data formats, analysis options), command-line invocation of R and the ionflow package functions, and output file declarations.: "Define the Galaxy tool XML wrapper specifying input parameters (data formats, analysis options), command-line invocation of R and the ionflow package functions, and output file declarations."
- [other] Implement input/output port bindings in the XML to map Galaxy data types (e.g., tabular ionomics datasets) to R function arguments.: "Implement input/output port bindings in the XML to map Galaxy data types (e.g., tabular ionomics datasets) to R function arguments."
- [other] Test the wrapper locally against the IonFlow R package with representative ionomics datasets to verify parameter passing, function execution, and output file generation.: "Test the wrapper locally against the IonFlow R package with representative ionomics datasets to verify parameter passing, function execution, and output file generation."
- [other] Validate wrapper syntax and Galaxy compliance using planemo lint and test harness.: "Validate wrapper syntax and Galaxy compliance using planemo lint and test harness."
- [readme] Galaxy tool for processing and analysis of ionomics data , based on the modification of R package IonFlow: "Galaxy tool for processing and analysis of ionomics data , based on the modification of R package IonFlow"
- [readme] Add this tool's location into Galaxy' tool config file: ~/Galaxy/config/tool_conf.xml: "Add this tool's location into Galaxy' tool config file: ~/Galaxy/config/tool_conf.xml"
