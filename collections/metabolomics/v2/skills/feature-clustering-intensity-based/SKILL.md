---
name: feature-clustering-intensity-based
description: Use when after matching mass-to-charge ratios to a KEGG database and obtaining multiple candidate metabolites per feature, but before filtering quasi-molecular adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-clustering-intensity-based

## Summary

Cluster LC-MS features that likely derive from the same metabolite by leveraging intensity patterns across samples, a preprocessing step in mWISE that prepares candidates for downstream filtering and diffusion-based prioritization. This skill reduces annotation redundancy by grouping related peaks before network-based ranking.

## When to use

Apply this skill after matching mass-to-charge ratios to a KEGG database and obtaining multiple candidate metabolites per feature, but before filtering quasi-molecular adducts. Use it when your feature table includes intensity values across samples and you suspect many peaks represent isotopologues, adducts, or in-source fragments of the same metabolite rather than distinct compounds.

## When NOT to use

- Input lacks or has insufficient intensity information across replicates/conditions (clustering cannot identify co-varying features without intensity variance).
- All features are already known to represent distinct metabolites (clustering would be redundant).
- Target is targeted metabolomics with a small, predefined set of peaks (intensity-based clustering designed for untargeted discovery where candidate explosion is common).

## Inputs

- Feature table with m/z values, retention time (if available), and intensity matrix across samples
- KEGG candidate assignments (output from matching stage with multiple candidates per feature)

## Outputs

- Clustered feature table with cluster membership annotations
- Cluster representatives ready for filtering and diffusion-based prioritization

## How to apply

Execute the mWISE `featuresClustering` function on the feature table populated with m/z values and intensity profiles across samples. The function groups features that co-vary in intensity, implicitly assuming features with similar abundance patterns across replicates or conditions likely originate from a single metabolite. The clustering is intensity-driven, meaning it uses the correlation or co-elution of intensity signals rather than m/z alone. After clustering, each cluster receives a single representative rank in downstream steps, reducing false positives. The output is a clustered candidate table that feeds directly into `clusterBased.filter`, which then applies quasi-molecular adduct and frequency thresholds to remove spurious members.

## Related tools

- **mWISE** (Provides the featuresClustering function and wraps clustering into the full annotation workflow) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Informs default adduct and fragment definitions used to refine clusters after intensity-based grouping)
- **cliqueMS** (Referenced as source for adduct and fragment knowledge integrated into cluster refinement)
- **R** (Execution environment for featuresClustering function)

## Examples

```
# Load Trypanosoma dataset and apply feature clustering
data("sample.dataset")
data("sample.keggDB")
clustered_features <- featuresClustering(sample.dataset$featureTable)
```

## Evaluation signals

- Cluster size and composition: verify that cluster members have correlated intensity patterns across samples and plausible m/z differences (e.g., ±1.008 Da for isotopes, adduct mass shifts).
- Reduction in candidate redundancy: confirm that the number of unique clusters is substantially less than the number of raw matched candidates, indicating successful grouping.
- Downstream filter stability: after `clusterBased.filter` is applied to clusters, check that quasi-molecular adducts dominate and that minimum observed frequency threshold removes singletons as intended.
- Performance metric improvement: verify that top-3 precision, recall, and F1-score metrics (computed by `performanceEvaluation` against df.Ref) improve or remain stable compared to unfiltered candidates.
- Peak recovery validation: confirm that `recoveringPeaks` function successfully recovers any completely filtered clusters, indicating clusters were appropriately formed.

## Limitations

- Clustering quality depends on sample heterogeneity and intensity variance; samples with uniform abundance profiles or low dynamic range may yield uninformative clusters.
- Intensity-based clustering assumes co-variance implies common origin; features with similar abundance by chance (unrelated metabolites with identical sample distribution) may be incorrectly grouped.
- No explicit retention time information is mentioned in the article; if RT is available but not used in clustering, temporally separated isomers may be grouped.
- The article does not specify clustering algorithm parameters (e.g., distance metric, linkage criterion, or correlation threshold); users must rely on mWISE defaults.

## Evidence

- [intro] the features that may come from the same metabolite are clustered using the `featuresClustering` function: "the features that may come from the same metabolite are clustered using the `featuresClustering` function"
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii) clustering and filtering the potential KEGG candidates: "mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii)"
- [intro] the `clusterBased.filter` function: "the `clusterBased.filter` function"
- [intro] the diffusion prioritized table is built using the `finalResults` function: "the diffusion prioritized table is built using the `finalResults` function"
