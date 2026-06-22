---
name: mass-spectral-similarity-scoring-across-samples
description: Use when after XCMS feature detection, grouping, and retention time correction when you have aligned features with consistent retention times and intensity patterns across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RAMClustR
  - dynamicTreeCut
  - R
  - InterpretMSSpectrum
  - XCMS
  - MSFinder
  - Sirius
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
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
---

# mass-spectral-similarity-scoring-across-samples

## Summary

Compute combined retention time and intensity-correlation similarity scores to group mass spectrometry features derived from the same compound. This skill combines approximate retention time matching with quantitative trend correlation across samples to identify co-eluting, co-varying features that represent isotopes, adducts, and fragments of a single metabolite.

## When to use

Apply this skill after XCMS feature detection, grouping, and retention time correction when you have aligned features with consistent retention times and intensity patterns across samples. Use it to disambiguate which features belong to the same molecular entity before molecular weight inference or spectral matching—especially in non-targeted LC-MS or GC-MS metabolomics where each compound produces multiple signals (isotopes, [M+H]+, [M+Na]+, fragments).

## When NOT to use

- Input features have not undergone retention time correction or regrouping; clustering will be misled by drift.
- Feature table is already clustered or de-isotoped by another method; re-clustering risks fragmentation or over-merging.
- Samples have highly variable chromatographic performance (e.g., very long or very short runs); intensity correlation becomes unreliable.

## Inputs

- XCMS xcmsSet object (post-grouping, retention-time-corrected, filled peaks)
- Experiment design metadata (sample-to-batch/group assignments)
- Feature abundance matrix with aligned m/z and retention time

## Outputs

- RC object (RAMClustR clustering result) with cluster assignments for each feature
- Spectral abundance matrix (RC$SpecAbund) with cluster-level intensities
- .msp format spectral file (one entry per cluster, suitable for MSFinder/Sirius import)
- Cluster annotations and molecular weight inferences

## How to apply

For each pair of XCMS features, compute a retention time similarity score (e.g., Euclidean distance or correlation of retention times across replicates) and an intensity correlation score (Pearson or Spearman correlation of quantitative abundance across all samples). Multiply the two scores to obtain a combined similarity metric that requires both conditions (similar RT and correlated intensity) to be satisfied simultaneously. Submit this scored feature-pair matrix to hierarchical clustering (e.g., Euclidean or average linkage), then apply dynamic tree cutting to partition the dendrogram into clusters. Each cluster represents features inferred to derive from one compound. The rationale is that true co-features must co-elute (RT proximity) AND co-vary quantitatively (intensity correlation), whereas false positives violate one or both conditions.

## Related tools

- **XCMS** (Performs initial feature detection, grouping by m/z and RT, retention time correction, and regrouping to produce the aligned feature set that is input to similarity scoring.)
- **dynamicTreeCut** (Cuts the hierarchical clustering dendrogram into clusters based on branch structure, avoiding arbitrary height thresholds and automatically merging or splitting branches to define cluster boundaries.)
- **RAMClustR** (Orchestrates similarity scoring, hierarchical clustering, and dynamic tree cutting; outputs RC object with cluster assignments, spectral abundance matrix, and .msp exports.) — https://github.com/cbroeckl/RAMClustR
- **InterpretMSSpectrum** (Provides findMain function adapted within RAMClustR to infer molecular weight from cluster mass values using multiple scoring methods.)
- **MSFinder** (External software that imports .mat or .msp spectral output from RAMClustR for spectral matching and structural annotation.)
- **Sirius** (External software that imports .ms spectral output from RAMClustR for spectral matching and structural annotation.)

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes = experiment); RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Each cluster contains features with approximately equal retention times (within instrument drift tolerance, typically <1–2 min).
- Features within a cluster show strong Pearson/Spearman correlation (r > 0.7–0.9) of intensity across samples.
- Cluster mass values form isotopic or adduct patterns (e.g., M, M+1, M+2 for 12C/13C; M+23 for sodium adduct) consistent with known ionization rules.
- .msp spectral file is generated with one entry per cluster; each entry contains aggregated spectra suitable for library matching.
- Downstream molecular weight inference (via do.findmain) converges on a single inferred mass per cluster with ~90% agreement between independent scoring methods.

## Limitations

- Algorithm assumes features from the same compound have approximately equal retention times; early/late-eluting isomers or chromatographic anomalies may fragment a single compound into multiple clusters.
- Intensity correlation requires sufficient sample-to-sample variation; uniform or very low-variance samples reduce discriminative power.
- No changelog or version history available; breaking changes between releases are undocumented, potentially affecting reproducibility.
- Scoring method combines RT and correlation via multiplication, which is heuristic; edge cases (e.g., near-zero RT distance + high correlation) may produce unintuitive boundary behavior.
- Dynamic tree cutting is automatic; no manual post-hoc validation or expert curation of clusters is provided.

## Evidence

- [intro] Two-condition requirement for co-features: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product scoring rationale: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] Hierarchical clustering and dynamic tree cutting: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [intro] Unsupervised, platform-agnostic approach: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [intro] RC object outputs and SpecAbund matrix: "Running ramclustR on an XCMS xcmsSet object produces: (1) an RC object with each XCMS feature assigned to a cluster, (2) a new 'spectra' directory containing a .msp file named after the project with"
- [readme] README: stepwise workflow and cluster inspection: "ramclustObj <- rc.ramclustr(ramclustObj = ramclustObj); ramclustObj <- do.findmain(ramclustObj = ramclustObj); print(ramclustobj$ann); print(ramclustobj$nfeat); print(ramclustobj$SpecAbund[,1:6])"
