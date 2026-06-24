---
name: xcms-ramclustr-data-object-integration
description: Use when when you have raw LC-MS all-ion fragmentation (AIF) chromatograms
  in centroid mode and need to prepare them for metabolite annotation using fragment
  ion matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
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
- To install this package, start R (version "4.5.0" or higher)
- An example of feature annotation using LC-MS AIF chromatograms processed using xcms
  and RamClustR packages
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
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

# xcms-ramclustr-data-object-integration

## Summary

Integration of xcms peak-picked data with RamClustR pseudo-MS/MS spectra to create a unified R object pair suitable for fragment-based metabolite annotation. This skill bridges feature detection and spectral clustering, enabling downstream annotation workflows in untargeted LC-MS all-ion fragmentation metabolomics.

## When to use

When you have raw LC-MS all-ion fragmentation (AIF) chromatograms in centroid mode and need to prepare them for metabolite annotation using fragment ion matching. Specifically: you have processed your data through xcms for peak detection and RamClustR for pseudo-MS/MS spectrum generation, and you need to combine these two objects into a single analytical framework before applying the annotateRC function.

## When NOT to use

- Input LC-MS data is already in profile (centroid = FALSE) mode; xcms requires centroid-mode acquisition or transformation.
- You have only one of xcms or RamClustR already processed; both must be generated from the same raw chromatogram to maintain feature correspondence.
- Your annotation goal does not require fragment-based matching (e.g., accurate-mass-only matching without spectral context).

## Inputs

- xcms object (XCMS class, containing peak-picked feature data with m/z, retention time, and intensity)
- RamClustR object (RC class, containing pseudo-MS/MS spectra as fragment ion lists with intensities)
- raw LC-MS all-ion fragmentation chromatograms in centroid mode (mzML, mzXML, or CDF format)

## Outputs

- integrated xcms object (R object class: XCMS)
- integrated RamClustR object (R object class: RC, with pseudo-MS/MS spectra linked to features)
- feature annotation-ready data structure (suitable for annotateRC function input)

## How to apply

Load the preprocessed xcms object (containing peak-picked feature data) and the RamClustR object (containing pseudo-MS/MS spectra derived from AIF) into the R environment. The xcms object should have been processed with default noise thresholds (noise = 0.005) and marker peak thresholds (mpeaksThres = 0.1). Verify that both objects contain consistent feature indexing and that the RamClustR object contains fragment ion intensity arrays corresponding to each feature. These paired objects are then passed together to downstream annotation functions like annotateRC, which uses the xcms object for peak intensity context and the RamClustR object for fragment matching against ion libraries. The integration ensures that fragment-based candidate scoring reflects both the observed fragmentation pattern and the feature's chromatographic/mass properties.

## Related tools

- **xcms** (Peak detection and feature alignment from raw LC-MS chromatograms; produces xcms object with m/z and intensity matrices) — https://bioconductor.org/packages/xcms/
- **RamClustR** (Clustering of co-eluting ions and generation of pseudo-MS/MS spectra from all-ion fragmentation data; produces RC object with fragment ion arrays) — https://github.com/caerusmatthew/RAMClustR
- **MetaboAnnotatoR** (Fragment-based metabolite annotation function (annotateRC) that consumes integrated xcms and RamClustR objects and matches fragments against ion libraries) — https://github.com/gggraca/MetaboAnnotatoR

## Examples

```
# Load preprocessed xcms and RamClustR objects
load('xset.RData')  # xcms object
load('RC.RData')    # RamClustR object
# Verify integration: check that xset and RC share feature indices
head(xset@features)
head(RC$mz)
```

## Evaluation signals

- Both xcms and RamClustR objects load without errors and share identical feature indices (same m/z values and retention times for corresponding features).
- RamClustR object contains non-empty pseudo-MS/MS spectra for ≥50% of detected features (indicating successful spectral clustering).
- xcms object peak intensities and RamClustR fragment intensities are present and non-zero for features selected for annotation.
- Downstream annotateRC function executes without dimension mismatch or missing-value errors when passed the integrated objects.
- Output annotation results show ≥30% of features receiving at least one candidate annotation (indicating successful fragment matching; task_001 observed 50% success rate for six test features).

## Limitations

- Integration requires raw chromatograms in centroid mode; profile-mode data will produce spurious or empty pseudo-MS/MS spectra in RamClustR.
- Feature correspondence between xcms and RamClustR depends on identical preprocessing parameters (same noise thresholds, retention time windows); mismatched parameters create index drift and failed annotations.
- RamClustR clustering quality is sensitive to the presence of chemical noise, isotopologue patterns, and in-source fragmentation; poorly clustered pseudo-spectra yield low-confidence fragment matches.
- No automated validation mechanism is provided to verify object consistency; manual inspection of shared feature indices is recommended before downstream analysis.
- No changelog or version history is available for either xcms or RamClustR in the documented codebase, limiting reproducibility across software versions.

## Evidence

- [intro] An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages: "An example of feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages"
- [intro] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [intro] a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data: "a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data"
- [intro] Peak-picking above noise level threshold (default: 0.005) and marker peak threshold (default: 0.1): "Peak-picking above noise level threshold (default: 0.005) and Peak-picking above marker peak threshold (default: 0.1)"
- [intro] annotations can be performed using the annotateRC function: "annotations can be performed using the *annotateRC* function"
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [readme] This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases.: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases."
