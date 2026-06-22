---
name: workflow-pipeline-execution-validation
description: Use when you have prepared metabolomics input files (feature quantification table, MS/MS spectra in MGF format, sample metadata) and are about to execute the TIMA taxonomically informed annotation pipeline, or after pipeline execution to verify all outputs were generated correctly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - R
  - tima R package
  - SIRIUS
  - GNPS-FBMN
  - LOTUS database
  - Docker (adafede/tima-r image)
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fpls.2019.01329
  all_source_dois:
  - 10.3389/fpls.2019.01329
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-pipeline-execution-validation

## Summary

Validate input data files and confirm successful execution of a complete metabolomics annotation pipeline by checking intermediate and final outputs against expected structure and content. This skill ensures early detection of data issues and proper workflow completion before downstream analysis.

## When to use

Apply this skill when you have prepared metabolomics input files (feature quantification table, MS/MS spectra in MGF format, sample metadata) and are about to execute the TIMA taxonomically informed annotation pipeline, or after pipeline execution to verify all outputs were generated correctly.

## When NOT to use

- Input data is already in annotated metabolite format (not a raw feature table)
- MS/MS spectra file is missing or empty (.mgf contains no spectra records)
- Sample metadata does not link to organism taxonomy information (single organism analysis may proceed, but organism annotation will be limited)

## Inputs

- Feature quantification table (.csv/.tsv with feature ID, retention time, m/z, sample intensity columns)
- MS/MS spectra file (.mgf format with fragment spectra)
- Sample metadata (.csv/.tsv linking samples to organisms)
- Optional: SIRIUS annotations (.zip v5/v6), GNPS-FBMN results, custom spectral libraries

## Outputs

- Validated input report (spectra counts, feature counts, metadata consistency)
- Intermediate annotation outputs (SIRIUS results, spectral library matches, organism-specific assignments)
- Final annotation table with metabolite identities and confidence metrics
- Workflow execution log and intermediate data artifacts

## How to apply

First, validate input files using the validate_inputs() function to check MGF spectra counts, feature table structure (presence of feature ID, retention time, m/z, and sample intensity columns), and metadata consistency before launching the pipeline. Then execute the canonical tima workflow pipeline via the Shiny GUI (tima::run_app()) or programmatically, specifying customizable column names and file paths. Finally, confirm workflow completion by verifying that all intermediate annotation outputs (SIRIUS results, GNPS-FBMN matches, spectral library matches) and final annotation tables are present with expected structure, non-empty content, and consistent feature identifiers across all outputs.

## Related tools

- **tima R package** (Executes taxonomically informed metabolite annotation pipeline with integrated spectral, chemical, and taxonomic knowledge) — https://github.com/taxonomicallyinformedannotation/tima
- **SIRIUS** (Provides optional external metabolite structure predictions (v5/v6) that are integrated into annotation workflow)
- **GNPS-FBMN** (Provides optional spectral networking results that can be imported for annotation validation)
- **LOTUS database** (Default structure-organism pairs library (>650k pairs) used for organism-aware metabolite annotation) — https://lotusnprod.github.io/lotus-manuscript/
- **Docker (adafede/tima-r image)** (Containerized execution environment with all dependencies pre-installed for reproducible pipeline execution) — https://hub.docker.com/r/adafede/tima-r/

## Examples

```
tima::validate_inputs(features="data/source/example_features.csv", spectra="data/source/example_spectra.mgf", metadata="data/source/example_metadata.tsv", feature_col="row ID", filename_col="filename", organism_col="ATTRIBUTE_species"); tima::run_app()
```

## Evaluation signals

- validate_inputs() reports zero missing or malformed columns in feature table and spectra counts match non-zero value
- All intermediate output files present in expected directory structure with timestamps matching pipeline execution start time
- Final annotation table contains same number of features as input feature table with all feature IDs preserved
- No empty annotation records; each feature has at least one assigned structure candidate or metabolite identifier
- Metadata cross-reference integrity: all sample IDs in final output correspond to input metadata file and organism taxonomies are correctly assigned

## Limitations

- Package lifecycle is experimental; changelog is not available per README, indicating potential API instability
- Workflow performance depends heavily on LOTUS database coverage for target organisms; organisms with sparse natural product data will yield lower annotation confidence
- Optional SIRIUS integration requires separate installation and licensing considerations (v5/v6 specified); workflow proceeds without it but with reduced structure prediction accuracy
- Column names must be customizable through Shiny app or YAML/CLI parameters; incorrect column name mapping will cause silent validation failures

## Evidence

- [readme] Workflow validation methodology: "**Start by validating your input files** to catch issues early and save debugging time"
- [readme] Feature table schema requirements: "Must contain: feature ID, retention time, m/z, and sample intensity columns"
- [readme] Validation function implementation: "validate_inputs() will: Count spectra in MGF files, Count features and check required columns, Check metadata file consistency"
- [other] Pipeline execution workflow completion criteria: "Validate workflow completion by confirming all intermediate and final annotation outputs are generated with expected structure and content"
- [readme] LOTUS as default resource: "**Structure-organism pairs library** - We provide **LOTUS** (>650k pairs) as default"
