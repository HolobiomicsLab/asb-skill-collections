---
name: lc-ms-mass-matching-reference-building
description: Use when at the start of an untargeted LC-MS annotation pipeline when
  you have a KEGG database with exact masses and need to prepare a mass-matching reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - KEGG database
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides
  tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA
  R package
- The default table of adducts and fragments is built using information from CAMERA
  R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lc-ms-mass-matching-reference-building

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build a compound–adduct lookup table (Cpd.Add) by combining KEGG database exact masses with curated adduct/fragment specifications to enable downstream mass-to-charge ratio matching in untargeted LC-MS metabolomics. This reference table serves as the foundation for matching observed m/z peaks to candidate metabolites.

## When to use

Apply this skill at the start of an untargeted LC-MS annotation pipeline when you have a KEGG database with exact masses and need to prepare a mass-matching reference. Use it before the matching stage if you are working with peak-intensity tables from LC-MS and require context-based annotation of m/z values to known compounds.

## When NOT to use

- If your input is already a feature table or extracted m/z peak list without KEGG identifiers — skip to the matching stage instead.
- If you lack a KEGG database or equivalent compound structure reference with exact masses.
- If you are performing targeted or MRM-based analysis with a predefined list of transitions — this skill is for untargeted discovery.

## Inputs

- KEGG database (KeggDB data frame with KEGG identifiers and exact masses)
- Info.Add table (adduct and fragment specifications with quasi-molecular indicators and frequency data)
- Experimental metadata (ionization mode, adduct preferences)

## Outputs

- Cpd.Add table (compound–adduct lookup table with m/z candidates)
- Validated reference structure for downstream mass-matching

## How to apply

Load the KEGG database (KeggDB or sample.keggDB) containing KEGG identifiers and exact masses into R. Execute the CpdaddPreparation function with adduct and fragment specifications derived from CAMERA, cliqueMS, and H. Tong et al. knowledge bases (or accept defaults). The function combines KEGG identifiers with their exact masses and Info.Add table entries, which include quasi-molecular indicators and observed frequency data from CliqueMS. The result is a Cpd.Add lookup table indexed by compound–adduct pairs. Validate table structure and completeness before proceeding to the mass-matching stage. Optionally subset adducts or fragments based on your experimental settings (ionization mode, solvent, instrument) to improve accuracy.

## Related tools

- **mWISE** (R package containing CpdaddPreparation function and default adduct/fragment tables for Cpd.Add construction) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Source of default adduct and fragment specifications integrated into mWISE Info.Add)
- **cliqueMS** (Source of adduct/fragment knowledge and observed frequency data used in Cpd.Add construction)
- **KEGG database** (Supplies compound identifiers and exact masses as primary reference data)
- **R** (Execution environment for mWISE and CpdaddPreparation function)

## Examples

```
data("KeggDB"); data("Info.Add"); Cpd.Add <- CpdaddPreparation(KeggDB = KeggDB, Info.Add = Info.Add)
```

## Evaluation signals

- Cpd.Add table structure validates: contains compound–adduct pairs with corresponding m/z candidates, quasi-molecular indicators, and observed frequency values.
- No missing or null entries in critical columns (KEGG identifiers, exact masses, adduct types).
- Frequency thresholds are applied consistently (e.g., minimum observed frequency > 0.1 for non-quasi-molecular adducts).
- Downstream mass-matching stage successfully matches observed m/z peaks to Cpd.Add rows within the expected mass tolerance (e.g., 5 ppm or instrument-specific accuracy).
- Row count and diversity of Cpd.Add reflect expected compound coverage — significant under-representation may indicate KEGG subset or adduct configuration error.

## Limitations

- Cpd.Add construction depends on completeness and accuracy of the input KEGG database; missing or misannotated compounds will not be matched.
- Adduct/fragment selection must align with experimental ionization mode and matrix; using inappropriate defaults can reduce sensitivity or introduce false positives.
- Observed frequency thresholds from CliqueMS may not generalize across different sample types or instrument platforms; users should validate or customize for their context.
- The table does not account for post-ionization modifications (e.g., oxidation, methylation) unless explicitly added to Info.Add; scope is limited to KEGG-defined compounds and common adducts.

## Evidence

- [intro] CpdaddPreparation combines KEGG database identifiers and exact masses with Info.Add to build Cpd.Add: "CpdaddPreparation function builds the Cpd.Add table from a KEGG database and adduct/fragment knowledge to enable mass-to-charge ratio matching"
- [intro] Adduct/fragment specifications derive from CAMERA, cliqueMS, and H. Tong et al.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] Info.Add includes quasi-molecular indicators and observed frequency data from CliqueMS: "CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add, which includes quasi-molecular indicators"
- [intro] Subset selection of adducts/fragments is recommended based on experimental settings: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their"
- [intro] Cluster-based filtering uses quasi-molecular adducts and frequency thresholds: "the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering"
- [intro] mWISE integrates matching as the first of three main annotation steps: "mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database"
