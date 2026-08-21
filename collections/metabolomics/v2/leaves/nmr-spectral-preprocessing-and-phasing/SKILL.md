---
name: nmr-spectral-preprocessing-and-phasing
description: Use when when working with raw 1H NMR FID data acquired on instruments
  like Bruker Avance spectrometers that require baseline correction, phase adjustment,
  and signal alignment before metabolite identification or statistical association
  testing can proceed reliably.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Bioconductor
  - MWASTools
  - TopSpin 3.2
  - Bruker Avance III 600 MHz
  - R/Bioconductor
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly
  pipeline'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  dedup_kept_from: coll_mwastools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btx477
  all_source_dois:
  - 10.1093/bioinformatics/btx477
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectral-preprocessing-and-phasing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Preprocessing and phasing of raw 1H NMR spectra to remove instrumental artifacts and align signals for downstream metabolomic analysis. This foundational step prepares FID data for quantitative metabolite assignment and association modeling.

## When to use

When working with raw 1H NMR FID data acquired on instruments like Bruker Avance spectrometers that require baseline correction, phase adjustment, and signal alignment before metabolite identification or statistical association testing can proceed reliably.

## When NOT to use

- Spectrum is already preprocessed and baseline-corrected (e.g., from a vendor preprocessing pipeline)
- Input is a feature table or binned spectral matrix rather than raw FID data
- Analysis does not require quantitative chemical shift alignment (e.g., purely qualitative metabolite detection)

## Inputs

- Raw 1H NMR FID (free induction decay) data from Bruker Avance spectrometer
- Acquisition parameters (field strength, pulse sequence, number of scans)

## Outputs

- Phase-corrected 1H NMR spectrum (netCDF or Bruker format)
- Baseline-corrected spectral intensity array
- Processed spectral data ready for metabolite assignment and MWAS

## How to apply

Load raw NMR FID data into TopSpin 3.2 or equivalent Bruker acquisition software. Apply phase correction (0-order and 1-order phasing) to align the real component of the spectral baseline to zero across the chemical shift range. Perform baseline correction to remove baseline drift and distortion artifacts. Export the phased and baseline-corrected spectrum in a standard format (e.g., netCDF or Bruker format) compatible with downstream R/Bioconductor pipelines. Verify that the resulting spectrum exhibits flat baseline, symmetric peaks, and chemical shift alignment consistent with reference standards before proceeding to metabolite assignment or statistical analysis.

## Related tools

- **TopSpin 3.2** (Bruker NMR acquisition and processing software for phase correction and baseline adjustment of raw FID data)
- **Bruker Avance III 600 MHz** (NMR spectrometer platform that acquires raw 1H NMR plasma spectra requiring downstream preprocessing)
- **R/Bioconductor** (Environment for loading and further processing preprocessed NMR spectral data for metabolite assignment and statistical analysis)
- **MWASTools** (R package that accepts preprocessed NMR spectral data for quality control, metabolite-phenotype association, and STOCSY-based metabolite assignment) — github.com/AndreaRMICL/MWASTools

## Evaluation signals

- Baseline is flat and centered near zero across the entire chemical shift range (typically 0–10 ppm for 1H NMR)
- Peak line shapes are symmetric and Lorentzian without phase distortion (left-to-right asymmetry)
- Chemical shift values align with literature references for known metabolites (e.g., valine doublets at δ 1.04 and δ 0.99)
- Signal-to-noise ratio is preserved and artifact peaks (spinning sidebands, solvent residuals) are minimized
- Spectral integration and peak area quantitation are consistent across replicate samples and known standards

## Limitations

- Phase correction quality depends on acquisition parameters and field homogeneity; poorly shimmed samples may yield residual phase distortion
- Baseline correction can introduce artifacts if solvent peaks or strong metabolite signals are improperly handled
- TopSpin 3.2 is proprietary software; preprocessing workflows are vendor-specific and not portable to open-source alternatives without additional conversion steps
- No automated quality control metrics provided in the article; manual inspection or downstream statistical outlier detection is required to identify failed preprocessing

## Evidence

- [intro] Following phasing and baseline correction in TopSpin 3.2 software: "Following phasing and baseline correction in TopSpin 3.2 software"
- [intro] 1H NMR plasma spectra were acquired on a Bruker Avance III 600 MHz spectrometer: "<sup>1</sup>H NMR plasma spectra were acquired on a Bruker Avance III 600 MHz spectrometer"
- [other] Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor: "Load the preprocessed NMR spectral data (metabo_SE) into R with Bioconductor"
- [intro] metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY): "metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)"
