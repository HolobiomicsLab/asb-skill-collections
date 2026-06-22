---
name: ceramide-name-standardization-with-regex
description: Use when when downloading a lipidomics dataset from Metabolomics Workbench (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - lipidr
  - R
  - Metabolomics Workbench API
  - R (base regex functions)
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
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

# ceramide-name-standardization-with-regex

## Summary

Recover and standardize unparsed Ceramide lipid names from public lipidomics studies by applying regular expression pattern matching to rename full chemical names into the supported 'Cer (' naming convention, enabling successful parsing into LipidomicsExperiment objects.

## When to use

When downloading a lipidomics dataset from Metabolomics Workbench (e.g., via fetch_mw_study()) and the resulting LipidomicsExperiment object contains parsing warnings indicating that Ceramide molecules were not parsed because their names do not follow supported patterns—typically when Ceramide molecules are written with full chemical names rather than the abbreviated 'Cer (' convention.

## When NOT to use

- Ceramide molecules are already named using the supported 'Cer (' convention—apply this skill only when parsing warnings indicate non-standard names.
- The input dataset contains no Ceramide molecules or all lipids have already been successfully parsed.
- The data source uses a different naming standard for lipids that should not be overwritten (e.g., vendor-specific or publication-specific nomenclature that is intentionally preserved).

## Inputs

- LipidomicsExperiment object with unparsed Ceramide molecules
- Metabolomics Workbench study data (study_id, e.g., ST001111)

## Outputs

- LipidomicsExperiment object with standardized Ceramide lipid names
- Updated molecule name mappings following 'Cer (' naming convention

## How to apply

After loading the dataset into a LipidomicsExperiment object, examine parsing warnings to identify unparsed molecules. Use a regular expression pattern to target Ceramide entries: substitute the initial portion of the full chemical name (matched by the pattern '^.* \(') with 'Cer (' to standardize the naming. This converts names like 'long-chain-base ceramide (d18:1/20:0)' into 'Cer (d18:1/20:0)', which matches the supported naming schema. Apply the rename operation directly to the molecule names in the experiment object. Verify success by confirming that all previously unparsed Ceramide molecules now parse without warnings.

## Related tools

- **lipidr** (R package for loading and parsing lipidomics datasets into LipidomicsExperiment objects; provides the container data structure and parsing infrastructure upon which molecule name standardization is applied) — https://github.com/ahmohamed/lipidr
- **Metabolomics Workbench API** (Public data repository and API endpoint for fetching raw lipidomics studies (via lipidr's fetch_mw_study() function) that may contain non-standard Ceramide nomenclature)
- **R (base regex functions)** (Provides grep, gsub, and string manipulation functions to implement the regular expression pattern substitution on molecule names)

## Examples

```
library(lipidr); d <- fetch_mw_study('ST001111'); d_corrected <- d; rownames(d_corrected) <- gsub('^.* \\(', 'Cer (', rownames(d_corrected))
```

## Evaluation signals

- No parsing warnings are raised when the LipidomicsExperiment object is re-parsed or validated after name standardization.
- All Ceramide molecule names in the resulting object follow the 'Cer (' pattern (e.g., 'Cer (d18:1/20:0)') and can be recognized by the lipidr parser.
- The count of successfully parsed molecules increases after regex substitution, corresponding to the number of previously unparsed Ceramide entries.
- Manual spot-check of renamed molecules confirms 1:1 mapping between original full chemical names and standardized 'Cer (' names with no data loss or corruption.
- Downstream differential expression and multivariate analysis workflows (e.g., PCA, de_analysis) execute without errors related to unparsed lipid names.

## Limitations

- The regex pattern '^.* \(' assumes all unparsed Ceramide molecules follow a consistent full-name structure with a consistent prefix and parenthetical suffix; highly irregular naming schemes may require manual curation or alternative patterns.
- This approach standardizes nomenclature but does not validate chemical accuracy of the resulting 'Cer (' names; if the underlying full chemical name is ambiguous or incorrect, the standardized name may also be incorrect.
- The skill is specific to Ceramide molecules; other unparsed lipid classes (e.g., phosphatidylcholines, triglycerides) with non-standard names require separate handling or additional regex patterns.
- Applying regex substitution to all molecule names indiscriminately without examining context may corrupt intentionally non-standard names or multi-lipid entries; inspection of parsing warnings and manual validation of at least a sample of renamed molecules is recommended.

## Evidence

- [other] Can unparsed Ceramide molecules from study ST001111 be successfully recovered and renamed using RegEx pattern matching to follow the supported 'Cer (' naming convention?: "Can unparsed Ceramide molecules from study ST001111 be successfully recovered and renamed using RegEx pattern matching to follow the supported 'Cer (' naming convention?"
- [other] Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all previously unparsed molecules.: "Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all"
- [other] Call fetch_mw_study('ST001111') to download and retrieve the study data from Metabolomics Workbench API.: "Call fetch_mw_study('ST001111') to download and retrieve the study data from Metabolomics Workbench API."
- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
- [intro] We can examine these molecules, remove them from the dataset or change their names, if desired.: "We can examine these molecules, remove them from the dataset or change their names, if desired."
