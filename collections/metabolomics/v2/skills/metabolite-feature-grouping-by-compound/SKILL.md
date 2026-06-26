---
name: metabolite-feature-grouping-by-compound
description: Use when after XCMS feature detection and retention time correction,
  when you have a feature table (CSV or XCMS object) with m/z and retention time values
  aligned across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - RAMClustR
  - R
  - dynamicTreeCut
  - XCMS
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  techniques:
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

# metabolite-feature-grouping-by-compound

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group mass spectrometry features derived from the same compound by leveraging retention time similarity and quantitative correlation across samples. This skill consolidates multiple ions, isotopes, and adducts representing a single metabolite into coherent clusters for downstream annotation and interpretation.

## When to use

After XCMS feature detection and retention time correction, when you have a feature table (CSV or XCMS object) with m/z and retention time values aligned across samples. Apply this skill when your dataset exhibits the characteristic pattern that features from the same compound share approximately the same retention time and show correlated intensity trends across replicates—a prerequisite for unsupervised clustering without curated rules.

## When NOT to use

- Input is already a pre-curated metabolite abundance table (i.e., features have already been manually or rule-based grouped); clustering would be redundant.
- Retention time information is absent or unreliable (e.g., flow injection analysis without chromatographic separation); the algorithm depends on RT correlation as a primary similarity signal.
- Data come from platforms with very poor mass accuracy (>>10 ppm over the mass range); feature matching by m/z will fail to resolve true co-eluting signals.

## Inputs

- CSV feature table with columns: sample names (first column by default) and features named in 'mz_rt' format (e.g., '200.1234_45.67')
- XCMS object (xcmsSet) with aligned features and retention time-corrected data after fillPeaks
- Phenotype/design CSV with sample metadata (batch, sample group, QC indicator if available)
- MS2 fragmentation table (optional; CSV with 'idmsms' parameter) for MS+idMS/MS combined analysis

## Outputs

- RAMClustR object (RC) containing 'nfeat' (number of clusters), 'ann' (cluster annotations), 'SpecAbund' (mean spectrum abundance per cluster), 'featclus' (feature-to-cluster assignments)
- Spectral output files in MSP format suitable for import into MSFinder or Sirius
- Cluster-level retention times and quantitative profiles for each grouped metabolite

## How to apply

Load your feature table (CSV with 'mz_rt' formatted feature names by default, or XCMS object) and supply it to the ramclustR function via the 'ms' parameter for MS1-only data or 'idmsms' parameter when MS2 fragmentation data is also available. Specify a similarity threshold ('st', typically 5 ppm or mass units) and retention time window ('maxt', typically 1 minute). The algorithm computes a combined similarity score as the product of retention time proximity and feature-across-samples quantitative correlation, then applies hierarchical clustering with dynamic tree cutting to partition features into compound groups. Verify clustering by inspecting the RC object's retention time ranges per cluster (should be tight, within specified window) and examining feature abundance correlation matrices (should show high correlation within clusters).

## Related tools

- **XCMS** (Detects and aligns mass spectrometry features; output fed to ramclustR for clustering)
- **dynamicTreeCut** (Performs hierarchical clustering dendrogram cutting to partition feature similarity matrix into clusters)
- **InterpretMSSpectrum** (Provides findMain scoring method adapted by ramclustR for molecular weight inference on clustered spectra)
- **MSFinder** (Downstream tool accepting RAMClustR-generated .mat format spectra for structure annotation)
- **Sirius** (Downstream tool accepting RAMClustR-generated .ms format spectra for structure and formula inference)
- **RAMClustR** (Core clustering function implementing the unsupervised, correlation + retention-time-based grouping algorithm) — https://github.com/cbroeckl/RAMClustR

## Examples

```
ramclustobj <- ramclustR(ms = 'peaks.csv', pheno_csv = 'phenoData.csv', st = 5, maxt = 1, blocksize = 1000)
```

## Evaluation signals

- Each cluster's internal features share retention time values within the specified window (e.g., < 1 minute spread for st=5, maxt=1)
- Feature abundance correlations within clusters are high (r > 0.7 or similar, indicating quantitative coherence across samples)
- Cluster sizes are reasonable for biological samples: singleton and small clusters (~2–5 features) for unique metabolites; larger clusters only when isotopes and adducts are expected
- RC object outputs (RC$nfeat, RC$ann, RC$SpecAbund) are populated; no errors or warnings about singular matrices or degenerate hierarchical clusters
- Downstream spectral annotation tools (MSFinder, Sirius) successfully import the generated MSP or .ms format files and return plausible structure/formula matches

## Limitations

- Algorithm assumes features from the same compound have approximately the same retention time; this breaks for isomers or when chromatographic resolution is poor.
- Similarity scoring uses product of RT and correlation metrics; if one signal is very noisy or sparse, the product may be misleadingly low even if RT overlap is strong.
- No changelog or version history is documented; breaking changes between versions are not tracked, complicating reproducibility across time.
- Performance depends on choice of 'st' (similarity threshold) and 'maxt' (retention time window); optimal values are data and platform-specific and may require tuning.
- The method is unsupervised and devoid of curated rules, which is a strength for generality but may group unrelated features if they happen to co-elute and correlate by chance in small sample sets.

## Evidence

- [intro] RAMClustR groups features from the same compound using unsupervised, platform-agnostic approach without curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [intro] Features from the same compound share retention time and quantitative correlation across samples: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product of retention time and correlation similarity provides best total similarity score: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [readme] RAMClustR accepts MS-only CSV input via 'ms' parameter and MS+idMS/MS input via 'idmsms' parameter: "If the file contains features from MS1, assign those to the `ms` parameter. If the file contains features from MS2, assign those to the `idmsms` parameter."
- [readme] Input CSV feature names expected in 'mz_rt' format with sample name column first by default: "Choose input file with feature column names `mz_rt` (expected by default). Column with sample name is expected to be first (by default). These can be adjusted with the `featdelim` and `sampNameCol`"
- [readme] ramclustR function accepts parameters for similarity threshold and retention time window: "ramclustobj <- ramclustR( ms = filename, pheno_csv = pheno, st = 5, maxt = 1, blocksize = 1000 )"
