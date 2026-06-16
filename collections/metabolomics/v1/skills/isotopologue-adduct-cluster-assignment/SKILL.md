---
name: isotopologue-adduct-cluster-assignment
description: Use when after sample alignment and peak picking have produced an aligned feature table with m/z and retention time coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW grouping module
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# isotopologue-adduct-cluster-assignment

## Summary

Groups detected LC-MS features into isotopologue and adduct clusters by clustering features that share the same molecular ion and mass differences corresponding to isotopic shifts (C13, N15, D) or common adduct transformations ([M+H]+, [M+Na]+, [M+NH4]+). This step operates after peak picking and sample alignment to consolidate redundant feature representations into molecular equivalence classes.

## When to use

After sample alignment and peak picking have produced an aligned feature table with m/z and retention time coordinates. Use this skill when your untargeted LC-MS workflow requires deconvolution of isotope and adduct variants into single molecular entities for downstream annotation and quantification. Essential when downstream analysis (e.g., gap-filling, MS2 consolidation) expects non-redundant feature lists.

## When NOT to use

- Input is already a consolidated feature table with isotopologues and adducts pre-grouped
- Analysis requires retention of all adduct and isotope variants separately (e.g., for adduct-specific quantification or ion suppression studies)
- Data are profile-mode (non-centroided) mzML; SLAW requires centroided input and will skip processing

## Inputs

- aligned feature table (m/z × retention time matrix from sample alignment step)
- feature coordinates (m/z and RT values for detected peaks)
- mass tolerance parameters (ppm or Da) for isotope/adduct matching

## Outputs

- grouped feature table with isotopologue/adduct cluster identifiers
- cluster membership assignments mapping features to canonical molecular ions
- cluster statistics (size, mass differences, RT variance)

## How to apply

Load the aligned feature table output from the sample alignment step, which contains m/z and retention time coordinates for all detected peaks. Apply a clustering algorithm that identifies features differing by isotopic mass shifts (e.g., 1.003 Da for C13, 0.997 Da for N15) or adduct mass differences (e.g., 21.98 Da for [M+H]+ to [M+Na]+, 18.03 Da for [M+H]+ to [M+NH4]+). Assign cluster identifiers to group features by molecular ion identity, accounting for typical mass tolerance windows used in the alignment step. Output a grouped feature table with isotopologue/adduct cluster membership annotations. Verification relies on inspecting cluster sizes, mass difference distributions within clusters, and retention time clustering (isotopologues and adducts must co-elute).

## Related tools

- **SLAW grouping module** (Performs isotopologue and adduct clustering as a dedicated processing step within the complete SLAW workflow) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm whose output (aligned features) feeds into the grouping module) — https://github.com/zamboni-lab/SLAW

## Evaluation signals

- All features within a cluster have co-eluting retention times (RT variance < alignment tolerance)
- Mass differences within clusters match expected isotopic shifts (C13 = 1.003 Da, N15 = 0.997 Da) or adduct transformations ([M+H]+ to [M+Na]+ = +21.98 Da)
- Cluster size distribution is reasonable (no artificially large clusters combining unrelated ions)
- Post-grouping feature count is lower than pre-grouping (redundancy removed)
- Gap-filling and downstream MS2 consolidation steps execute successfully without mass/RT mismatches

## Limitations

- Requires centroided mzML input; profile-mode data will cause skip or failure
- Accuracy depends on mass tolerance and alignment precision from preceding steps; poor alignment propagates into incorrect cluster assignments
- Does not disambiguate between isotopologues and isobaric adducts with identical mass differences; retention time overlap is assumed to break ties
- Performance scales with feature table size; processing thousands of samples with SLAW requires automated parameter optimization enabled

## Evidence

- [other] SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment.: "SLAW includes a processing step for grouping of isotopologues and adducts as part of its complete untargeted LC-MS workflow, which operates after peak picking and sample alignment."
- [other] Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct transformations (e.g., [M+H]+, [M+Na]+, [M+NH4]+).: "Apply isotopologue and adduct grouping algorithm to cluster features sharing the same molecular ion with mass differences corresponding to isotopic shifts (e.g., C13, N15, D) or common adduct"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
