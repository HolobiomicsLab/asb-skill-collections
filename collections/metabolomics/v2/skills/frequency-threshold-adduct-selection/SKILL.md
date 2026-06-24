---
name: frequency-threshold-adduct-selection
description: Use when after feature clustering has grouped co-eluting features and
  assigned candidate KEGG metabolites with multiple potential adduct forms, use this
  skill when you need to reduce false positive annotations by filtering out low-frequency
  adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mWISE
  - R
  - CAMERA
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides
  tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
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

# frequency-threshold-adduct-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A filtering step that selects adducts and fragments for metabolite annotation based on observed frequency thresholds, optionally retaining quasi-molecular adducts with minimum occurrence frequency above a user-defined cutoff. This is applied during cluster-based candidate filtering to improve specificity by removing rare or low-confidence adduct assignments.

## When to use

After feature clustering has grouped co-eluting features and assigned candidate KEGG metabolites with multiple potential adduct forms, use this skill when you need to reduce false positive annotations by filtering out low-frequency adducts. Particularly useful when the experimental setup or MS ionization conditions are not a priori constrained, or when you want to let the data empirically guide adduct selection by retaining only adducts observed with frequency > 0.1 (or user-specified threshold).

## When NOT to use

- Input is already a pre-validated peak table with known adducts and ionization conditions — skip to diffusion prioritization.
- Your MS experiment used a restricted ionization protocol with predetermined adducts — provide an explicit quasi-molecular adduct list rather than relying on frequency thresholds.
- Dataset is very small (< 50 features) such that observed frequency statistics are unreliable — use domain expertise or external adduct databases instead.

## Inputs

- Annotated feature table with KEGG candidate assignments and adduct annotations (from matching stage)
- Cluster group identifiers (pcgroup column) from feature clustering output
- Optional: user-defined quasi-molecular adduct list (e.g., MH, MNa, MK)
- Optional: minimum observed frequency threshold (default 0.1)

## Outputs

- Filtered MH.Tab: feature table containing only features with quasi-molecular adducts meeting frequency threshold
- Adduct-filtered candidate annotations retaining only high-confidence molecular ion assignments

## How to apply

Apply the mWISE `clusterBased.filter` function to the annotated feature table after `featuresClustering` has produced cluster group assignments (pcgroup). By default, the filter retains quasi-molecular adducts (MH, MNa, MK, etc.) together with any other adducts exhibiting observed frequency higher than 0.1 across the dataset, unless you explicitly provide a restricted quasi-molecular adduct list. The user can modify the minimum observed frequency threshold according to their ionization efficiency expectations and noise tolerance. Features assigned to in-source fragments or adducts below the frequency cutoff are discarded, producing a filtered MH.Tab output containing only cluster-validated quasi-molecular ion candidates.

## Related tools

- **mWISE** (Provides clusterBased.filter function to apply frequency-based adduct filtering and quasi-molecular adduct retention logic) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Source of default adduct and fragment table used by mWISE, informing which ion forms are considered quasi-molecular vs. in-source)
- **R** (Execution environment for mWISE functions)

## Examples

```
mWISE::clusterBased.filter(annotated.table, pcgroup='pcgroup', min.frequency=0.1, quasi.molecular=c('MH', 'MNa', 'MK'))
```

## Evaluation signals

- Verify that output MH.Tab contains no features assigned to in-source fragments or rare adducts below the frequency threshold.
- Check that the number of candidate annotations per feature has been reduced compared to pre-filter input, indicating successful removal of low-confidence adduct assignments.
- Confirm that quasi-molecular adducts (MH, MNa, MK) are present in output even if their observed frequency equals or exceeds the threshold.
- Inspect cluster group (pcgroup) identifiers are preserved in output, confirming that filtering operated on clustered features rather than singleton features.
- Validate that adduct frequency statistics used for thresholding were computed consistently across all clusters in the dataset.

## Limitations

- Frequency-based filtering assumes that high-frequency adducts are biologically or chemically meaningful, which may not hold for ionization artifacts or matrix effects.
- Default 0.1 threshold is empirically motivated but may be too stringent for small datasets or too permissive for noisy experiments; user must validate the choice against their MS acquisition and sample complexity.
- Does not account for adduct-specific ionization efficiencies or instrumental bias; adducts with genuinely lower ionization efficiency may be incorrectly filtered out.
- Filtering is irreversible within this step; features removed cannot be recovered unless the recoveringPeaks function is later applied to restore completely removed peaks.

## Evidence

- [other] The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts, optionally using adducts with observed frequency higher than 0.1 if no specific quasi-molecular list is provided: "The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts, optionally using adducts with observed frequency higher than 0.1 if no specific"
- [other] Apply mWISE clusterBased.filter function to each cluster, retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency adducts (observed frequency ≤ 0.1 threshold): "Apply mWISE clusterBased.filter function to each cluster, retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency"
- [intro] If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering. The user can modify the minimum observed: "If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering. The user can modify the minimum observed"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS"
