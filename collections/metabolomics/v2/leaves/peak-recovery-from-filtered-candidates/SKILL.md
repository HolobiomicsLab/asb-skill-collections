---
name: peak-recovery-from-filtered-candidates
description: Use when after applying cluster-based filtering with quasi-molecular
  adducts and frequency thresholds on candidate metabolites from KEGG matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mWISE
  - R
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
- we will now use the sample graph provided by FELLA R package
- g.metab <- igraph::as.undirected(sample.graph)
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

# peak-recovery-from-filtered-candidates

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recover LC-MS peaks that were completely removed during cluster-based filtering to prevent loss of potentially valid metabolite annotations. This skill reconstructs a complete peak inventory before final diffusion-based ranking, ensuring no valid candidates are discarded by conservative filtering thresholds.

## When to use

After applying cluster-based filtering with quasi-molecular adducts and frequency thresholds on candidate metabolites from KEGG matching. Use this skill when you need to preserve annotation completeness despite aggressive filtering that may have removed entire peak features due to low observed frequency or non-standard adduct assignments.

## When NOT to use

- Input peak table is already fully annotated or contains no filtered-out features
- Filtering stage was not applied or filtering criteria retained all candidate peaks
- Recovery strategy conflicts with downstream analysis requiring strict frequency-based confidence cutoffs

## Inputs

- filtered_candidates (output from clusterBased.filter)
- original_peak_candidate_assignments (pre-filter peak–KEGG compound mappings)
- diffusion_results (output from set.diffusion with z-score normalization)

## Outputs

- recovered_peaks (reconstructed peak–compound associations)
- merged_ranked_table (diffusion-prioritized peaks plus recovered peaks, ranked by Ranked.Tab)

## How to apply

Apply the `recoveringPeaks` function to reconstruct peaks that were completely eliminated by the cluster-based filter step. This function compares the filtered candidate pool against the original unfiltered peak-candidate assignments to identify and recover removed peaks. The recovered peaks are then merged with diffusion-prioritized results by compound identifier before final ranking, ensuring that peaks removed by conservative filtering criteria (e.g., frequency thresholds below 0.1 or rare adduct forms) are restored to the annotation table. This recovery occurs after z-score normalization of diffusion scores but before the final ranking step via the `finalResults` function.

## Related tools

- **mWISE** (Provides the recoveringPeaks function to restore completely filtered peaks and finalResults function to merge recovered peaks with diffusion-ranked results) — https://dev.b2s.club/b2slab/mWISE
- **R** (Host language for executing recoveringPeaks and finalResults functions)
- **FELLA** (Provides the metabolite network graph (sample.graph) used to compute diffusion scores that are merged with recovered peaks)

## Examples

```
recoveringPeaks(filteredCandidates = clusterBased.filter(...), originalPeakTable = peakCandidates); finalResults(diffusionResults, recoveredPeaks, scores='z')
```

## Evaluation signals

- Recovered peaks are identifiable by comparing row counts: (filtered candidates + recovered peaks) ≥ (original pre-filter candidates)
- All recovered peaks have valid compound identifiers matching KEGG database entries used in diffusion input
- Merged final table contains no duplicate peak–compound pairs after recovery and diffusion merge by compound identifier
- Peaks recovered are those with low observed frequency or non-standard adducts that were excluded by clusterBased.filter thresholds but not by mass accuracy constraints
- Final Ranked.Tab output includes all recovered peaks ranked by z-score-normalized diffusion scores, with no NAs introduced by the recovery step

## Limitations

- Recovery reconstructs peaks removed by filtering but cannot restore confidence in their metabolite assignment beyond what the diffusion network provides
- Peaks with conflicting or ambiguous compound annotations may be recovered multiple times (one per compound), requiring downstream deduplication logic
- Recovery strategy assumes the original unfiltered peak–candidate assignment table is available and correctly preserved; partial or corrupted filtering history may yield incomplete recovery

## Evidence

- [intro] The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter.: "The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter."
- [intro] (4) merging the recovered peaks with diffusion results by compound identifier; and (5) building a final ranked table using `finalResults` function with z-score normalization.: "merging the recovered peaks with diffusion results by compound identifier; and (5) building a final ranked table using `finalResults` function"
- [intro] Recover peaks completely removed by cluster-based filtering using the recoveringPeaks function.: "Recover peaks completely removed by cluster-based filtering using the recoveringPeaks function."
- [intro] Compile and rank final results using the finalResults function to generate the diffusion-prioritized Ranked.Tab output.: "Compile and rank final results using the finalResults function to generate the diffusion-prioritized Ranked.Tab output."
