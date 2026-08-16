---
name: compound-isotope-and-adduct-grouping
description: Use when after XCMS feature detection, retention time correction, regrouping,
  and missing value imputation have produced an aligned feature table with multiple
  signals per compound. Use it when your data contains isotopic peaks (e.g., ¹³C variants)
  and multiple ionization products (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  license_tier: restricted
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

# compound-isotope-and-adduct-grouping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group mass spectrometry features derived from the same compound by clustering features that share similar retention time and quantitative trends across samples, thereby collapsing isotopic peaks and adduct variants into single compound representations. This skill is essential for reducing feature redundancy and improving metabolite annotation confidence in untargeted LC-MS/GC-MS metabolomics.

## When to use

Apply this skill after XCMS feature detection, retention time correction, regrouping, and missing value imputation have produced an aligned feature table with multiple signals per compound. Use it when your data contains isotopic peaks (e.g., ¹³C variants) and multiple ionization products (e.g., [M+H]+, [M+Na]+, [M+NH4]+) that obscure the true number of metabolites. Trigger conditions include: (1) feature count is 3–10× higher than expected compound count, (2) you observe co-eluting features with mass differences consistent with isotope patterns (~1.003 Da for ¹³C), and (3) you need spectral-matching-based annotation, which requires one representative spectrum per compound.

## When NOT to use

- Input is already a compound-level abundance table (e.g., post-annotation, one row per metabolite)—grouping has already been performed.
- Data contains only MS1 (intact mass) features with no retention time information or very poor retention time precision (>2 min drift)—correlation-based grouping will fail.
- Sample cohort lacks quantitative variation across conditions—near-zero correlation among features makes abundance-based clustering unreliable; consider RT and mass defect alone.

## Inputs

- XCMS xcmsSet object (after feature detection, grouping, retention time correction, regrouping, and fillPeaks)
- CSV feature table with mz_rt column names and sample names as first column
- Experiment design metadata (sample class labels for correlation computation)

## Outputs

- RC object (ramclustR object) containing cluster assignments for each feature
- RC$SpecAbund: spectral abundance matrix (clusters × samples) with summed intensities
- RC$ann: cluster annotations and molecular weight inferences
- RC$nfeat: number of features per cluster
- .msp spectral file in 'spectra' directory for external software import (MSFinder, Sirius)

## How to apply

Load a preprocessed XCMS xcmsSet object (or CSV feature table with columns named 'mz_rt' by default, first column as sample names) into RAMClustR. Execute the ramclustR function, which computes a similarity matrix combining: (1) retention time similarity (features within ~10–20 s are candidates), and (2) Pearson correlation of log-normalized intensities across all samples. The function multiplies these two scores to produce a combined similarity score, then performs hierarchical clustering with dynamic tree cutting (dynamicTreeCut package) to partition features into clusters. Each cluster represents features from a single compound. Extract the resulting RC object, which maps each original XCMS feature to a cluster ID; access spectral abundance (intensity summed across isotopes/adducts per cluster per sample) via RC$SpecAbund. Rationale: features from the same compound must satisfy both conditions simultaneously—shared retention time alone is insufficient (many unrelated compounds co-elute); abundance correlation alone is insufficient (different ionization efficiencies can produce uncorrelated signals). The product of the two scores ensures both constraints are met. The dynamic tree-cutting algorithm avoids manual threshold choice, automatically adapting to local dendrogram structure.

## Related tools

- **XCMS** (Performs feature detection, grouping by RT and mass, RT correction, regrouping, and missing value filling upstream of clustering)
- **dynamicTreeCut** (Performs automatic dendrogram cutting to partition hierarchical clusters into compact groups without manual threshold)
- **InterpretMSSpectrum** (Infers molecular weight from clustered spectra using main fragment/neutral loss rules (findMain function adapted into RAMClustR))
- **MSFinder** (External software for spectral matching and compound annotation using .msp output from RAMClustR)
- **Sirius** (External software for spectral matching and compound annotation using .ms output from RAMClustR)
- **RAMClustR** (Implements the full clustering workflow (ramclustR main function or individual stepwise functions)) — https://github.com/cbroeckl/RAMClustR

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes=experiment); RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Verify each cluster is internally coherent: all features within a cluster should share RT within ~10–20 s tolerance and show Pearson r > 0.7 (or higher, depending on ICC settings) across samples.
- Verify each cluster produces one representative spectrum (summed MS/MS if available, or consensus MS1 isotope pattern) suitable for library matching.
- Inspect RC$SpecAbund dimensions: number of rows should be << original feature count (typical compression to 20–40% of original feature count in real metabolomics data).
- Cross-check with external annotation: RC$ann should list inferred [M+H]+ m/z and annotations; verify these match expected metabolite masses and known adduct patterns for your ionization mode.
- Validate QC reproducibility: clusters detected in QC replicates should show low intra-sample CV in SpecAbund and high inter-sample rank correlation in biological replicates.

## Limitations

- Clustering quality depends heavily on input XCMS preprocessing quality; poor RT correction or feature detection propagates into failed grouping.
- Features from different compounds with very similar RT and high abundance correlation by chance (e.g., co-metabolites in same pathway) may be incorrectly grouped; manual inspection of high-correlation clusters recommended.
- Rare isotopologues (e.g., ³⁷Cl, ⁸¹Br) may not cluster with their parent if correlation is disrupted by low abundance or noise; consider filtering low-intensity features pre-clustering.
- No versioning or changelog documented; breaking changes across RAMClustR versions not formally tracked, potentially affecting reproducibility of old workflows.
- Molecular weight inference (do.findmain) agrees with InterpretMSSpectrum scoring ~90% of the time; edge cases remain, especially for ambiguous [M+H]+ vs. [M+Na]+ assignments.

## Evidence

- [intro] each compound is represented by several features. With any ionization method, isotopic peaks will be observed: "each compound is represented by several features. With any ionization method, isotopic peaks will be observed"
- [intro] two features derived from the same compound will have (approximately) the same retention time and (approximately) the same quantitative trend: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] the product of the two similarity scores provides the best approximation of total similarity: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] hierarchical clustering with dynamic tree cutting partitions features into clusters: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [intro] RAMClustR was designed to group features from the same compound using an unsupervised, platform-agnostic approach devoid of curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [other] Running ramclustR produces RC object with feature cluster assignments, spectra directory with .msp file, and SpecAbund dataset: "Running ramclustR on an XCMS xcmsSet object produces: (1) an RC object with each XCMS feature assigned to a cluster, (2) a new 'spectra' directory containing a .msp file named after the project with"
- [other] XCMS preprocesses data through feature detection, grouping, RT correction, regrouping, and missing value filling before RAMClustR: "Load a preprocessed XCMS xcmsSet object (faahKO dataset) that has undergone feature detection, grouping across samples by retention time and mass, retention time drift correction, regrouping, and"
- [readme] Column with sample name is expected to be first, feature columns named 'mz_rt' by default, adjustable with parameters: "Column with sample name is expected to be first (by default). These can be adjusted with the `featdelim` and `sampNameCol` parameters."
