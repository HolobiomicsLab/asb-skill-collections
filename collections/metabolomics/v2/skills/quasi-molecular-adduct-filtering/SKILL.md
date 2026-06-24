---
name: quasi-molecular-adduct-filtering
description: Use when after feature clustering has been applied to co-eluting LC-MS
  features and mass-to-charge ratio matching to KEGG has produced an annotated table
  with adduct assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
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
- we will now use the sample graph provided by FELLA R package
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

# quasi-molecular-adduct-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter LC-MS feature candidates to retain only quasi-molecular ion adducts (e.g., MH, MNa, MK) after feature clustering, removing in-source fragments and low-frequency adducts. This step reduces annotation candidate noise and improves specificity before diffusion-based prioritization.

## When to use

After feature clustering has been applied to co-eluting LC-MS features and mass-to-charge ratio matching to KEGG has produced an annotated table with adduct assignments. Use this skill when you need to focus on biologically plausible quasi-molecular ions and eliminate spurious in-source fragments or rare adducts that are unlikely to represent the true metabolite.

## When NOT to use

- Features have not yet been clustered — cluster-based filtering requires pcgroup assignments from featuresClustering.
- You need to retain all candidate adducts (including fragments) for separate analysis — this skill explicitly removes them.
- Input is already a final ranked annotation table — filtering should occur earlier in the pipeline, before diffusion prioritization.

## Inputs

- annotated feature table with KEGG candidates and adduct assignments (from matching stage)
- cluster group identifiers (pcgroup column, from featuresClustering output)
- quasi-molecular adduct list (optional; defaults to MH, MNa, MK if not supplied)
- observed adduct frequency threshold (default 0.1)

## Outputs

- filtered annotation table (MH.Tab) containing only quasi-molecular ion candidates
- cluster-validated feature annotations with spurious in-source fragments removed

## How to apply

Apply the mWISE clusterBased.filter function to the annotated feature table containing cluster group identifiers (pcgroup) and adduct assignments. Retain only candidates with quasi-molecular adducts (MH, MNa, MK, etc.); if no explicit quasi-molecular list is provided, the function defaults to these adducts plus any adducts with observed frequency > 0.1 (this threshold can be modified). The function processes each cluster independently, filtering out in-source fragments and low-frequency adducts (observed frequency ≤ 0.1) to produce a cleaned MH.Tab output table. This filtered table then serves as input to diffusion-based prioritization, ensuring that downstream scoring focuses on metabolically relevant ion species.

## Related tools

- **mWISE** (Provides clusterBased.filter function to filter candidates by quasi-molecular adducts and frequency thresholds; provides featuresClustering function that generates input pcgroup assignments) — https://dev.b2s.club/b2slab/mWISE
- **R** (Execution environment for mWISE functions)
- **CAMERA** (Source of default adduct and fragment information used to build adduct tables in mWISE)
- **cliqueMS** (Contributes to default adduct and fragment reference tables used for classification)

## Examples

```
MH.Tab <- clusterBased.filter(annotated_table, pcgroup_col="pcgroup", quasi_molecular_list=c("MH", "MNa", "MK"), freq_threshold=0.1)
```

## Evaluation signals

- Output table contains only candidates with quasi-molecular adduct labels (MH, MNa, MK, etc.) — no in-source fragments or other adduct types remain.
- Adduct frequency distribution in output shows all retained adducts have observed frequency > 0.1 (or user-specified threshold).
- Number of rows in filtered table is less than or equal to the input annotated table (filtering removes or consolidates candidates).
- Cluster group (pcgroup) assignments are preserved in output and align with input feature clusters.
- Downstream diffusion prioritization produces valid probability/network scores without missing-value errors, confirming input structure is correct.

## Limitations

- Default observed frequency threshold (0.1) may not be optimal for all ionization modes or instrument configurations; users should validate or adjust based on their experimental design.
- Filtering removes potentially informative fragment ions; if fragment-level analysis is needed, it must be performed on unfiltered data before this step.
- Assumes accurate prior clustering and mass-to-charge matching; errors in earlier stages (e.g., wrong pcgroup assignments, mismatched masses) propagate through filtering.
- Relies on accurate adduct annotation in the input table; if input adduct labels are misclassified, filtering will not recover them.

## Evidence

- [intro] The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts: "The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts"
- [intro] retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency adducts: "retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency adducts (observed frequency ≤ 0.1 threshold)"
- [intro] If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering: "If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering"
- [intro] Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity. Merge the resulting cluster group (pcgroup) identifiers into the annotated table: "Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity. Merge the resulting cluster group (pcgroup) identifiers into the"
- [intro] Output the filtered table containing only cluster-validated quasi-molecular ion candidates: "Output the filtered table containing only cluster-validated quasi-molecular ion candidates"
