---
name: adduct-fragment-table-construction
description: Use when when initializing an mWISE annotation pipeline with a new or
  custom KEGG database, or when you need to reconstruct the Cpd.Add matching table
  with modified adduct/fragment specifications (e.g., subset to instrument-specific
  adducts or adjust frequency thresholds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
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
  provenance_tier: literature
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

# adduct-fragment-table-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Constructs a compound–adduct lookup table (Cpd.Add) by combining KEGG database identifiers with exact masses and adduct/fragment annotations from curated knowledge bases (CAMERA, cliqueMS, H. Tong et al.). This table enables rapid mass-to-charge ratio matching in untargeted LC-MS metabolomics annotation.

## When to use

When initializing an mWISE annotation pipeline with a new or custom KEGG database, or when you need to reconstruct the Cpd.Add matching table with modified adduct/fragment specifications (e.g., subset to instrument-specific adducts or adjust frequency thresholds). Required before the mass-matching stage.

## When NOT to use

- Input is already a complete, validated Cpd.Add table and you only need to apply filtering or matching — use the matching stage directly instead.
- You lack a curated KEGG database or adduct reference — CpdaddPreparation requires both structural and mass annotation inputs.
- Your goal is to filter or cluster features that have already been matched to m/z values — use clusterBased.filter or featuresClustering instead.

## Inputs

- KEGG database (KeggDB or sample.keggDB data frame: KEGG identifiers, exact masses)
- Info.Add reference table (adduct/fragment specifications with quasi-molecular indicators and observed frequency data)
- Optional: user-selected adduct/fragment subset (vector of adduct strings)

## Outputs

- Cpd.Add table (compound–adduct association matrix: rows = unique KEGG–adduct pairs, columns ≥ KEGG ID, adduct form, theoretical m/z, quasi-molecular flag, observed frequency)

## How to apply

Load a KEGG database (KeggDB or sample.keggDB) containing KEGG identifiers and exact masses into R. Execute the CpdaddPreparation function with adduct and fragment specifications; the default specifications are derived from CAMERA, cliqueMS, and H. Tong et al. knowledge bases and include quasi-molecular indicators and observed frequency data. Generate the output Cpd.Add table, which associates each KEGG compound with all applicable adduct/fragment forms. Optionally subset adducts or fragments before execution to match your experimental ionization mode and improve specificity. Validate table structure (row count, column presence, no null exact masses or adduct strings) and verify that quasi-molecular forms have observed frequency annotations for later filtering stages.

## Related tools

- **mWISE** (R package providing CpdaddPreparation function and default adduct/fragment specifications for Cpd.Add construction) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Source of default adduct and fragment definitions integrated into mWISE's Info.Add reference table)
- **cliqueMS** (Source of adduct/fragment knowledge and observed frequency data for Info.Add)
- **R** (Execution environment for CpdaddPreparation and table validation)
- **KEGG database** (Source of compound identifiers and exact masses for Cpd.Add rows)

## Examples

```
data("KeggDB"); data("Info.Add"); Cpd.Add <- CpdaddPreparation(keggdb=KeggDB, Info.Add=Info.Add)
```

## Evaluation signals

- Cpd.Add table row count ≥ source KEGG compound count (due to one-to-many compound-to-adduct mapping); typically 3–8× larger.
- All rows have non-null KEGG identifier, exact mass (numeric), and adduct form (string); no missing or malformed values.
- Quasi-molecular forms (e.g., [M+H]+, [M-H]−) have observed frequency annotations in [0, 1] range; rare adducts should have frequency < 0.1 if user frequency filter was applied.
- Theoretical m/z values are correctly computed (exact mass ± adduct mass offset); spot-check 5–10 rows against formula.
- Table structure matches downstream matching-stage expectations: column names align with mass-matching function input schema; no unexpected duplicate KEGG–adduct pairs.

## Limitations

- Cpd.Add construction relies on the completeness and accuracy of the input KEGG database and Info.Add reference table; missing adducts or incorrect exact masses propagate to matching stage.
- Default adduct/fragment set may not reflect all instrument-specific ionization phenomena (in-source losses, multi-stage fragmentation); users must validate or subset adducts based on experimental settings.
- Observed frequency thresholds (default 0.1) are empirically derived from CliqueMS; may be suboptimal for rare metabolites or instrument-specific workflows.
- No built-in mechanism to handle post-translational modifications or non-standard adducts; construction assumes neutral KEGG structures.

## Evidence

- [intro] CpdaddPreparation constructs Cpd.Add from KEGG and adduct/fragment knowledge: "CpdaddPreparation computes the Cpd.Add table by combining KEGG database identifiers with their exact masses and adduct/fragment information from Info.Add, which includes quasi-molecular indicators"
- [intro] Default adducts derive from CAMERA, cliqueMS, H. Tong et al.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] Cpd.Add table is built from Info.Add reference: "The `Cpd.Add` table is built from the `Info.Add` table"
- [intro] Users can subset adducts/fragments for matching stage: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their"
- [intro] Frequency threshold for quasi-molecular adducts: "If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering."
