---
name: ms2-spectrum-peak-filtering-by-training-set-membership
description: Use when when you have raw MS2 spectra (m/z and intensity pairs) and
  need to compute a Probability Product Kernel score or other fragmentation-based
  similarity metric against a training dataset of known spectra (e.g., GNPS library
  spectra with structural annotations).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0208
  tools:
  - GNPS
  - Chemistry Development Kit (CDK)
  - NPLinker
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- this way, we built a set of known BGC-spectrum pairs. To avoid etabolites based
  on properties absent from an MS2 spectrum,
- we use library MS2 spectra from the public, community-driven GNPS knowledge base
  [33] as a training set for the IOKR model
- 'Molecular fingerprints are extracted from SMILES strings using the Chemistry Development
  Kit [29]. The fingerprint vector is composed of three concatenated sets of fingerprints:
  CDK Substructure,'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 spectrum peak filtering by training set membership

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter MS2 spectrum peaks to retain only those present in a training dataset prior to kernel-based scoring, reducing noise and computational cost while accepting a small bias toward the training set's ion diversity. This preprocessing step is essential when applying the Probability Product Kernel (PPK) to metabolomics spectra linked to genomic data in natural products discovery workflows.

## When to use

When you have raw MS2 spectra (m/z and intensity pairs) and need to compute a Probability Product Kernel score or other fragmentation-based similarity metric against a training dataset of known spectra (e.g., GNPS library spectra with structural annotations). Use this skill when the input spectrum contains many noise peaks and you want to reduce computational burden while leveraging the ion diversity already captured in your training set. This is particularly relevant in genomic-metabolomic linking workflows where you must score hundreds of BGC–spectrum pairs and cannot afford to compute fragmentation trees for every input spectrum.

## When NOT to use

- Input spectrum is already validated or curated from the same training dataset — re-filtering may remove genuine signal or introduce redundancy.
- Your workflow does not require Probability Product Kernel computation or other kernel-based scoring; alternative denoising methods (e.g., intensity threshold, local noise estimation) may be more appropriate.
- The training dataset is very small or not representative of the chemical space in your input spectra — filtering may remove true signals and bias results severely.

## Inputs

- Raw MS2 spectrum (m/z and intensity pairs, e.g., in mzML, mzXML, or tabular format)
- Training dataset peak list (extracted from library spectra, typically from GNPS with structural annotations)
- Mass tolerance parameter (e.g., in Da or ppm)

## Outputs

- Filtered MS2 spectrum (m/z, intensity, and kernel weight in tabular format)
- Validation summary (e.g., number of peaks retained, proportion of signal retained)

## How to apply

Load both the input MS2 spectrum (m/z and intensity pairs) and the training dataset peak list (extracted from annotated library spectra, e.g., GNPS). Match peaks in the input spectrum to peaks in the training data using exact m/z values or a specified mass tolerance (e.g., ±0.1 Da). Retain only the matched peaks and discard all other peaks from the input spectrum. Apply the Probability Product Kernel denoising step to the filtered peak list to reweight peaks based on their likelihood in the training set. Output the denoised spectrum as a tabular file with columns for m/z, intensity, and kernel weight. This approach trades a small bias toward the training set's ion space for robust noise reduction and computational efficiency; the bias is acceptable because the training set is large enough (e.g., GNPS contains tens of thousands of spectra) to maintain sufficient ion diversity for downstream scoring.

## Related tools

- **GNPS** (Source of training dataset peak lists extracted from library MS2 spectra with structural annotations) — https://gnps.ucsd.edu/
- **Chemistry Development Kit (CDK)** (Mass calculation and m/z matching utility) — https://cdk.github.io/
- **NPLinker** (Framework that integrates this filtering step into the BGC–spectrum linking pipeline prior to Probability Product Kernel scoring) — https://github.com/NPLinker/nplinker

## Evaluation signals

- All retained peaks have exact or tolerance-matched m/z values in the training dataset; no peaks remain that are absent from the training set.
- The number of peaks retained is typically 20–50% of the input spectrum's peak count (typical denoising effect); if retention is >90% or <5%, verify mass tolerance and training dataset completeness.
- Kernel weights assigned to retained peaks are in the range [0, 1] and reflect the likelihood of each m/z in the training set; weights should be higher for abundant ions (e.g., precursor-related peaks).
- Output tabular file has exactly three columns (m/z, intensity, kernel weight) with no missing values and all numeric entries are non-negative.
- Downstream Probability Product Kernel score computation completes without errors; if filtering is too aggressive (retains <10 peaks), downstream scoring may fail or produce artificially low scores.

## Limitations

- Filtering theoretically biases the model toward the training set's ion space; novel ions or low-abundance diagnostic peaks not in the training set will be removed, potentially obscuring new natural products or rare structural features.
- The effectiveness of filtering depends critically on the completeness and diversity of the training dataset. If the training set is biased toward a subset of natural product classes or ionization conditions, the filtered spectrum will be biased accordingly.
- Mass tolerance parameter choice (e.g., ±0.1 Da vs. ±5 ppm) significantly affects which peaks are retained; there is no universal standard, and tolerance must be chosen based on the mass analyzer type and calibration quality.
- The approach does not account for systematic mass shifts or calibration errors in either the input spectrum or the training dataset, which can lead to false non-matches and loss of genuine signal.
- Kernel function and parameter selection for the Probability Product Kernel step are highly dependent on the choice of molecular fingerprint substructures, and this interdependency is not fully characterized in the literature.

## Evidence

- [other] Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation.: "Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation."
- [other] The training set is large enough to contain robust ion diversity and the bias effect is small.: "the training set is large enough to contain robust ion diversity and the bias effect is small."
- [other] Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list. Identify peaks in the input spectrum whose m/z values match peaks present in the training data (exact or within a specified mass tolerance).: "Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). 2. Identify peaks in the input"
- [other] Retain only the matched peaks and remove all other peaks from the spectrum. Apply the Probability Product Kernel (PPK) denoising step to the filtered peak list to adjust weights based on likelihood in the training set.: "Retain only the matched peaks and remove all other peaks from the spectrum. 4. Apply the Probability Product Kernel (PPK) denoising step to the filtered peak list to adjust weights based on"
- [other] Output the denoised spectrum as a tabular file (m/z, intensity, kernel weight) and a validation summary.: "Output the denoised spectrum as a tabular file (m/z, intensity, kernel weight) and a validation summary."
- [abstract] to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability"
- [readme] Python version ≥3.11: "Python version ≥3.11"
