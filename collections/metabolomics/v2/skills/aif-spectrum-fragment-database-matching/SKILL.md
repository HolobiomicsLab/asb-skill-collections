---
name: aif-spectrum-fragment-database-matching
description: Use when you have a feature table from untargeted LC–MS all-ion fragmentation
  (AIF) chromatograms processed by xcms and RamClustR, and you want to assign metabolite
  annotations to individual features by comparing their experimental MS/MS spectra
  against curated fragment libraries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS
  All-ion fragmentation (AIF) datasets
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

# AIF Spectrum Fragment Database Matching

## Summary

Match experimental MS/MS spectra from all-ion fragmentation LC–MS data against ion fragment libraries to assign metabolite identities to detected features. This skill bridges processed feature tables (from xcms/RamClustR) with ranked lipid or metabolite annotations by comparing fragmentation patterns.

## When to use

You have a feature table from untargeted LC–MS all-ion fragmentation (AIF) chromatograms processed by xcms and RamClustR, and you want to assign metabolite annotations to individual features by comparing their experimental MS/MS spectra against curated fragment libraries (e.g., LipidPos for lipids). Use this skill when spectral fragmentation data and feature identifiers are available and you need rank-ordered candidate annotations with quality confidence.

## When NOT to use

- Input spectra are in profile mode rather than centroid mode; MetaboAnnotatoR requires centroid-mode raw LC-MS AIF chromatograms.
- Feature table is already annotated or contains pre-assigned metabolite identifiers; use this skill as the primary annotation step, not as a post-hoc validator.
- No RamClustR object is available or coeluting features have not been clustered; the annotateRC function requires the RC object for context and spectral quality assessment.

## Inputs

- xcmsSet object (processed LC–MS AIF chromatogram feature set)
- RamClustR object (RC; clustering of coeluting features)
- Feature table (e.g., targetTable.csv with feature identifiers and m/z values)
- Ion fragment database (e.g., LipidPos library for positive ionization mode)
- Centroid-mode MS/MS spectra associated with features

## Outputs

- Ranked candidate metabolite/lipid annotations object (annotations with rankedResult)
- Annotation summary report (global statistics on successful assignments)
- Matched-ion spectra visualizations (from plotResultSpec)
- Saved annotation results table (user-specified directory)

## How to apply

Load the xcmsSet object and RamClustR object containing processed AIF chromatograms alongside a feature table (targetTable.csv format) specifying the features to annotate. Execute the annotateRC function, passing the xset, RC object, and selected fragment library (e.g., LipidPos for lipid-mode data). The function matches experimental spectra against the database, returning ranked candidate annotations prioritized by match quality. Extract and inspect the rankedResult object from the annotations output to identify rank-1 assignments and filter for high-confidence lipid or metabolite matches. Validate results by visually inspecting matched ions using plotResultSpec to confirm spectral alignment; typically expect 40–50% of features to receive valid annotations depending on spectral quality and library coverage.

## Related tools

- **MetaboAnnotatoR** (Primary annotation engine; provides annotateRC function for spectrum–database matching and plotResultSpec for result visualization) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Prerequisite feature detection and retention-time alignment; produces xcmsSet object required as input to annotateRC)
- **RamClustR** (Prerequisite spectral clustering of coeluting features; produces RC object required as input to annotateRC)
- **R** (Scripting environment for loading objects, executing annotateRC, and inspecting ranked results)

## Examples

```
annotateRC(xset = xset, RC = RC, targets = targetTable.csv, database = 'LipidPos'); inspect(annotations$rankedResult); plotResultSpec(annotations, feature_idx = 1)
```

## Evaluation signals

- Rank-1 annotation success rate: verify that ≥1 feature receives a valid lipid/metabolite annotation (baseline expectation 3/6 in reference example); compare ranked annotations across features to identify consistent vs. spurious matches.
- Spectral match quality: inspect plotResultSpec outputs to confirm that matched ions align between experimental and database spectra; verify cosine similarity or fragment ion overlap is high (visual inspection for significant peak correspondence).
- Annotation coverage and distribution: confirm that the annotation summary report lists all features attempted and categorizes them by match rank (rank-1, rank-2, unmatched); ensure no obvious features are missing from the output.
- Library specificity: verify that annotations are drawn from the selected library (e.g., all results from LipidPos should contain lipid class names and m/z values consistent with lipid structures).
- Output file integrity: check that saved annotation results include feature identifiers, ranked candidate names, match metrics, and reproducible output paths.

## Limitations

- Annotation success depends on spectral quality and library completeness; lipophilic or rare metabolites may not be represented in fragment databases, resulting in unmatched features even with high-quality spectra.
- Installation may fail due to Rcpp version mismatches or missing i386 architecture support on some systems; workarounds exist but require environment configuration (e.g., Sys.setenv(R_REMOTES_NO_ERRORS_FROM_WARNINGS='true'), --no-multiarch flag).
- Requires centroid-mode MS/MS spectra; profile-mode data or spectra that have not been properly deisotoped or cleaned will produce poor or no annotations.
- Rank-1 annotation assignments do not guarantee biological validity; manual curation via plotResultSpec and reference to known metabolite markers is necessary for high-confidence interpretation.
- Performance and annotation rate vary by LC–MS instrumental setup, ionization mode (positive vs. negative), and metabolite class; the reference example (3/6 features) should not be generalized as an expected rate across all datasets.

## Evidence

- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [intro] Experimental spectra are matched against fragment databases via the annotateRC function: "Then annotations can be performed using the *annotateRC* function"
- [intro] Three of six features received successful lipid annotations using LipidPos library: "Three out of the six features were annotated with to a lipid"
- [intro] Ranked results are accessed via the rankedResult object stored in the annotations output: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [intro] Spectral matching is visualized and validated using the plotResultSpec function: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [readme] Input data must be centroid-mode LC-MS AIF chromatograms: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [intro] The workflow loads processed xcms and RamClustR objects as prerequisites: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [intro] Annotation results can be saved to a user-specified directory: "It is possible to save the annotation results to a user-specified directory"
