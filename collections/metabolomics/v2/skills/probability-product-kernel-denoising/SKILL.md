---
name: probability-product-kernel-denoising
description: Use when you have raw MS2 spectra (m/z and intensity pairs) that you want to match against a large training dataset of annotated library spectra (e.g., GNPS), and you need to reduce noise and computational burden before applying kernel-based scoring methods such as IOKR.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - GNPS
  - Chemistry Development Kit (CDK)
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based on properties absent from an MS2 spectrum,
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
- 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development Kit [29]. The fingerprint vector is composed of three concatenated sets of fingerprints: CDK Substructure,'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# probability-product-kernel-denoising

## Summary

Denoise MS2 spectra by retaining only peaks present in a training dataset, then reweight peaks using a Probability Product Kernel (PPK) that adjusts intensities based on ion likelihood in the training set. This filtering reduces computational cost and noise while preserving signal diversity sufficient for downstream scoring.

## When to use

You have raw MS2 spectra (m/z and intensity pairs) that you want to match against a large training dataset of annotated library spectra (e.g., GNPS), and you need to reduce noise and computational burden before applying kernel-based scoring methods such as IOKR. Use this skill when the training set is large enough to contain robust ion diversity and you can tolerate the small bias toward training-set patterns.

## When NOT to use

- The training dataset is small or not representative of your sample's ion chemistry — the filtering will lose signal diversity.
- You require an unbiased, unfiltered representation of the original spectrum for independent validation or method comparison.
- Your input spectra are already preprocessed or come from a different analytical platform with incompatible m/z calibration.

## Inputs

- MS2 spectrum (m/z and intensity pairs)
- Training dataset peak list (from GNPS library spectra with structural annotations)
- Mass tolerance parameter (e.g., ppm or Da)

## Outputs

- Denoised MS2 spectrum (m/z, intensity, kernel weight triples)
- Validation summary (count of retained vs. removed peaks, kernel weight statistics)

## How to apply

Load the input MS2 spectrum and the training dataset peak list (e.g., extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum whose m/z values match peaks in the training data within a specified mass tolerance (exact match or tolerance-based). Retain only the matched peaks and remove all other peaks. Apply the Probability Product Kernel by reweighting each retained peak's intensity according to its likelihood in the training set, producing a denoised spectrum with adjusted kernel weights. Output the filtered spectrum as a tabular file (m/z, intensity, kernel weight) and a validation summary; this denoised output is then passed to downstream scoring steps such as IOKR.

## Related tools

- **GNPS** (Source of library MS2 spectra and training dataset peak lists with structural annotations)
- **Chemistry Development Kit (CDK)** (Molecular fingerprint generation and chemical structure processing for kernel computation)
- **NPLinker** (Framework that integrates PPK-denoised spectra into IOKR scoring for genomic-metabolomic linking) — https://github.com/NPLinker/nplinker

## Evaluation signals

- Peak retention rate: verify that the filtered spectrum retains a meaningful fraction of the original peaks (typically >10% depending on training set coverage) and that this fraction is consistent with training-set size.
- Kernel weight distribution: check that kernel weights are non-negative, bounded, and show higher values for peaks frequent in the training set and lower values for rare peaks.
- Downstream IOKR performance: confirm that IOKR scores computed on PPK-denoised spectra show improved top-n accuracy and AUC compared to undenoised spectra or random baselines.
- m/z matching accuracy: validate that peak-matching logic correctly identifies training peaks within the specified mass tolerance (e.g., confirm a sample of matched pairs by manual inspection of m/z differences).
- Output file schema: ensure output tabular file contains exactly three columns (m/z, intensity, kernel weight) with consistent numeric precision and no missing values.

## Limitations

- Filtering biases the model toward the training set; while the training set is large enough to contain robust ion diversity, the bias effect is non-negligible for rare or novel metabolites not well-represented in GNPS.
- IOKR kernel function and parameter selection significantly affect performance but choices are not fully characterized; suboptimal kernel choice can degrade denoising effectiveness.
- Mass tolerance parameter choice is critical: too tight a tolerance will lose valid peaks; too loose will retain spurious matches. Optimal tolerance depends on MS instrument calibration and mass accuracy.
- Applicability is limited to spectra whose peaks are likely to overlap with the training set; spectra from novel chemical space or non-standard ionization modes may retain few or no peaks after filtering.

## Evidence

- [other] Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation.: "Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation."
- [other] Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum whose m/z values match peaks present in the training data (exact or within a specified mass tolerance). Retain only the matched peaks and remove all other peaks from the spectrum. Apply the Probability Product Kernel (PPK) denoising step to the filtered peak list to adjust weights based on likelihood in the training set.: "Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum"
- [other] While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the bias effect is small.: "While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the"
- [abstract] to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures: "IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures"
