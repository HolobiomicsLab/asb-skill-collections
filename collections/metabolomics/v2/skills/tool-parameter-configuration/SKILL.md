---
name: tool-parameter-configuration
description: Use when you have selected a specific SECIMTools module (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Galaxy Genomics Framework
  - SECIMTools suite
derived_from:
- doi: 10.1186/s12859-018-2134-1
  title: SECIMTools
evidence_spans:
- can be run in a standalone mode or via Galaxy Genomics Framework
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_secimtools_cq
    doi: 10.1186/s12859-018-2134-1
    title: SECIMTools
  dedup_kept_from: coll_secimtools_cq
schema_version: 0.2.0
---

# tool-parameter-configuration

## Summary

Configure and invoke SECIMTools metabolomics processing tools in standalone mode by specifying required arguments and parameters according to tool-specific documentation. This skill bridges the gap between selecting a tool and executing it with correct input–parameter bindings to produce validated metabolomics output artifacts.

## When to use

You have selected a specific SECIMTools module (e.g., normalization, quality-control, or feature-filtering) and possess metabolomics input data in the format required by that tool (feature table, sample metadata), but need to determine how to pass arguments, set parameters, and validate execution in standalone command-line mode rather than through Galaxy.

## When NOT to use

- You are running SECIMTools through Galaxy Genomics Framework (the framework handles parameter binding and invocation automatically).
- Input data is already in a downstream format or has already been processed by the target tool (avoid redundant re-processing).
- Tool documentation or parameter schema is unavailable or ambiguous, making it unsafe to guess argument values.

## Inputs

- Metabolomics feature table (abundance matrix with samples × features)
- Sample metadata file (annotations, covariates, batch information)
- Tool-specific parameter specification (documentation, config file, or CLI arguments)

## Outputs

- Processed metabolomics data artifact (normalized, filtered, or quality-controlled feature table)
- Tool-specific output files (plots, statistics, intermediate matrices)
- Execution log or validation report

## How to apply

Obtain the SECIMTools repository and identify the target tool's documentation to determine required arguments (input file paths, output destination) and optional parameters specific to the analysis (e.g., normalization method, filtering thresholds). Prepare metabolomics input data in the format specified by the tool (commonly feature abundance tables and sample metadata files). Construct the command-line invocation by passing all required arguments and tuning parameters as documented. Execute the tool and verify that output artifacts are produced in the expected format and directory. Cross-check output schema, row/column counts, and numeric ranges against tool documentation to confirm correct parameter application.

## Related tools

- **SECIMTools suite** (Collection of standalone and Galaxy-wrapped tools for metabolomics data processing (normalization, QC, feature selection, statistical analysis, classification).) — github.com/secimTools/SECIMTools
- **Galaxy Genomics Framework** (Alternative execution environment for SECIMTools; provides graphical parameter configuration and workflow composition as alternative to standalone CLI.)

## Evaluation signals

- Output file exists at the specified path and is readable in the documented format.
- Output artifact schema matches tool documentation (e.g., row/column headers, data types, numeric ranges).
- Row and feature counts in output correspond to input and expected filtering/normalization behavior.
- Numeric values (e.g., normalized abundance, quality metrics) fall within biologically plausible or documented ranges.
- Tool execution completes without error messages and returns a zero exit code.

## Limitations

- SECIMTools are primarily designed for metabolomics data; applicability to other omics domains is not discussed.
- Standalone mode requires manual parameter specification; Galaxy integration provides a graphical interface that may reduce configuration errors.
- No changelog is available in the repository, making it difficult to track parameter changes or backward compatibility across versions.

## Evidence

- [readme] SECIMTools project aims to develop a suite of tools for processing of metabolomics data, which can be run in a standalone mode or via Galaxy Genomics Framework.: "which can be run in a standalone mode or via Galaxy Genomics Framework"
- [other] Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented.: "Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented"
- [other] Validate that the output artifact is produced in the expected format and location.: "Validate that the output artifact is produced in the expected format and location"
- [readme] The suite includes a comprehensive set of quality control metrics (retention time window evaluation and various peak evaluation tools), visualization techniques (hierarchical cluster heatmap, principal component analysis, linear discriminant analysis, modular modularity clustering), basic statistical analysis methods (partial least squares - discriminant analysis, analysis of variance), advanced classification methods (random forest, support vector machines), and advanced variable selection tools (least absolute shrinkage and selection operator LASSO and Elastic Net).: "comprehensive set of quality control metrics... visualization techniques... statistical analysis methods... advanced classification methods... variable selection tools"
