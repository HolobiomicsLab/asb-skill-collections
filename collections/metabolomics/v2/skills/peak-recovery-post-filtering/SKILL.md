---
name: peak-recovery-post-filtering
description: Use when after applying cluster-based filtering with quasi-molecular adduct constraints and frequency thresholds on LC-MS feature candidates, when some peaks have been entirely removed from the candidate pool and you want to prevent loss of true metabolites that failed to meet filtering criteria.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
  - KEGG database
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-recovery-post-filtering

## Summary

Recovery of metabolite peaks that were completely removed during cluster-based filtering in untargeted LC-MS annotation pipelines. This skill restores potentially valid candidates that may have been over-filtered, improving annotation sensitivity without sacrificing specificity.

## When to use

After applying cluster-based filtering with quasi-molecular adduct constraints and frequency thresholds on LC-MS feature candidates, when some peaks have been entirely removed from the candidate pool and you want to prevent loss of true metabolites that failed to meet filtering criteria due to experimental noise or adduct rarity.

## When NOT to use

- Input is a raw untargeted LC-MS feature table that has not yet undergone cluster-based filtering — apply clustering and filtering first.
- Your filtering criteria (quasi-molecular adducts, frequency threshold) are already conservative or lenient enough that no peaks warrant recovery — inspect the rate of removal before deciding.
- Downstream analysis requires strict control over false positive rate — recovered peaks have lower confidence and may introduce spurious annotations if not re-ranked with network diffusion.

## Inputs

- filtered cluster table (output from clusterBased.filter with removed peaks marked or excluded)
- original feature table with mass-to-charge ratios and intensities
- KEGG candidate match table from matching stage
- cluster membership assignments

## Outputs

- augmented candidate table with recovered peaks re-integrated
- updated cluster-based candidate list ready for diffusion prioritization

## How to apply

Following the clusterBased.filter step in the mWISE.annotation workflow, apply the recoveringPeaks function to restore peaks that were completely removed by the preceding filtering stage. The function takes the filtered cluster output and re-integrates peaks based on their original mass-to-charge ratio matching to KEGG, without re-applying the stringent quasi-molecular adduct or frequency thresholds. This two-stage approach balances computational efficiency (aggressive filtering removes noise early) with recall (recovery ensures rare but genuine metabolites are not discarded). The recovered peaks are then passed to the diffusion prioritization stage where they compete fairly for ranking alongside surviving candidates.

## Related tools

- **mWISE** (provides the recoveringPeaks function and orchestrates the full annotation pipeline including clustering, filtering, and recovery stages) — https://dev.b2s.club/b2slab/mWISE
- **R** (runtime environment for executing recoveringPeaks and integrating with clusterBased.filter and diffusion.input functions)
- **KEGG database** (source of reference mass values and metabolite identifiers for matching recovered peaks)

## Examples

```
recovered_candidates <- recoveringPeaks(filtered.clusters = cluster.output, original.features = feature.table, kegg.matches = kegg.candidates)
```

## Evaluation signals

- Number of recovered peaks is > 0 and ≤ total number of removed peaks (no phantom recovery)
- Each recovered peak has a valid mass-to-charge ratio match to KEGG within the specified tolerance used in the matching stage
- Recovered peaks appear in the final ranked results after diffusion prioritization with computed diffusion scores
- Performance metrics (precision, recall, F1-score) computed via performanceEvaluation against df.Ref benchmark show improved or maintained recall without degradation of precision
- Recovered peaks retain cluster membership information and intensity values consistent with the original feature table

## Limitations

- Recovery is unconditional — all removed peaks are restored without stratification by confidence or reason for removal, potentially re-introducing low-quality candidates.
- Effectiveness depends on having informative downstream prioritization (network diffusion); without it, recovered peaks may rank arbitrarily.
- The skill does not distinguish between peaks removed due to low frequency (rare adducts, true metabolites) versus peaks removed due to noise; both are equally restored.
- Recovery does not restore peaks lost in earlier stages (e.g., quality filtering before clustering); only peaks removed by clusterBased.filter are recovered.

## Evidence

- [intro] The recoveringPeaks function recovers the peaks that have been completely removed by the cluster-based filter.: "The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter."
- [intro] Clustering and filtering stage follows matching to remove low-confidence candidates before prioritization.: "clustering and filtering the potential KEGG candidates"
- [intro] Diffusion prioritization uses recovered peaks after recovery, applying network-based scoring.: "building a final prioritized list using diffusion in networks"
- [intro] Cluster-based filtering uses quasi-molecular adducts and frequency thresholds to remove candidates.: "If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering."
