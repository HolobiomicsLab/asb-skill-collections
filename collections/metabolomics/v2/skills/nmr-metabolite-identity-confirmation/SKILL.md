---
name: nmr-metabolite-identity-confirmation
description: Use when you have preprocessed 1H NMR spectral data with an unknown or ambiguous peak (e.g., at a specific chemical shift δ), and you need to determine its chemical identity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Bioconductor
  - MWASTools
  - TopSpin 3.2
derived_from:
- doi: 10.1093/bioinformatics/btx477
  title: MWASTools
evidence_spans:
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
- '"MWASTools" is an R package designed to provide an integrated and user-friendly pipeline'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-metabolite-identity-confirmation

## Summary

Use Statistical Total Correlation Spectroscopy (STOCSY) to confirm the chemical identity of unknown NMR signals by analyzing their covariance and correlation patterns with a known driver signal. This skill resolves ambiguous metabolic features to specific metabolites through spectral correlation analysis.

## When to use

Apply this skill when you have preprocessed 1H NMR spectral data with an unknown or ambiguous peak (e.g., at a specific chemical shift δ), and you need to determine its chemical identity. STOCSY is particularly useful when the unknown signal's identity cannot be established by chemical shift alone, but you suspect it correlates structurally with another known metabolite signal (e.g., amino acids with characteristic multiplet patterns like valine's doublets).

## When NOT to use

- Raw (unphased, unbaseline-corrected) NMR spectra — preprocessing must be completed in TopSpin or equivalent before STOCSY is reliable.
- Spectral data from metabolites without distinctive multiplet structures or covariance patterns — STOCSY relies on correlated spin systems; singlets or isolated peaks will not generate informative correlation profiles.
- When only a single isolated peak exists for a metabolite — STOCSY requires at least two structurally correlated signals to establish identity; use chemical shift databases or 2D NMR (COSY, HSQC) instead.

## Inputs

- Preprocessed 1H NMR spectral data matrix (phased and baseline-corrected)
- Chemical shift value (ppm) of driver signal
- Spectral metadata (e.g., ppm scale, number of scans)

## Outputs

- STOCSY correlation coefficient profile across chemical shifts
- Annotated STOCSY plot with identified metabolite peaks and correlation values
- Extracted correlation data table (ppm vs. correlation coefficient)
- Metabolite identity assignment with confidence based on peak matching

## How to apply

Load preprocessed NMR spectral data (formatted as a matrix or phased/baseline-corrected spectra) into R with Bioconductor. Select a driver signal at a known chemical shift (e.g., δ 1.04 for valine) that belongs to the target metabolite. Apply the STOCSY function with the query ppm parameter set to the driver signal's chemical shift, generating a correlation coefficient profile across the entire spectral range. Extract and visualize the resulting correlation spectrum to identify secondary peaks that co-vary with the driver signal. Cross-reference the identified secondary peaks (e.g., δ 0.99) against literature valine signatures and known multiplet patterns. Generate an annotated STOCSY plot showing metabolite assignments and export the correlation coefficient data for downstream reporting.

## Related tools

- **MWASTools** (R/Bioconductor package providing STOCSY function and integrated metabolite assignment workflow) — github.com/AndreaRMICL/MWASTools
- **R** (Programming environment for loading, manipulating, and analyzing NMR spectral data; STOCSY requires R >= 3.3)
- **Bioconductor** (Dependency for statistical and metabolomic analysis functions used by MWASTools)
- **TopSpin 3.2** (Bruker NMR acquisition and processing software for phasing and baseline correction prior to STOCSY)

## Examples

```
library(MWASTools); stocsy_result <- STOCSY(metabo_SE, query.ppm = 1.04); plot(stocsy_result); annotated_peaks <- extract_correlation_peaks(stocsy_result, threshold = 0.7)
```

## Evaluation signals

- Identified secondary peaks in the STOCSY correlation profile exhibit strong correlation coefficients (typically r > 0.7 or equivalent threshold) with the driver signal, indicating robust covariance.
- Secondary peaks match known literature chemical shifts for the target metabolite (e.g., valine doublets at δ 1.04 and δ 0.99 ± 0.02 ppm tolerance).
- Correlation pattern is specific to the driver signal — peaks from non-related metabolites should show weak or near-zero correlation coefficients.
- STOCSY plot annotations are reproducible when the analysis is repeated with the same driver signal and preprocessed spectral dataset.
- Extracted metabolite identity does not contradict complementary identification methods (e.g., 1D chemical shift ranges, reference spectra, or orthogonal 2D NMR data when available).

## Limitations

- STOCSY requires preprocessed, phased, and baseline-corrected NMR spectra; poor spectral quality or inadequate preprocessing will yield unreliable correlation profiles.
- The skill is most effective for metabolites with distinctive multiplet structures (e.g., amino acids); singlets and overlapping signals from structurally unrelated metabolites may confound assignment.
- Correlation strength depends on sample composition and relative metabolite concentrations; low-abundance metabolites may generate weak or noisy STOCSY signals.
- STOCSY does not provide stereochemical resolution (e.g., cannot distinguish enantiomers or diastereomers with identical spin systems).
- The choice of driver signal ppm is critical; incorrect driver signal selection or misalignment to phasing/calibration will produce false or uninformative correlation patterns.

## Evidence

- [intro] STOCSY application and driver signal selection: "metabolite assignment using Statistical Total Correlation Spectroscopy (STOCSY)"
- [other] STOCSY identifies covariance through correlation of unknown features with known driver signals: "STOCSY analysis using δ 1.04 as the driver signal identified two highlighted doublets at δ 1.04 and δ 0.99, indicating the unknown signal corresponds to valine"
- [abstract] Integration of STOCSY into MWASTools workflow for metabolite confirmation: "Key functionalities of the package include: quality control analysis; metabolite-phenotype association models; data visualization tools; and metabolite assignment using statistical total correlation"
- [intro] Preprocessing and software environment requirements: "Assuming that R (>=3.3) and Bioconductor have been correctly installed"
- [intro] NMR instrument and preprocessing workflow: "Following phasing and baseline correction in TopSpin 3.2 software"
