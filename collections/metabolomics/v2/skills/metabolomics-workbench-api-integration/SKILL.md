---
name: metabolomics-workbench-api-integration
description: Use when when you need to analyze a publicly archived lipidomics study (identified by study_id like ST001111) and want to bypass manual data download and format conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - Metabolomics Workbench API
  - R
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- Through integration with Metabolomics Workbench API, `lipidr` allows users, to quickly explore public lipidomics experiments.
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-workbench-api-integration

## Summary

Retrieve and parse public lipidomics datasets directly from Metabolomics Workbench into a structured LipidomicsExperiment object using the lipidr R package's API integration. This skill enables rapid access to standardized lipidomics data without manual download and reformatting.

## When to use

When you need to analyze a publicly archived lipidomics study (identified by study_id like ST001111) and want to bypass manual data download and format conversion. Use this when your input is a Metabolomics Workbench study identifier and your goal is to load the data into R for downstream quality control, differential analysis, or multivariate modeling.

## When NOT to use

- Your data is already in a local file format (CSV, Skyline export) — use read.csv() or read_skyline() instead
- You have already downloaded and locally stored the raw Metabolomics Workbench data — load it directly with file I/O functions
- Your study is not publicly archived in Metabolomics Workbench — this skill requires API access to a registered study

## Inputs

- Metabolomics Workbench study_id string (e.g., 'ST001111')
- Internet connection to Metabolomics Workbench API

## Outputs

- LipidomicsExperiment object containing parsed lipid abundances and sample metadata
- Parsing warnings listing unparsed molecule names and their counts

## How to apply

Call lipidr's fetch_mw_study(study_id) function with the target Metabolomics Workbench study identifier to download and automatically parse the dataset into a LipidomicsExperiment object. Examine parsing warnings to identify molecules with unsupported naming patterns (e.g., full chemical names for Ceramides). For unparsed molecules, apply regex-based renaming to convert full names to the supported 'Cer (' convention using pattern substitution (e.g., '^.* \(' to '(Cer ('). Verify successful parsing by checking that all molecule names follow supported lipid class naming conventions before proceeding to quality control and analysis steps.

## Related tools

- **lipidr** (R package providing fetch_mw_study() function for API integration and LipidomicsExperiment object creation) — https://github.com/ahmohamed/lipidr
- **Metabolomics Workbench API** (Remote API service hosting public lipidomics datasets indexed by study_id) — https://www.metabolomicsworkbench.org
- **R** (Runtime environment for executing lipidr functions and regex-based molecule name standardization)

## Examples

```
d <- fetch_mw_study('ST001111'); d
```

## Evaluation signals

- LipidomicsExperiment object is successfully created with non-zero dimensions (lipids × samples)
- Sample metadata (e.g., SampleType, Cancer Stage, Race) are present in the colData slot
- All molecule names conform to supported lipid naming patterns; parsing warning count is zero or only includes expected non-recoverable entries
- Lipid abundance matrix contains numeric values (typically Areas or peak intensities) with no missing values in the primary measure column
- Row and column names match the expected study layout (lipid names as rows, sample identifiers as columns)

## Limitations

- Skill depends on the study being publicly registered in Metabolomics Workbench; private or embargoed studies cannot be accessed via API
- Molecules with non-standard naming conventions (e.g., full chemical nomenclature) will fail to parse unless manually renamed post-fetch
- Large studies may require substantial memory and network bandwidth; no automatic chunking or streaming is documented
- API availability and response time are external to the lipidr package and may vary

## Evidence

- [readme] Through integration with Metabolomics Workbench API, lipidr allows users, to quickly explore public lipidomics experiments.: "Through integration with Metabolomics Workbench API, lipidr allows users, to quickly explore public lipidomics experiments."
- [intro] Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id.: "Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id."
- [other] Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all previously unparsed molecules.: "Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all"
- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
- [intro] We can examine these molecules, remove them from the dataset or change their names, if desired.: "We can examine these molecules, remove them from the dataset or change their names, if desired."
