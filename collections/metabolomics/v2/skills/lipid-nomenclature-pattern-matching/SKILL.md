---
name: lipid-nomenclature-pattern-matching
description: Use when when loading a lipidomics dataset into lipidr and the parsing
  step generates warnings about unparsed molecules due to unsupported naming patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
  - R (base)
  - Metabolomics Workbench API
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
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

# lipid-nomenclature-pattern-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recover and standardize unparsed lipid molecule names that do not follow supported naming conventions by applying regular expression pattern matching. This skill enables successful parsing of molecules with full chemical names (e.g., Ceramides) into canonical lipidomics formats, expanding the set of analyzable lipids in a LipidomicsExperiment.

## When to use

When loading a lipidomics dataset into lipidr and the parsing step generates warnings about unparsed molecules due to unsupported naming patterns. This typically occurs with datasets from Metabolomics Workbench or similar sources where lipid names use full chemical nomenclature instead of standardized abbreviations (e.g., 'Ceramide (d18:1/16:0)' instead of 'Cer (d18:1/16:0)').

## When NOT to use

- Lipid names already follow supported abbreviation patterns (e.g., 'PC (', 'TG (', 'Cer (') — no transformation needed.
- The unparsed molecules represent genuine annotation errors or species not supported by lipidr — renaming will not resolve semantic mismatches.
- Structural information (chain lengths, unsaturation) is absent or ambiguous in the original name — pattern matching cannot reliably recover it.

## Inputs

- LipidomicsExperiment object with unparsed molecule names
- Parsing warnings indicating molecules with unsupported naming patterns
- Lipid name strings with full chemical nomenclature (e.g., 'Ceramide (d18:1/16:0)')

## Outputs

- LipidomicsExperiment object with standardized lipid names following supported conventions
- Set of successfully recovered and renamed lipid molecules
- Updated parsing status reflecting newly recognized lipids

## How to apply

After calling fetch_mw_study() or read_skyline() to load the dataset, examine parsing warnings to identify the naming pattern of unparsed molecules. Use regular expressions to match and replace the variable prefix portion while preserving the core lipid class and structural information. For Ceramides, the pattern '^.* \(' matches any initial text up to an opening parenthesis, which is then replaced with 'Cer (' to conform to the supported convention. Apply this transformation using string manipulation in R, then re-parse or validate the renamed molecules. The rationale is that the lipid structure (chain lengths, unsaturation, functional groups) is preserved in the portion after the opening parenthesis, so only the prefix nomenclature requires standardization.

## Related tools

- **lipidr** (Primary R package used to load, parse, and manage LipidomicsExperiment objects; provides the fetch_mw_study() function and parsing infrastructure.) — https://github.com/ahmohamed/lipidr
- **R (base)** (Execution environment for regex pattern matching via sub(), gsub(), or stringr functions to rename lipid molecules.)
- **Metabolomics Workbench API** (Source of lipidomics datasets (e.g., study ST001111) that may contain non-standardized lipid names requiring pattern matching.) — https://www.metabolomicsworkbench.org

## Examples

```
# After loading study ST001111 and observing parsing warnings
d <- fetch_mw_study('ST001111')
# Rename unparsed Ceramide molecules: 'Ceramide (d18:1/16:0)' → 'Cer (d18:1/16:0)'
lipid_names(d) <- sub('^.* \\(', 'Cer (', lipid_names(d))
```

## Evaluation signals

- All molecules matching the target pattern (e.g., '.*\(') are successfully renamed to the canonical form (e.g., 'Cer (') without data loss.
- The renamed LipidomicsExperiment object contains no parsing warnings for the previously unparsed molecules.
- Structural information (e.g., chain lengths, unsaturation) in the portion after '(' is preserved identically before and after renaming.
- Downstream analyses (PCA, differential expression, enrichment) run without errors using the newly standardized molecule names.
- The number of recognized lipid molecules increases and the number of unparsed molecules decreases after applying the pattern-matching transformation.

## Limitations

- Regular expression patterns must be carefully tailored to each non-standard naming convention; a single pattern may not capture all variants (e.g., spacing, punctuation differences).
- Pattern matching relies on the assumption that the chemical structure is encoded consistently in the portion after the opening parenthesis; if structure notation itself varies, additional transformations may be required.
- Molecules with missing or incomplete structural information (e.g., 'Ceramide' without chain specification) cannot be reliably recovered by this approach alone.
- The skill does not validate whether renamed molecules are chemically or biologically plausible — only that they conform to the naming convention.

## Evidence

- [other] Can unparsed Ceramide molecules from study ST001111 be successfully recovered and renamed using RegEx pattern matching to follow the supported 'Cer (' naming convention?: "Can unparsed Ceramide molecules from study ST001111 be successfully recovered and renamed using RegEx pattern matching to follow the supported 'Cer (' naming convention?"
- [other] Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all previously unparsed molecules.: "Ceramide molecules written with full chemical names can be recovered by substituting the initial portion with 'Cer' using the RegEx pattern '^.* \(' to '(Cer (', enabling successful parsing of all"
- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
- [intro] We can examine these molecules, remove them from the dataset or change their names, if desired.: "We can examine these molecules, remove them from the dataset or change their names, if desired."
- [intro] Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id.: "Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id."
