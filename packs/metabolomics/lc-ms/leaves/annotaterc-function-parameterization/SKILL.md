---
name: annotaterc-function-parameterization
description: Use when you have LC–MS all-ion fragmentation chromatograms already processed by xcms and clustered by RamClustR, a feature table (targetTable.csv format) listing features to annotate, and you need rank-1 metabolite or lipid identifications with confidence metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotaterc-function-parameterization

## Summary

Configure and execute the annotateRC function to match experimental LC–MS all-ion fragmentation spectra against fragment ion databases (e.g., LipidPos) and rank candidate metabolite annotations. This skill bridges processed xcms/RamClustR objects and feature tables to produce ranked lipid or metabolite identifications.

## When to use

You have LC–MS all-ion fragmentation chromatograms already processed by xcms and clustered by RamClustR, a feature table (targetTable.csv format) listing features to annotate, and you need rank-1 metabolite or lipid identifications with confidence metrics. Use this skill when annotation libraries (e.g., LipidPos for positive-mode lipids) match your ionization mode and metabolite class of interest.

## When NOT to use

- Raw (non-centroid) LC–MS data: annotateRC requires centroid-mode spectra.
- Features not yet processed through xcms and RamClustR: the function expects pre-clustered xset and RC objects.
- Ionization mode or metabolite class mismatch: e.g., using LipidPos (positive mode) on negative-mode data will yield invalid or zero annotations.

## Inputs

- xcms xset object (processed all-ion fragmentation chromatograms in centroid mode)
- RamClustR RC object (clustered features from the xset)
- Feature table (e.g., targetTable.csv: CSV with feature identifiers to annotate)
- Fragment ion database library (e.g., LipidPos for positive-mode lipids)

## Outputs

- annotations object containing rankedResult (candidate annotations ranked by match score)
- Matched ion spectra and fragment matches per feature
- Global annotation summary report (count of successfully annotated features)
- Saved annotation results (to user-specified directory)

## How to apply

Load the xcms xset object and RamClustR RC object containing processed all-ion fragmentation data; load the target feature table (e.g., targetTable.csv) specifying which features to annotate. Call the annotateRC function, supplying the xset, RC object, and the appropriate fragment library (LipidPos for lipids in positive mode, or other MAMP/MSMS databases as applicable). The function will match experimental spectra against database entries and return a ranked annotations object. Extract the rankedResult object to inspect matched ions, rank scores, and candidate identities. Visualize matched spectra using plotResultSpec to validate ion matches before reporting results; save annotation outputs to a user-specified directory. Success is indicated by rank-1 annotations (highest confidence match) for a subset of features; expect that not all features will receive valid annotations depending on database coverage and spectral quality.

## Related tools

- **xcms** (Processes raw LC–MS all-ion fragmentation chromatograms into feature tables and xset objects required by annotateRC) — https://bioconductor.org/packages/xcms
- **RamClustR** (Clusters and groups features from xcms into consolidated RC objects passed to annotateRC for spectral matching) — https://bioconductor.org/packages/RamClustR
- **MetaboAnnotatoR** (Wrapper package containing annotateRC function and fragment ion database libraries (e.g., LipidPos)) — https://github.com/gggraca/MetaboAnnotatoR

## Examples

```
annotateRC(xset = xset, RC = RC, targets = targetTable, libname = 'LipidPos', ionmode = 'pos'); rankedResult <- annotations$rankedResult
```

## Evaluation signals

- At least one feature receives a rank-1 annotation (highest-confidence match) with non-null candidate name and fragment match score.
- Rank-1 annotations correspond to reasonable m/z and retention-time predictions for known metabolites or lipids in the ionization mode.
- Matched ion spectra (from plotResultSpec) show substantial overlap between experimental and database fragment peaks (visual validation of rank-1 candidate).
- Global annotation summary counts the total number of successfully annotated features; expect 0–100% depending on database coverage and spectral quality (e.g., 3 of 6 features in the example).
- rankedResult object is non-empty and sortable by rank score; features without annotation have zero or null rank-1 entries.

## Limitations

- Annotation success depends on database coverage: features with spectral properties outside library entries will not be annotated.
- All-ion fragmentation spectra can be noisy; poor spectral quality or missing characteristic fragments reduce rank-1 match confidence.
- LipidPos library is specific to positive-mode lipids; incorrect library choice (e.g., using positive libraries on negative-mode data) yields no or spurious annotations.
- Installation issues may arise from Rcpp version conflicts or multiarch compilation errors; documented workarounds include setting R_REMOTES_NO_ERRORS_FROM_WARNINGS or using --no-multiarch flag.
- Only centroid-mode spectra are supported; profile-mode or uncalibrated m/z data will fail or produce unreliable matches.

## Evidence

- [intro] annotateRC enables matching of experimental spectra to fragment databases with confidence ranking: "Then annotations can be performed using the *annotateRC* function"
- [intro] Feature table format and RamClustR/xcms object requirements: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [intro] Ranked result inspection and visualization workflow: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [intro] Spectral visualization and result saving steps: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [readme] Centroid-mode data requirement: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [intro] Example outcome showing partial annotation success: "Three out of the six features were annotated with to a lipid"
