---
name: metabolite-mass-lookup-preparation
description: Use when when beginning an untargeted LC-MS annotation workflow, before attempting to match experimental m/z peaks to metabolite identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - KEGG database
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
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
---

# metabolite-mass-lookup-preparation

## Summary

Build a compound–adduct lookup table (Cpd.Add) by combining KEGG database exact masses with adduct and fragment knowledge, enabling subsequent mass-to-charge ratio matching in untargeted LC-MS annotation. This is the prerequisite data structure for the matching stage of the mWISE workflow.

## When to use

When beginning an untargeted LC-MS annotation workflow, before attempting to match experimental m/z peaks to metabolite identities. Specifically required when you have raw LC-MS peak data with mass-to-charge ratios and need to map them to known compounds in KEGG, accounting for the fact that observed peaks may represent different adduct or fragment forms of the same compound.

## When NOT to use

- You have already constructed or imported a pre-built Cpd.Add table and simply need to apply it for matching.
- Your metabolites of interest are not present in the KEGG database or you are using a custom metabolite database without adduct/fragment annotations.
- You are only interested in targeted analysis of known compounds with fixed adduct forms, not in comprehensive untargeted LC-MS annotation.

## Inputs

- KEGG database (KeggDB or sample.keggDB) — data frame with KEGG identifiers and exact masses
- Info.Add table — adduct/fragment specifications with quasi-molecular indicators and observed frequency data

## Outputs

- Cpd.Add table — compound–adduct lookup table with KEGG identifiers, exact masses, adduct forms, and quasi-molecular indicators

## How to apply

Load a KEGG database (KeggDB or sample.keggDB) containing KEGG identifiers and their exact masses into R. Execute the CpdaddPreparation function with the default adduct and fragment specifications derived from CAMERA, cliqueMS, and H. Tong et al. knowledge bases (or optionally a curated subset if you have domain expertise about your experimental ionization mode and settings). The function combines each KEGG compound's exact mass with the Info.Add table, which contains quasi-molecular indicators and observed frequency data, producing a data frame where each row represents a unique compound–adduct pair. Validate the resulting Cpd.Add table by checking that all expected adducts are present, that frequencies match your ionization method, and that no duplicate or malformed entries exist before proceeding to the matching stage.

## Related tools

- **mWISE** (R package containing the CpdaddPreparation function and the entire annotation workflow) — https://dev.b2s.club/b2slab/mWISE
- **KEGG database** (Source of compound identifiers and exact masses for lookup table construction)
- **CAMERA** (Provides default adduct and fragment specifications for table construction)
- **cliqueMS** (Contributes adduct/fragment knowledge and observed frequency data to Info.Add)
- **R** (Runtime environment for executing CpdaddPreparation and manipulating the Cpd.Add table)

## Examples

```
data("KeggDB"); data("Info.Add"); Cpd.Add <- CpdaddPreparation(KeggDB, Info.Add)
```

## Evaluation signals

- The Cpd.Add table contains no duplicate compound–adduct pairs and all rows have valid KEGG identifiers, exact mass values, and adduct annotations.
- All expected quasi-molecular adducts (e.g., [M+H]+, [M+Na]+, [M−H]−) are represented with correct mass offsets relative to the parent compound mass.
- Observed frequency values for adducts are consistent with the experimental ionization mode (positive or negative) and match the knowledge base ranges cited (e.g., frequency > 0.1 for commonly observed adducts).
- The table structure matches the mWISE schema expected by downstream functions (featuresClustering, clusterBased.filter, diffusion.input).
- Row count and unique adduct diversity scale appropriately with the input KEGG database size (no unexpected collapse or explosion of rows).

## Limitations

- Cpd.Add construction relies entirely on the completeness and accuracy of the input KEGG database; if a compound or its exact mass is absent or incorrect, no matching will recover it.
- The default adduct/fragment specifications are derived from general knowledge bases (CAMERA, cliqueMS) and may not capture rare or method-specific adducts; users should curate or subset the Info.Add table if their experimental settings differ (e.g., specialized ESI or APCI modes).
- Observed frequency thresholds (default > 0.1) are statistical and may exclude rare but genuine adducts in niche metabolomes; filtering threshold is user-modifiable but requires domain expertise to optimize.
- The lookup table is static once constructed; it does not adapt or retrain based on actual peak detection results and must be regenerated if KEGG is updated or adduct knowledge changes.

## Evidence

- [other] CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add, which includes quasi-molecular indicators and observed frequency data from CliqueMS: "CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add, which includes quasi-molecular indicators"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] data frame containing KEGG identifiers and their exact masses: "a data frame containing KEGG identifiers and their exact masses"
- [intro] The Cpd.Add table is built from the Info.Add table: "The `Cpd.Add` table is built from the `Info.Add` table"
- [intro] matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments: "matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments"
