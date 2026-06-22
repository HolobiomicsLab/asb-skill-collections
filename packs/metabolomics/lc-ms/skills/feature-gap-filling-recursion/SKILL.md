---
name: feature-gap-filling-recursion
description: Use when after sample alignment has established consensus m/z and retention time coordinates, and after grouping of isotopologues and adducts is complete.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-gap-filling-recursion

## Summary

Gap-filling by data recursion recovers missing peaks at aligned feature locations across LC-MS samples by re-interrogating raw data at consensus m/z and retention time coordinates. This step completes the feature matrix after alignment and isotopologue grouping, ensuring quantitative data continuity across the cohort.

## When to use

After sample alignment has established consensus m/z and retention time coordinates, and after grouping of isotopologues and adducts is complete. Use this skill when you have aligned feature locations but observe missing intensity values (zeros or NAs) in the feature table for samples where the metabolite should theoretically be present based on detection in other samples in the cohort.

## When NOT to use

- Do not apply gap-filling if the feature table is already complete (no missing values across samples) — it would be computationally wasteful.
- Do not apply gap-filling to DIA-MS data or profile-mode LC-MS; SLAW gap-filling is designed for centroided DDA data only.
- Do not use gap-filling as a substitute for proper peak picking parameter optimization; if most peaks are missing, re-optimize peak picker parameters instead of relying on recursive recovery.

## Inputs

- Aligned feature table with consensus m/z, retention time, and sample membership
- Raw LC-MS data (mzML/mzXML format, centroided)
- Isotopologue and adduct grouping annotations
- Mass and retention time tolerance parameters from alignment

## Outputs

- Consolidated feature matrix with missing peak intensities filled
- Gap-filling metadata (which features were filled in which samples)
- Updated feature intensity table ready for downstream statistical analysis

## How to apply

For each aligned feature group (defined by consensus m/z and retention time), recursively query the raw LC-MS data at the aligned location in samples where no peak was detected in the initial picking pass. Extract the intensity value at that m/z and retention time coordinate window (using mass and time tolerances derived from the alignment step) and populate the missing value in the feature matrix. The recursion leverages the consensus coordinates learned from samples where the feature *was* detected, avoiding re-parameterization of the peak picker and ensuring consistency. Apply this after isotopologue and adduct grouping so that gap-filling respects the consolidated feature identities rather than filling noise or chemical noise artifacts.

## Related tools

- **Centwave** (Initial peak picking algorithm; gap-filling uses Centwave's detected peaks and tolerances to define aligned coordinates)
- **FeatureFinderMetabo** (Alternative initial peak picking algorithm; gap-filling uses detected peaks and tolerances from this algorithm if selected)
- **ADAP** (Alternative initial peak picking algorithm; gap-filling uses detected peaks and tolerances from this algorithm if selected)
- **SLAW** (Container orchestrating the complete workflow including automated gap-filling parameter optimization) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Feature matrix completeness: confirm that the fraction of missing (zero/NA) values in the final feature table is substantially reduced compared to the pre-gap-filling state.
- Mass accuracy of filled peaks: verify that filled intensity values correspond to the correct consensus m/z within the specified mass tolerance window (e.g., ±5 ppm).
- Retention time consistency: confirm that filled peaks appear at the consensus retention time ± the alignment tolerance window, not at arbitrary or off-target times.
- Quantitative plausibility: check that filled intensities are within the dynamic range observed for that feature in other samples; extreme outliers suggest incorrect feature matching.
- No artifactual features: validate that gap-filling did not create spurious peaks by filling at m/z and time coordinates that fall in chemical noise or blank regions.

## Limitations

- Gap-filling depends on the quality of sample alignment; poor alignment produces incorrect consensus coordinates, leading to filled peaks at wrong m/z or retention time locations.
- Gap-filling cannot recover truly absent peaks (e.g., due to sample loss or instrument malfunction); it only fills peaks that exist in raw data but were missed by the initial peak picker.
- The method requires that at least some samples detected the feature reliably; if a feature is present in only one sample, alignment will be weak and gap-filling may fail to recover it in other samples.
- Gap-filling is optimized for DDA experiments with centroided data; profile data or DIA-MS data types are not supported by SLAW and will produce incorrect results.
- Very low-abundance features may be filled with noise if the mass and retention time tolerance windows are too permissive; tolerance tuning via automated parameter optimization is recommended.

## Evidence

- [intro] gap-filling by data recursion at aligned feature locations across samples: "Group detected peaks by isotopologue and adduct relationships using mass difference and intensity ratio criteria. 5. Fill missing peaks via data recursion gap-filling at aligned feature locations"
- [other] Gap-filling is one of the six sequential processing steps in SLAW: "SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data"
- [intro] Automated parameter optimization for gap-filling: "Automated parameter optimization for picking, alignment, gap-filling"
- [readme] Gap-filling is part of the complete processing workflow: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic"
- [readme] Centroided mzML input format requirement: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
