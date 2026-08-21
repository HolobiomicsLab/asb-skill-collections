---
name: ionization-mode-merging-and-reconciliation
description: Use when you have acquired MS-DIAL peak lists in both positive and negative
  ionization modes on the same sample set and want to consolidate detected features
  across modes to avoid reporting duplicate annotations for the same molecule.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - MS-CleanR
  - MS-DIAL
  - MS-FINDER
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ionization-mode-merging-and-reconciliation

## Summary

This skill merges feature clusters derived from positive ionization mode (PI) and negative ionization mode (NI) LC-MS acquisitions into a unified feature space, enabling detection of the same molecular entity across both modes. It is applied during the feature clustering phase of untargeted metabolomics workflows to reduce redundancy and improve annotation consistency.

## When to use

Apply this skill when you have acquired MS-DIAL peak lists in both positive and negative ionization modes on the same sample set and want to consolidate detected features across modes to avoid reporting duplicate annotations for the same molecule. This is optional but recommended when both PI and NI modes are present in the input data.

## When NOT to use

- Single ionization mode acquisition (PI or NI only) — merging is unnecessary and the optional step should be skipped.
- Data acquired in MS1-only mode without MS/MS fragmentation spectra — MS-CleanR will crash before reaching the clustering step.
- Features already pre-merged or deduplicated by external means prior to MS-CleanR import.

## Inputs

- MS-DIAL peak list (post-generic filtering) in positive ionization mode with m/z, retention time, and peak intensity
- MS-DIAL peak list (post-generic filtering) in negative ionization mode with m/z, retention time, and peak intensity
- Feature clusters derived from MS-DIAL peak character estimation algorithm for each mode

## Outputs

- Unified feature table with merged cluster IDs spanning both ionization modes
- Feature cluster membership annotations reconciled across PI and NI
- Consolidated feature list ready for parental signal extraction and MS-FINDER export

## How to apply

After MS-DIAL peak character estimation has generated separate feature clusters for each ionization mode, optionally invoke the mode-merging step in MS-CleanR to reconcile PI and NI clusters. The algorithm identifies features with similar m/z and retention time across modes and assigns them to unified cluster IDs. The decision to merge should be informed by the expected adduct mass shifts (typically +1.008 Da for protonated PI species vs. −1.008 Da for deprotonated NI species) and retention time tolerance (typically ±0.2–0.5 min). Merging is performed before parental signal extraction; features successfully merged receive consolidated cluster membership. The output is a single feature table with cluster IDs that reflect both ionization modes, reducing false duplicate annotations in downstream MS-FINDER in silico annotation.

## Related tools

- **MS-DIAL** (Peak detection, feature clustering via peak character estimation algorithm, and ionization mode separation prior to merging) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Implements optional PI/NI mode merging during feature clustering step using multi-level optimization of modularity algorithm) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-FINDER** (Receives merged and consolidated feature list for in silico annotation using hydrogen rearrangement rules scoring) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Cluster ID consistency: all features with the same molecular m/z (±0.005 Da) and similar retention time (±0.5 min) across PI and NI should be assigned the same cluster ID post-merge.
- No duplicate annotations in final MS-FINDER output: features post-merge should not yield redundant identifications of the same molecule under different ionization adducts.
- Cluster count reduction: total number of clusters in merged table should be less than or equal to the sum of separate PI and NI cluster counts, reflecting successful consolidation.
- Feature count preservation: total number of features should remain unchanged; merging reconciles cluster membership, not feature counts.
- Adduct mass shift validation: features merged across modes should exhibit m/z differences consistent with expected adduct shifts (e.g., [M+H]+ vs. [M−H]−).

## Limitations

- Merging requires at least both PI and NI mode data; single-mode acquisitions derive no benefit.
- Feature matching across modes relies on retention time precision; isomeric or co-eluting features may be incorrectly merged if retention time tolerance is too permissive.
- MS-CleanR requires all input features to contain MS/MS spectra (DDA or DIA mode); MS1-only data will cause the pipeline to crash before clustering is attempted.
- Known bug in R > 4.2: 'Error: the condition has length > 1' may occur during downstream database annotation merging step; workaround requires R ≤ 4.2.
- No changelog or version history provided; active development ceased in favor of MS-DIAL 5.x integration, so support for future LC-MS workflows may be limited.

## Evidence

- [readme] Optionally, MS-CleanR can merge PI and NI mode during this step: "Optionally, MS-CleanR can merge PI and NI mode during this step"
- [readme] feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [readme] MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis (DDA) or data independent analysis (DIA) using either positive ionization mode (PI) or negative ionization mode (NI) or both: "MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis (DDA) or data independent analysis (DIA) using either positive ionization mode (PI) or negative ionization mode (NI) or"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained.: "Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained."
