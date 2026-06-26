---
name: spectral-denoising-via-training-data-filtering
description: Use when you have untargeted MS2 spectra from environmental or clinical
  samples that will be used for natural product identification (e.g., linking to BGCs
  via IOKR or other kernel-based methods), and you have access to a high-quality training
  library of annotated spectra with known structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - GNPS
  - MIBiG
  - Chemistry Development Kit (CDK)
  - antiSMASH
  - Probability Product Kernel (PPK)
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
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
  and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base
  [33] as a training set for the IOKR model
- To assign one or more molecular structures to BGCs, according to how many high-scoring
  matches are found in MIBiG
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development
  Kit
- Molecular fingerprints are extracted from SMILES strings using the Chemistry Development
  Kit [29]
- after downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
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

# Spectral denoising via training data filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter MS2 spectra to retain only peaks present in a reference training library, then apply the Probability Product Kernel (PPK) as a denoising step before downstream scoring. This reduces computational burden and noise in spectrum-to-BGC matching by excluding unexplained fragmentation peaks.

## When to use

You have untargeted MS2 spectra from environmental or clinical samples that will be used for natural product identification (e.g., linking to BGCs via IOKR or other kernel-based methods), and you have access to a high-quality training library of annotated spectra with known structures. Use this skill when computational cost or peak noise threatens the stability of kernel-based scoring methods.

## When NOT to use

- Input spectra are from a targeted analysis with known fragmentation patterns; filtering may remove biologically important diagnostic peaks.
- The training library is too small (<500 spectra) or has poor coverage of your sample's chemical space; filtering will remove too many peaks and bias results.
- You need to preserve all peaks for manual de novo structure elucidation or fragmentation tree interpretation; filtering obscures information needed for chemical reasoning.

## Inputs

- MS2 spectra (m/z and intensity pairs, e.g., from GNPS or mzML format)
- Reference training library (annotated spectra with chemical structures and SMILES strings)
- PPM tolerance threshold (typical range: 5–10 ppm for exact mass instruments)

## Outputs

- Filtered MS2 spectra (m/z and intensity pairs with only training-library-matched peaks)
- Probability Product Kernel (PPK) matrix for each spectrum
- Peak presence/absence binary indicator per spectrum relative to training library

## How to apply

First, load a reference training set of MS2 spectra with validated structural annotations (e.g., GNPS library: 4138 spectra with SMILES-derived molecular fingerprints). Extract the set of all m/z peaks present across the training set. For each input spectrum, retain only peaks whose m/z values (within typical PPM tolerance) match peaks in the training set; discard all other peaks as unexPlained noise. Then compute the Probability Product Kernel (PPK) on the filtered spectrum to produce a kernel matrix suitable for downstream methods like IOKR. This filtering acts as a denoising step before time-consuming computation of fragmentation trees or kernel regressions. The rationale is that peaks absent from the training library are unlikely to aid scoring and introduce unnecessary computational overhead.

## Related tools

- **GNPS** (Provides the reference training library of annotated MS2 spectra with chemical structures for peak matching and denoising)
- **Probability Product Kernel (PPK)** (Computes kernel matrix on filtered spectra for downstream IOKR or kernel regression methods)
- **Chemistry Development Kit (CDK)** (Extracts molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from training library SMILES strings)
- **NPLinker** (Framework integrating spectral denoising and IOKR scoring for BGC-spectrum linking) — https://github.com/NPLinker/nplinker

## Evaluation signals

- Peak retention rate: typically 30–70% of original peaks remain after filtering, with retained peaks distributed across m/z range relevant to the training library.
- PPK matrix rank and condition number remain stable and computationally tractable after filtering (no numerical instability or rank deficiency introduced).
- Downstream IOKR top-n accuracy (e.g., top-5, top-10) on the filtered spectrum set matches or exceeds that of unfiltered spectra, with no loss of discriminative power.
- Distribution of mean scores for validated BGC-spectrum pairs shifts toward higher values (e.g., IOKR mean increases from 0.0105 to significantly higher for filtered data), with p-value < 0.05 in rank-sum test against unfiltered baseline.
- Computational runtime for subsequent kernel-based scoring (IOKR, PPK) decreases by ≥20% due to reduced peak dimensionality.

## Limitations

- Reliance on training library quality and coverage: if the training library has incomplete fragmentation patterns or is biased toward certain compound classes, filtering may systematically remove important peaks for underrepresented metabolite types.
- PPM tolerance parameter (5–10 ppm assumed) must be matched to the mass accuracy of both training library and input spectra; mismatch will result in over- or under-filtering.
- No guarantee that training-library peaks are causal for BGC matching; peaks present in training data may be generic and not discriminative for your specific linking task.
- Filtered spectra may lose information needed for manual spectroscopic interpretation or de novo structure elucidation, making downstream validation more challenging.

## Evidence

- [abstract] we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK): "we filter the input spectra to include only the peaks found in the training data, before using the Probability Product Kernel (PPK)"
- [abstract] As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra: "As a denoising step, to avoid time-consuming computation of fragmentation trees for the spectra"
- [other] For the 6246 MS2 spectra in the MIBiG/GNPS evaluation set, apply the trained IOKR model to predict molecular fingerprints... Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step.: "Filter input MS2 spectra using the Probability Product Kernel (PPK) to retain only peaks present in the training data as a denoising step."
- [other] Load the GNPS library training set (4138 spectra with structural annotations) and extract molecular fingerprints (CDK Substructure, PubChem Substructure, Klekota-Roth) from SMILES strings for each annotated metabolite.: "Load the GNPS library training set (4138 spectra with structural annotations) and extract molecular fingerprints"
