---
name: spectral-preprocessing-for-machine-learning
description: Use when when preparing raw MS2 spectra (m/z and intensity pairs) for kernel-based scoring methods such as IOKR, especially when the training dataset is large and represents diverse ion types.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - GNPS
  - Chemistry Development Kit (CDK)
  - NPLinker
  - Probability Product Kernel (PPK)
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
---

# spectral-preprocessing-for-machine-learning

## Summary

Filter MS2 spectra to retain only peaks present in the training dataset before applying machine learning kernels, reducing noise and computational cost while leveraging the statistical coverage of the training set. This denoising step precedes Probability Product Kernel (PPK) computation to normalize peak diversity and avoid spurious signal.

## When to use

When preparing raw MS2 spectra (m/z and intensity pairs) for kernel-based scoring methods such as IOKR, especially when the training dataset is large and represents diverse ion types. Apply this skill when computational efficiency is a concern and the training data covers sufficient chemical diversity to avoid introducing severe bias.

## When NOT to use

- Input spectra are already preprocessed or contain only highly abundant peaks — avoid re-filtering to prevent over-denoising.
- Training dataset is small or unrepresentative of the chemical space of interest — filtering would introduce unacceptable bias.
- Peak annotation or fragmentation tree computation is the downstream task — this filter may remove diagnostic peaks needed for structural elucidation.

## Inputs

- Raw MS2 spectrum (m/z and intensity pairs, e.g., .mzML or tabular format)
- IOKR training dataset peak list (m/z values extracted from GNPS library spectra with structural annotations)

## Outputs

- Denoised MS2 spectrum (tabular: m/z, intensity, PPK kernel weight)
- Preprocessing validation summary (number of peaks retained, fraction of signal, weight statistics)

## How to apply

Load the input MS2 spectrum and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum whose m/z values match peaks in the training data using exact matching or a specified mass tolerance (e.g., ±0.1 Da). Retain only matched peaks and remove all others. Apply Probability Product Kernel (PPK) denoising to the filtered peak list to reweight intensities based on likelihood in the training set. Output the preprocessed spectrum as a tabular file (m/z, intensity, kernel weight) and generate a validation summary reporting the number of peaks retained, fraction of signal preserved, and PPK weight distribution. The underlying rationale is that while this filtering theoretically introduces training-set bias, the large size and chemical diversity of public libraries like GNPS mean the effect is negligible in practice, and the benefit in noise reduction and computational speed outweighs the bias.

## Related tools

- **GNPS** (Source of library MS2 spectra and training dataset peak lists with structural annotations)
- **Chemistry Development Kit (CDK)** (Mass tolerance matching and m/z peak alignment)
- **NPLinker** (Downstream framework integrating preprocessed spectra for BGC–metabolite linking via IOKR scoring) — https://github.com/NPLinker/nplinker
- **Probability Product Kernel (PPK)** (Kernel-based reweighting of filtered peaks to adjust intensities by likelihood in training set)

## Evaluation signals

- Peak retention fraction is consistent across replicate spectra of the same compound (e.g., >60% of peaks retained for well-represented metabolite classes).
- PPK kernel weights follow the expected distribution (higher weights for abundant training peaks, lower for rare ones; mean kernel weight should differ significantly between validated and random links, as shown by p-value < 0.01).
- Downstream IOKR scoring improves discrimination between validated and false BGC–spectrum links (e.g., top-1 accuracy >0.10, AUC >0.60, compared to random baseline AUC ~0.52).
- m/z matching is reproducible: rerunning with the same mass tolerance yields identical peak sets.
- Output validation summary reports 0 unmatched peaks (all input peaks either retained or explicitly filtered) and PPK weights sum to 1.0 or are bounded in [0, 1].

## Limitations

- Training set bias: filtering to training-set peaks theoretically excludes novel chemistry outside the training distribution, reducing sensitivity for rare or previously undiscovered natural products.
- Kernel and parameter selection for PPK significantly affect performance but are not fully characterized; the choice of mass tolerance, kernel function, and parameter values requires empirical validation.
- Reliance on training set quality and coverage: if the training dataset (e.g., GNPS library) is skewed toward certain compound classes or ionization modes, the filtered spectra will inherit that bias.
- No stratification by compound class: current filtering approach does not account for differences in peak diversity across natural product types (e.g., polyketides vs. non-ribosomal peptides), potentially disadvantaging underrepresented classes.

## Evidence

- [abstract] Input MS2 spectra denoising and filtering: "Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation."
- [abstract] Workflow steps for peak filtering: "Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum"
- [abstract] PPK denoising application: "Apply the Probability Product Kernel (PPK) denoising step to the filtered peak list to adjust weights based on likelihood in the training set."
- [abstract] Training set size justification: "While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the"
- [abstract] Purpose of filtering: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability"
- [readme] Installation and environment setup: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
