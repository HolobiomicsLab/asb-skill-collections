---
name: ms-dial-peak-character-estimation
description: Use when you have a filtered MS-DIAL peak list (post-generic filtering,
  containing m/z, retention time, and peak intensity metrics for each feature) and
  need to group features into clusters that represent true metabolite signals rather
  than instrumental or chemical artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MS-DIAL v4.00 or higher
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- Needs MS-DIAL (v4.00 or higher)
- Needs MS-DIAL (v4.00 or higher) ... MS-CleanR use as input MS-DIAL peak list processed
  in data dependent analysis (DDA) or data independent analysis (DIA)
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

# ms-dial-peak-character-estimation

## Summary

Applies the MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties, enabling network-based clustering of LC-MS features prior to parental signal extraction. This skill is essential for reducing feature redundancy in untargeted metabolomics workflows by grouping adducts, isotopes, and in-source fragments into coherent clusters.

## When to use

Apply this skill when you have a filtered MS-DIAL peak list (post-generic filtering, containing m/z, retention time, and peak intensity metrics for each feature) and need to group features into clusters that represent true metabolite signals rather than instrumental or chemical artifacts. Use it as the bridge between initial feature filtering and parental signal extraction in MS-CleanR pipelines.

## When NOT to use

- Input lacks MS/MS data or contains MS1-only acquisitions (MS-CleanR requires DDA or DIA modes with fragment spectra)
- Features have not undergone generic filtering (blank subtraction, background removal, mass defect filtering) — clustering assumes clean input
- Peak list comes from a different tool or format not compatible with MS-DIAL peak character descriptors

## Inputs

- Filtered MS-DIAL peak list (post-generic filtering) in MS-DIAL format
- Peak-level data: m/z, retention time, peak intensity metrics
- MS-DIAL peak character descriptors (peak shape, chromatographic properties)
- Sample metadata indicating ionization mode (PI, NI, or both)

## Outputs

- Feature similarity network (graph structure with features as nodes, similarity scores as edge weights)
- Feature cluster assignments (cluster IDs mapped to all features)
- Clustered feature table with cluster membership annotations
- Optional merged PI/NI cluster assignments

## How to apply

Load the filtered MS-DIAL peak list output from the generic filtering step. Apply the MS-DIAL peak character estimation algorithm to compute pairwise feature similarity based on peak shape properties (e.g., peak width, asymmetry) and chromatographic alignment (retention time proximity). Construct a feature similarity network from these pairwise scores. Apply the multi-level optimization of modularity algorithm to identify densely connected feature clusters from the network. Optionally merge clusters derived from positive ionization mode (PI) and negative ionization mode (NI) if both acquisition modes are present in the input. Assign cluster IDs to all features and export the clustered feature table with cluster membership annotations for downstream parental signal extraction.

## Related tools

- **MS-DIAL** (Provides peak list with peak character descriptors and MS-DIAL peak character estimation algorithm implementation; required version 4.00 or higher) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Orchestrates the peak character estimation clustering step as part of its feature filtering and annotation pipeline) — https://github.com/eMetaboHUB/MS-CleanR

## Evaluation signals

- All features in the input peak list are assigned a non-null cluster ID; no features are orphaned or unassigned
- Feature clusters are internally cohesive: features within a cluster share similar peak shapes, retention times, and m/z patterns consistent with adducts, isotopes, or in-source fragments of the same metabolite
- Cluster size distribution is reasonable (no single cluster dominates >50% of features, suggesting over-merging)
- If PI and NI modes are merged, the resulting inter-mode clusters show consistent mass differences (e.g., [M+H]+ vs [M−H]−) and retention time alignment
- Exported cluster table schema includes original feature identifiers, assigned cluster IDs, and peak character metrics used in clustering

## Limitations

- Requires at least 3 blank and 3 QC samples for preceding generic filtering step; missing replicates will prevent RSD/RMD thresholding
- All features without MS/MS spectra are discarded during the generic filtering step prior to clustering; MS1-only data will cause MS-CleanR to crash
- Clustering quality depends on the accuracy and resolution of peak character estimation from MS-DIAL; poor peak picking or coelution will propagate into clusters
- Since active development of MSDial 5.x integrates parts of MS-CleanR, this tool is no longer actively maintained; users are advised to migrate to MSDial 5.x-compatible workflows

## Evidence

- [other] Apply MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties: "Apply MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties."
- [other] Construct feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters: "Construct a feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters."
- [readme] Feature clustering based on MS-DIAL peak character estimation followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [readme] Optionally merge positive ionization mode and negative ionization mode clusters: "Optionally, MS-CleanR can merge PI and NI mode during this step"
- [readme] All features without MS/MS will be discarded during first step; if data contain MS1 only, first MS-CleanR step will crash: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] No longer maintained; active development has moved to MSDial 5.x with integrated MS-CleanR functionality: "Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained."
