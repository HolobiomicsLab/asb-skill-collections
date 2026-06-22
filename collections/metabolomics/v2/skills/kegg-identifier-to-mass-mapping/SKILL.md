---
name: kegg-identifier-to-mass-mapping
description: Use when you have raw LC-MS peak intensity data with mass-to-charge ratios and need to match them to known metabolites. This skill must be applied before the matching stage if you are working with a KEGG database (KeggDB or sample.keggDB) and require a precomputed adduct/fragment lookup table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - KEGG database
  - CAMERA
  - cliqueMS
  - KEGG
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- matching mass-to-charge ratio values to KEGG database
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

# kegg-identifier-to-mass-mapping

## Summary

Build a lookup table (Cpd.Add) that associates KEGG compound identifiers with their exact masses and adduct/fragment modifications to enable mass-to-charge ratio matching in untargeted LC-MS annotation. This skill transforms static KEGG reference data into a dynamic, searchable resource indexed by observable m/z values.

## When to use

You have raw LC-MS peak intensity data with mass-to-charge ratios and need to match them to known metabolites. This skill must be applied before the matching stage if you are working with a KEGG database (KeggDB or sample.keggDB) and require a precomputed adduct/fragment lookup table. Apply this skill early in the mWISE pipeline to enable fast m/z-to-compound association without repeated computation.

## When NOT to use

- Your peak table is already annotated or you have external compound identifiers other than KEGG (use direct chemical database mapping instead).
- You are using a non-KEGG compound reference (e.g., local metabolite library, PubChem, or species-specific database — use the appropriate reference-specific preparation function).
- You have pre-existing m/z-to-compound associations and only need to filter or rank them (skip to clustering/filtering stage directly).

## Inputs

- KEGG database (KeggDB or sample.keggDB): data frame containing KEGG identifiers and exact masses
- Info.Add table: adduct/fragment specifications with quasi-molecular indicators and observed frequency data
- Optional: custom adduct/fragment subset specification (expert-tuned for specific experimental conditions)

## Outputs

- Cpd.Add table: compound–adduct associations indexed by computed m/z, ready for mass-matching queries
- Validated lookup structure suitable for downstream feature-to-compound matching

## How to apply

Load the KEGG database containing KEGG identifiers and their exact masses into R using data(KeggDB) or data(sample.keggDB). Execute the CpdaddPreparation function with default adduct and fragment specifications derived from CAMERA, cliqueMS, and H. Tong et al. knowledge bases (Info.Add table), or supply a custom adduct/fragment subset to match your experimental ionization method and instrument settings. The function combines each KEGG entry with all applicable adduct and fragment modifications, computing the resulting m/z values and storing them alongside quasi-molecular indicators and observed frequency data. Validate the resulting Cpd.Add table for completeness: verify that the number of rows equals the product of unique KEGG entries and applicable modifications, and check that m/z values are numeric and positive. This table then serves as the lookup resource for the matching stage.

## Related tools

- **mWISE** (Main R package hosting CpdaddPreparation function and the full untargeted LC-MS annotation pipeline) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Source of default adduct and fragment knowledge base used to populate Info.Add)
- **cliqueMS** (Provides adduct/fragment specifications and observed frequency data integrated into Info.Add)
- **KEGG** (Reference database providing compound identifiers and exact masses)
- **R** (Execution environment for CpdaddPreparation function and data manipulation)

## Examples

```
data("KeggDB"); data("Info.Add"); Cpd.Add <- CpdaddPreparation(kegg.database = KeggDB, info.adduct = Info.Add)
```

## Evaluation signals

- Row count of Cpd.Add equals unique KEGG entries × applicable adducts/fragments (no missing or duplicate associations)
- All m/z values in Cpd.Add are numeric, positive, and fall within expected instrument range (typically 50–1000 m/z for small molecules)
- Quasi-molecular adduct indicators match Info.Add specification (e.g., [M+H]+, [M-H]−, [M+NH4]+)
- Spot check: known metabolite KEGG IDs appear in Cpd.Add with correct exact mass ± adduct modification (e.g., glucose exact mass 180.06339 → [M+H]+ m/z 181.07065)
- Observed frequency data preserved: adducts with frequency ≥ 0.1 (or user-specified threshold) are retained; optional or rare modifications are marked appropriately

## Limitations

- CpdaddPreparation assumes KEGG database entries contain valid, non-null exact mass values; malformed or missing mass data will propagate errors into Cpd.Add.
- The skill is blind to sample-specific ionization chemistry: it relies on static Info.Add specifications. If your experimental conditions favor unexpected adducts or suppress common ones, the default lookup may have poor coverage; expert curation of the adduct subset is recommended.
- Computational cost scales with KEGG database size × adduct/fragment multiplicity; large custom databases or extended adduct lists may slow the matching stage downstream.
- In-source fragments and neutral losses are approximated using fixed rules from CAMERA, cliqueMS, and literature; unusual or compound-specific fragmentations are not captured.

## Evidence

- [other] CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add: "CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add"
- [other] Execute the CpdaddPreparation function with default adduct and fragment specifications derived from CAMERA, cliqueMS, and H. Tong et al.: "Execute the CpdaddPreparation function with default adduct and fragment specifications derived from CAMERA, cliqueMS, and H. Tong et al. knowledge bases"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] data frame containing KEGG identifiers and their exact masses: "a data frame containing KEGG identifiers and their exact masses"
- [intro] The `Cpd.Add` table is built from the `Info.Add` table: "The `Cpd.Add` table is built from the `Info.Add` table"
- [intro] matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments: "matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments"
