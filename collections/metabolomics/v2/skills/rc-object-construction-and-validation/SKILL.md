---
name: rc-object-construction-and-validation
description: Use when after feature detection and alignment (XCMS or equivalent),
  when you have a CSV feature table with m/z and retention time columns and need to
  group features derived from the same compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - RAMClustR
  - R
  - dynamicTreeCut
  - XCMS
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  techniques:
  - LC-MS
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

# rc-object-construction-and-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and validate RAMClustR (RC) objects by ingesting feature tables (MS-only or MS+idMS/MS) and experimental design metadata, then verify that clustered features group by retention time similarity and quantitative correlation. This skill bridges raw XCMS or CSV feature data into an RC object ready for downstream molecular weight inference and annotation.

## When to use

After feature detection and alignment (XCMS or equivalent), when you have a CSV feature table with m/z and retention time columns and need to group features derived from the same compound. Use this skill when you possess: (1) a CSV feature table with sample columns and m/z_rt feature identifiers (or equivalent delimiter), (2) experimental design metadata specifying sample names and group assignments, and (3) either MS-only or MS+idMS/MS data modality. This skill is mandatory before molecular weight inference or spectral annotation.

## When NOT to use

- Input is already a clustered or annotated feature table—skip directly to do.findmain() or other downstream steps.
- Data lacks retention time information—ramclustR requires approximate same-RT clustering; MS1-only data without RT will fail.
- Feature table is in non-CSV format (e.g., Excel, NetCDF, .h5) without prior conversion to CSV with explicit m/z_rt or equivalent naming.

## Inputs

- CSV feature table with m/z_rt (or delimiter-specified) feature names and sample intensity columns
- Experimental design metadata (pheno_csv or ExpDes object) with sample names and group assignments
- Optional: XCMS object (xcmsObj parameter) if using xcms output directly
- Optional: MS/MS feature table (idmsms parameter) for combined MS+idMS/MS analysis

## Outputs

- RAMClustR object (RC) with clustered features grouped by compound
- RC$SpecAbund: feature abundance matrix indexed by cluster and sample
- RC$ann: annotations and metadata for each cluster
- RC$mzrt: retention time and m/z values per feature per cluster
- MSP-format spectra files written to 'spectra' subfolder (ready for MSFinder/Sirius import)

## How to apply

Load the feature table (CSV) via the `ms` parameter (MS-only) or both `ms` and `idmsms` parameters (combined data), specifying the feature delimiter (`featdelim`, default 'mz_rt'), similarity threshold (`st`, e.g., 5 ppm), sample name column position (`sampNameCol`), and experimental design via `ExpDes` or `pheno_csv`. For MS+idMS/MS data, additionally specify `timepos` to indicate where retention time appears in feature identifiers. Execute the main `ramclustR()` function or the stepwise workflow (`rc.get.xcms.data()`, `rc.expand.sample.names()`, `rc.feature.replace.na()`, `rc.feature.normalize.qc()`, `rc.ramclustr()`), which internally applies retention time and quantitative correlation similarity scoring via `dynamicTreeCut` hierarchical clustering. Validate the output RC object by confirming that clustered features share approximately the same retention time and quantitative trends across samples (inspecting `RC$ann`, `RC$SpecAbund`, and retention time fields).

## Related tools

- **XCMS** (Feature detection and alignment upstream; output (xcmsSet or xcmsObj) can be directly passed to ramclustR via xcmsObj parameter)
- **dynamicTreeCut** (Hierarchical clustering and dendrogram cutting used internally by ramclustR to group features by retention time and correlation similarity)
- **InterpretMSSpectrum** (Provides findMain function adapted for molecular weight inference in RC object post-processing)
- **MSFinder** (Downstream import target for RC-generated .mat format spectra for structural annotation)
- **Sirius** (Downstream import target for RC-generated .ms format spectra for structural annotation)

## Examples

```
ramclustobj <- ramclustR(ms = "peaks.csv", pheno_csv = "phenoData.csv", st = 5, maxt = 1, blocksize = 1000)
```

## Evaluation signals

- RC object is non-null and contains $SpecAbund (feature abundance matrix), $ann (cluster annotations), and $mzrt (retention time/m/z per feature) fields.
- Feature clusters have approximately identical retention times (within same-RT tolerance, typically ±2–3 min depending on chromatography).
- Feature clusters exhibit quantitative correlation across samples (Pearson or Spearman r > 0.7 typical for true co-eluting features).
- Number of clusters (nrow(RC$SpecAbund) or length(unique(cluster IDs))) is less than the input feature count, confirming grouping occurred.
- Spectra folder contains .msp (or .mat/.ms) files with one file per cluster, parseable by downstream tools (MSFinder/Sirius).

## Limitations

- No changelog or version history documented—users cannot track breaking changes between releases.
- Requires retention time alignment and correction (retcor) upstream; garbage-in/garbage-out if RT drift is not corrected.
- Unsupervised clustering may misgroup features from different compounds if they co-elute and correlate; manual curation or spectral validation recommended.
- Performance scales with feature count; blocksize parameter (default 1000) may need tuning for very large datasets (>10,000 features).
- Missing value handling via fillPeaks or rc.feature.replace.na must be applied before ramclustR; sparse or unimputed data will degrade correlation scoring.

## Evidence

- [other] RAMClustR accepts csv input via the 'ms' parameter for MS-only analysis and additionally accepts an 'idmsms' parameter for combined MS+idMSMS analysis.: "RAMClustR accepts csv input via the 'ms' parameter for MS-only analysis and additionally accepts an 'idmsms' parameter for combined MS+idMSMS analysis"
- [intro] Features derived from the same compound have approximately the same retention time and quantitative trend across samples: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product of retention time and correlational similarity scores provides best approximation of total similarity: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] RAMClustR groups features from the same compound using unsupervised, platform-agnostic approach without curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [readme] If the file contains features from MS1, assign those to the ms parameter. If the file contains features from MS2, assign those to the idmsms parameter.: "If the file contains features from MS1, assign those to the `ms` parameter. If the file contains features from MS2, assign those to the `idmsms` parameter."
- [readme] Individual stepwise workflow supports na replacement, normalization, and filtering before ramclustR clustering: "ramclustObj <- rc.feature.replace.na(ramclustObj = ramclustObj); ramclustObj <- rc.feature.normalize.qc(ramclustObj = ramclustObj, qc.tag = "QC"); ramclustObj <- rc.feature.filter.cv(ramclustObj ="
