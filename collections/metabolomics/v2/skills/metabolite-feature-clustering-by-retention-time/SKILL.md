---
name: metabolite-feature-clustering-by-retention-time
description: Use when after XCMS feature detection, grouping, retention time correction,
  regrouping, and missing value filling on LC-MS or GC-MS data, when you have an aligned
  feature table with retention times and intensity profiles across multiple samples
  and need to collapse redundant features into.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RAMClustR
  - dynamicTreeCut
  - R
  - InterpretMSSpectrum
  - XCMS
  - MSFinder
  - Sirius
  techniques:
  - LC-MS
  - GC-MS
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting
  dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-clustering-by-retention-time

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Groups mass spectrometry features derived from the same metabolite by clustering on retention time similarity and quantitative correlation patterns across samples. This resolves the problem that each compound produces multiple features due to isotopic peaks and adduction/fragmentation phenomena, enabling downstream spectral annotation and molecular weight inference.

## When to use

After XCMS feature detection, grouping, retention time correction, regrouping, and missing value filling on LC-MS or GC-MS data, when you have an aligned feature table with retention times and intensity profiles across multiple samples and need to collapse redundant features into compound-level clusters for annotation.

## When NOT to use

- Input is a pre-clustered or already-annotated feature table — this skill assumes unclustered, aligned XCMS features.
- Data lacks meaningful retention time information (e.g., direct infusion or untargeted shotgun data without chromatographic separation).
- Sample set is too small or lacks replicate structure — clustering relies on correlation patterns across samples and will be unreliable with <3 replicates or highly variable sample types.

## Inputs

- XCMS xcmsSet object (preprocessed with feature detection, grouping, retention time correction, regrouping, and fillPeaks)
- Feature intensity matrix (CSV with sample names as first column, feature names as mz_rt format in header)
- Experiment design metadata (optional; sample batch, order, and QC indicators for normalization)

## Outputs

- RC object (RAMClustR object) with clustered feature assignments
- SpecAbund matrix (features × samples, one row per cluster)
- .msp spectral file (spectra directory with MSP-formatted spectra for all clusters)
- Cluster annotations and molecular weight inferences (RC$ann, RC$mz)

## How to apply

Execute the ramclustR function on a preprocessed XCMS xcmsSet object or a feature intensity matrix (with rows as features labeled by mz_rt and columns as samples), optionally providing experiment design metadata. The algorithm computes pairwise similarity scores as the product of (1) retention time similarity (features within ~10–20 s are considered similar) and (2) Pearson correlation of intensity patterns across samples. These scores are submitted to hierarchical clustering with dynamic tree cutting to define cluster boundaries. The method is unsupervised and platform-agnostic, requiring no curated rules. Output includes an RC object mapping each feature to a cluster, a SpecAbund abundance matrix with one row per cluster, and a .msp spectral file suitable for external annotation tools. Molecular weight inference can then be applied via do.findmain using either retention time-based or intensity-based scoring (~90% agreement).

## Related tools

- **XCMS** (Upstream feature detection and alignment; produces xcmsSet object input to ramclustR)
- **dynamicTreeCut** (Performs hierarchical clustering dendrogram cutting to define cluster boundaries from retention time and correlation similarity scores)
- **RAMClustR** (Main clustering engine; implements unsupervised feature grouping and molecular weight inference) — github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Provides findMain function adapted by RAMClustR for molecular weight scoring and inference)
- **MSFinder** (External software for spectral annotation; consumes .mat format spectra exported by RAMClustR)
- **Sirius** (External software for spectral annotation; consumes .ms format spectra exported by RAMClustR)

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes = experiment); RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Each feature in the input xcmsSet is assigned to exactly one cluster in the RC object (no orphaned or multiply-assigned features).
- SpecAbund matrix has one row per cluster and one column per sample; all values are non-negative and represent aggregated or representative abundances.
- Clusters containing features with similar retention times (within expected drift tolerance of ~10–20 s) and high Pearson correlation (r > 0.7) across samples; inspect RC$clrt (cluster retention times) and inter-cluster distances.
- .msp file in spectra directory is valid and readable; each entry contains cluster ID, retention time, and m/z values.
- Molecular weights inferred by do.findmain agree with theoretical monoisotopic masses within ±0.02 Da (absolute error) or ±10 ppm (relative error), and ~90% concordance between retention time and intensity-based scoring methods.

## Limitations

- No changelog or version history documented; breaking changes between releases are undocumented.
- Clustering depends on correlation structure across samples; datasets with only a few replicates, high technical variance, or very different sample types may produce unstable clusters.
- Retention time alone is insufficient; features must also show correlated intensity patterns—features with identical RT but uncorrelated profiles across samples will not cluster together.
- Molecular weight inference (do.findmain) achieves ~90% agreement between methods; the remaining 10% of ambiguous cases may require manual review or external validation.
- Platform-agnostic design means no compound-specific curated rules are applied; this improves generalizability but may miss known adducts or losses in specialized contexts.

## Evidence

- [intro] two features derived from the same compound will have (approximately) the same retention time and will have (approximately) the same: "two features derived from the same compound will have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] ramclustR was designed to group features designed from the same compound using an approach which is unsupervised, platform agnosic, and devoid of curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [intro] submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [methods] RC object containing clustered features, spectral abundance matrix, and molecular weight inferences: "Extract the RC object containing clustered features, spectral abundance matrix, and molecular weight inferences."
- [readme] ramclustobj <- ramclustR( ms = filename, pheno_csv = pheno, st = 5, maxt = 1, blocksize = 1000 ): "ramclustobj <- ramclustR( ms = filename, pheno_csv = pheno, st = 5, maxt = 1, blocksize = 1000 )"
- [intro] In practice we find that the two scoring methods agree about 90% of the time.: "In practice we find that the two scoring methods agree about 90% of the time."
