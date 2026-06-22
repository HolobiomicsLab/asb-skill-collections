---
name: lcms-feature-table-construction
description: Use when you have centroided, single-polarity mzML files from DDA LC-MS experiments and need to generate a quantitative feature table with aligned m/z and retention time coordinates, isotopic annotations, and MS2 spectra for downstream statistical or annotation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - ProteoWizard
  techniques:
  - LC-MS
  - tandem-MS
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

# lcms-feature-table-construction

## Summary

Build a consolidated feature table from untargeted LC-MS data by sequentially performing peak picking, sample alignment, isotopologue/adduct grouping, gap-filling, and MS2 annotation across all samples. This skill transforms raw mzML files into quantitative data matrices suitable for metabolomic analysis.

## When to use

You have centroided, single-polarity mzML files from DDA LC-MS experiments and need to generate a quantitative feature table with aligned m/z and retention time coordinates, isotopic annotations, and MS2 spectra for downstream statistical or annotation analysis. Use this when you want to process multiple samples in a single containerized, self-optimizing workflow rather than tuning parameters individually.

## When NOT to use

- Input data are profile-mode (non-centroided) mzML files — convert to centroid format first via ProteoWizard.
- Input includes DIA-MS2 data — SLAW processes DDA only; DIA-MS2 spectra are skipped.
- Input contains mixed polarity data — SLAW requires all data to be of unique polarity; process positive and negative modes separately.
- You have already constructed an aligned feature table from another workflow — this skill duplicates that work.

## Inputs

- centroided mzML files (DDA mode, single polarity)
- samples.csv file (two columns: filename and type [QC|sample|MS2|blank])
- parameters.txt file (specifies algorithm, optimization flags, parameter ranges)

## Outputs

- feature table (data matrix with features as rows, samples as columns, intensity values)
- alignment metadata (consensus m/z and retention time per feature)
- isotopic annotations (isotopologue and adduct relationships)
- consolidated MS2 spectra (consensus or representative spectra per feature)
- individual peak tables and MS2 spectra per sample (OPENMS/CENTWAVE/ADAP subdirectories)

## How to apply

Load centroided mzML files (obtained via ProteoWizard with vendor peakPicking) into the SLAW container, along with a samples.csv file annotating file types (QC, sample, MS2, blank) and a parameters.txt file specifying optimization settings. Execute the six-step pipeline: (1) peak picking using one of three wrapped algorithms (Centwave, FeatureFinderMetabo, or ADAP) with automated parameter optimization on QC samples; (2) sample alignment to establish consensus retention time and m/z coordinates; (3) repeat peak picking for consistency; (4) group detected peaks by isotopologue and adduct relationships using mass difference and intensity ratio criteria; (5) fill missing peaks via data recursion at aligned feature locations; (6) extract and consolidate MS2 spectra and isotopic data for each feature. Export the final feature table containing peak intensities, alignment metadata, isotopic annotations, and MS2 reference information.

## Related tools

- **Centwave** (One of three wrapped peak picking algorithms for detecting LC-MS features; selected via parameters.txt)
- **FeatureFinderMetabo** (One of three wrapped peak picking algorithms for detecting LC-MS features; selected via parameters.txt)
- **ADAP** (One of three wrapped peak picking algorithms for detecting LC-MS features; selected via parameters.txt)
- **ProteoWizard** (Converts vendor raw mass spectrometry data to centroided mzML format required by SLAW; use filter 'peakPicking vendor msLevel=1-2')

## Examples

```
docker run --rm -v /path/to/mzML/files:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Feature table dimensions: number of rows (features) and columns (samples) are consistent with input file count; no empty or duplicate rows.
- Alignment metadata: all features have assigned consensus m/z (within expected instrument resolution, typically < 5 ppm for high-resolution MS) and retention time values; retention times are monotonically increasing or clustered appropriately by sample.
- Isotopic annotations: detected isotopologues have mass differences consistent with 13C, 2H, or 15N shifts; intensity ratios between isotope peaks follow expected natural abundance patterns (e.g., M+1 ≈ 1.1% for singly charged features).
- Gap-filling efficacy: features detected in QC samples are present across most study samples; missing values are filled at aligned locations, reducing NAs in the feature table.
- MS2 annotation: consolidated MS2 spectra are associated with the correct parent ion m/z and retention time; spectrum quality (number of fragments, signal intensity) is consistent with DDA acquisition parameters.

## Limitations

- SLAW processes DDA experiments only; DIA-MS2 spectra are skipped during consolidation.
- All input data must be centroided and of a single polarity; mixed-polarity or profile-mode files will cause errors or be incorrectly processed.
- Parameter optimization requires QC samples (pooled or reference materials); if no QC samples are defined, SLAW selects random samples, potentially degrading alignment quality.
- Automated parameter optimization can be time-consuming (up to ~1 hour per dataset); optimization is disabled by default.
- Gap-filling by data recursion may introduce false positives if features are aligned incorrectly or if noise peaks are mistaken for true signals; manual inspection of low-intensity or rarely detected features is recommended.

## Evidence

- [other] SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data recursion, and extraction of consolidated MS2 spectra and isotopic data.: "SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data"
- [other] Load LC-MS sample files (mzML/mzXML format) into the SLAW pipeline. Execute peak picking using one of the three wrapped algorithms (Centwave, FeatureFinderMetabo, or ADAP) with automated parameter optimization.: "Load LC-MS sample files (mzML/mzXML format) into the SLAW pipeline. Execute peak picking using one of the three wrapped algorithms (Centwave, FeatureFinderMetabo, or ADAP) with automated parameter"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
- [other] Extract and consolidate MS2 spectra and isotopic data for each aligned feature group. Export the consolidated feature table with peak intensities, alignment metadata, isotopic annotations, and MS2 reference information.: "Extract and consolidate MS2 spectra and isotopic data for each aligned feature group. Export the consolidated feature table with peak intensities, alignment metadata, isotopic annotations, and MS2"
- [readme] DDA only). It was developed by Alexis Delabriere in the Zamboni Lab at ETH Zurich.: "SLAW is a scalable, containerized workflow for untargeted LC-MS processing (DDA only)."
- [readme] If no QC samples are defined, or the samples.csv is missing, SLAW will pick random sample files.: "If no QC samples are defined, or the samples.csv is missing, SLAW will pick random sample files."
