---
name: peak-matching-and-mass-alignment
description: Use when when you have raw MS2 spectra (m/z and intensity pairs) and a curated reference peak list from a large training dataset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# peak-matching-and-mass-alignment

## Summary

Filter MS2 spectrum peaks by matching their m/z values against a reference training dataset peak list, retaining only peaks found in the training data to reduce noise and bias computations toward well-characterized ion patterns. This denoising step precedes kernel-based spectrum scoring and improves signal quality for downstream natural product identification.

## When to use

When you have raw MS2 spectra (m/z and intensity pairs) and a curated reference peak list from a large training dataset (e.g., GNPS library spectra with structural annotations), and you need to denoise spectra before applying kernel-based scoring methods such as the Probability Product Kernel (PPK) or IOKR to link spectra to biosynthetic gene clusters. Use this skill when computational efficiency and reduction of spurious peaks are priorities and the training set is known to be large and representative of your metabolite diversity.

## When NOT to use

- Input training dataset is small, domain-specific, or unrepresentative of your metabolite classes — filtering will introduce unacceptable bias toward the training set at the cost of signal diversity.
- Your downstream analysis requires full peak information including rare or novel fragments not present in the training data — peak matching will discard potentially informative low-frequency peaks.
- Mass tolerance is not well-defined or calibration quality is poor — m/z matching accuracy will degrade and produce unreliable filtered spectra.

## Inputs

- Raw MS2 spectrum as m/z and intensity pairs (tabular format or mzML/mzXML)
- Reference peak list extracted from training dataset (e.g., GNPS library spectra with structural annotations)
- Mass tolerance threshold (ppm or Da) for m/z matching

## Outputs

- Denoised MS2 spectrum as tabular file (m/z, intensity, kernel weight columns)
- Validation summary (peaks retained count, intensity fraction, match rate)

## How to apply

Load the input MS2 spectrum (m/z and intensity pairs) and the reference peak list extracted from the training dataset (e.g., GNPS library with structural annotations). Identify peaks in the input spectrum whose m/z values match peaks in the training data within a specified mass tolerance (e.g., exact match or predefined ppm window). Retain only the matched peaks and discard all others from the spectrum. Apply the Probability Product Kernel (PPK) denoising step to the filtered peak list to adjust weights based on likelihood in the training set. Output the denoised spectrum as a tabular file with columns for m/z, intensity, and kernel weight, along with a validation summary (e.g., number of peaks retained, fraction of original spectrum intensity preserved). The rationale is that while this filtering theoretically introduces training-set bias, the bias effect is small in practice because large, diverse training sets like GNPS contain robust ion coverage across natural product classes.

## Related tools

- **GNPS** (Source of curated library MS2 spectra and reference peak list for training set construction) — https://gnps.ucsd.edu
- **Chemistry Development Kit (CDK)** (Support for m/z alignment, mass tolerance matching, and peak manipulation utilities)
- **NPLinker** (Framework integrating peak-matched spectra with IOKR scoring for BGC-spectrum linking) — https://github.com/NPLinker/nplinker

## Evaluation signals

- Verify that all retained peaks in the denoised spectrum have exact m/z matches (or within specified tolerance) to the reference peak list; no unmatched peaks should remain.
- Check that the output tabular file contains three columns (m/z, intensity, kernel weight) with no missing values; kernel weights should be in range [0, 1] or normalized probability scale.
- Confirm that the fraction of original spectrum intensity preserved is reasonable (typically 30–70% depending on noise level and training set coverage); a value < 10% or > 95% suggests miscalibration or poor training set match.
- Validate that the number of peaks retained is less than the original spectrum but non-zero; zero retained peaks indicates mass tolerance is too strict or training set does not cover the observed m/z range.
- Compare denoised spectrum to reference spectra in GNPS library by matching against known compounds; confirmed matches should show higher cosine similarity or IOKR score than the unfiltered spectrum.

## Limitations

- Filtering biases the model toward the training set, although this effect is small if the training set is large and covers sufficient ion diversity. This may reduce sensitivity to novel or rare fragment ions not present in GNPS.
- Performance and applicability depend heavily on mass tolerance selection and quality of m/z calibration in the input spectra; miscalibration will produce few or no matches.
- The approach assumes the reference peak list is representative and accurate; errors or gaps in the training dataset (e.g., missing ion types, wrong annotations) will propagate to the filtered spectra and reduce downstream scoring quality.
- For spectra from less common or newly discovered natural products, the training set may lack relevant peaks, resulting in excessive filtering and loss of diagnostic fragments.

## Evidence

- [other] Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation.: "Input MS2 spectra are denoised by retaining only peaks that appear in the training dataset prior to Probability Product Kernel computation."
- [other] 1. Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). 2. Identify peaks in the input spectrum whose m/z values match peaks present in the training data (exact or within a specified mass tolerance). 3. Retain only the matched peaks and remove all other peaks from the spectrum.: "Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations). Identify peaks in the input spectrum"
- [other] While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the bias effect is small.: "While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the"
- [abstract] to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data, before filtering using the Probability: "to avoid time-consuming computation of fragmentation trees for the spectra, we filter the input spectra to include only the peaks found in the training data"
- [other] Output the denoised spectrum as a tabular file (m/z, intensity, kernel weight) and a validation summary.: "Output the denoised spectrum as a tabular file (m/z, intensity, kernel weight) and a validation summary."
