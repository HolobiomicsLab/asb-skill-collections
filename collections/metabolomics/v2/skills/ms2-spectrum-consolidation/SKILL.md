---
name: ms2-spectrum-consolidation
description: Use when after sample alignment and feature grouping steps in untargeted LC-MS workflows, when you have DDA-mode raw files with both MS1 and MS2 scans and need to link tandem mass spectra to quantified features for annotation and structural characterization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - Centwave (XCMS)
  - ProteoWizard
  - SLAW (zamboni-lab/SLAW)
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
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
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

# MS2 Spectrum Consolidation

## Summary

Consolidates and extracts MS2 spectra from DDA LC-MS experiments by mapping MS2 scans to aligned MS1 features and pooling reference spectra across samples. This produces a unified MS2 spectral library indexed to the quantitative feature table, enabling spectral annotation and confidence scoring for identified metabolites.

## When to use

After sample alignment and feature grouping steps in untargeted LC-MS workflows, when you have DDA-mode raw files with both MS1 and MS2 scans and need to link tandem mass spectra to quantified features for annotation and structural characterization. Particularly relevant when processing multi-sample cohorts where MS2 evidence is sparse or distributed unevenly across replicates.

## When NOT to use

- Input data are in DIA-MS (data-independent acquisition) mode; SLAW skips DIA-MS2 spectra extraction
- Raw files are in profile mode (not centroided); pre-process with ProteoWizard vendor peak picking filter first
- No MS2 scans present in the input files (MS1-only experiments)
- Input features are already a finalized feature table without access to raw MS data or aligned feature coordinates

## Inputs

- Centroided mzML files with MS1 and DDA-MS2 scans (positive or negative polarity, not mixed)
- Aligned feature table with m/z, retention time, and feature group IDs from prior alignment step
- Samples metadata (samples.csv) optionally specifying which files to prioritize for MS2 (e.g., 'MS2' file type)
- Isotopologue/adduct grouping annotations from prior grouping step

## Outputs

- Consolidated MS2 spectra in mzML or MGF format indexed by aligned feature ID
- Fused MGF file containing one consensus MS2 spectrum per feature group
- Annotation table mapping feature IDs to MS2 metadata (precursor m/z, collision energy, scan count, etc.)
- Updated feature table with MS2 reference information and isotopic annotations

## How to apply

SLAW consolidation works in two phases: (1) During the main pipeline, MS2 scans are extracted from DDA files and mapped to the aligned MS1 feature coordinates (m/z and retention time) that were established during sample alignment. (2) For each aligned feature group (isotopologue/adduct cluster), all MS2 spectra associated with that feature across all samples are pooled and stored as a consensus spectrum, indexed by feature ID. The mapping uses the aligned m/z and retention time windows to link precursor ions to product ion spectra. DIA-MS and profile-mode data are excluded; only centroided DDA data in mzML format are processed. Files marked as 'MS2' type in the samples.csv input can be flagged for MS2-only extraction without contributing to MS1 quantification. Export includes consolidated MS2 reference information linked to the feature table via feature ID.

## Related tools

- **Centwave (XCMS)** (Wrapped peak picking algorithm; MS2 extraction depends on accurate MS1 feature detection)
- **ProteoWizard** (Pre-processing tool to centroid vendor profile data and filter MS levels (e.g., peakPicking vendor msLevel=1-2))
- **SLAW (zamboni-lab/SLAW)** (End-to-end containerized workflow orchestrating MS2 consolidation as final step) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- All MS2 spectra in output files map to feature IDs present in the aligned feature table; no orphaned spectra
- Precursor m/z of consolidated spectra fall within the aligned m/z window ± tolerance of their associated MS1 feature
- Retention time of MS2 scans lie within the aligned retention time window for their feature group
- Number of MS2 spectra per feature is ≥1 (at least one sample contributed MS2 evidence to the consensus)
- Fused MGF file contains one spectrum entry per unique aligned feature group; no duplicate feature IDs
- Files marked 'MS2' type in samples.csv contribute spectra to consolidation but do not inflate MS1 quantification

## Limitations

- DIA-MS data are not supported; only DDA mode is processed. DIA-MS2 spectra are skipped
- Profile-mode (non-centroided) data must be centroided externally (e.g., via ProteoWizard) before input to SLAW
- All input files must be of the same polarity (positive or negative). Mixed-polarity datasets must be split and processed separately
- MS2 spectra are consolidated at the aligned feature group level; high-resolution separation of isomers or isobars sharing precursor m/z is limited by prior alignment and grouping quality
- Sparse or uneven MS2 coverage across samples may result in weak consensus spectra for low-abundance features or undersampled time points

## Evidence

- [other] SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data recursion, and extraction of consolidated MS2 spectra and isotopic data.: "extraction of consolidated MS2 spectra and isotopic data"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data: "extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped)"
- [readme] Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported. All data must be centroided and of unique polarity.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
- [readme] MS2: indicates files that include primarily MS2 spectra and should not be considered for MS1 peak picking and quantification. MS2 spectra will be mapped to MS1 features (identified in QC and samples) after alignment.: "MS2 spectra will be mapped to MS1 features (identified in QC and samples) after alignment."
- [readme] The outputs are generated in PATH_OUTPUT the complete outputs are: datamatrices: The complete table with row corresponding to features or ions and the columns corresponding to a sample. Three flavors of datamatrices are generated. fused_mgf: The consensus mfg spectra obtained, storing one ms-ms spectrum by features in the data matrices.: "fused_mgf: The consensus mfg spectra obtained, storing one ms-ms spectrum by features in the data matrices."
