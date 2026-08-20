---
name: training-data-inventory-construction-from-spectral-libraries
description: Use when you are preparing to apply Probability Product Kernel–based scoring to MS2 spectra for genomic–metabolomic linking, and you need to establish a reference set of ion peaks that represent robust spectral diversity without overfitting to any single study.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - GNPS
  - Chemistry Development Kit (CDK)
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# training-data-inventory-construction-from-spectral-libraries

## Summary

Construct a curated peak inventory from public spectral libraries (e.g., GNPS) with structural annotations to serve as the reference set for MS2 spectrum filtering and Probability Product Kernel (PPK) denoising. This inventory enables downstream kernel-based scoring of BGC–metabolite links while leveraging community-validated spectral data.

## When to use

You are preparing to apply Probability Product Kernel–based scoring to MS2 spectra for genomic–metabolomic linking, and you need to establish a reference set of ion peaks that represent robust spectral diversity without overfitting to any single study. Use this skill when GNPS or similar public spectral libraries with chemical structure annotations are accessible and you intend to denoise input spectra by retaining only peaks present in the training inventory.

## When NOT to use

- Input spectra are already from the same library used to construct the inventory (risk of circular validation and overstated confidence).
- The analysis goal requires preservation of rare or novel peaks not yet documented in public libraries; filtering by inventory will remove potentially diagnostic unknown ions.
- No public spectral library with structural annotations is available for your metabolite class or organism type.

## Inputs

- Library MS2 spectra from GNPS or similar public database with structural annotations (m/z, intensity pairs; format: tabular or JSON)
- Input MS2 spectrum to be filtered (m/z and intensity pairs)
- Mass tolerance parameter (e.g., exact match or ±5 ppm)

## Outputs

- Peak inventory: tabular list of m/z values extracted from library spectra
- Filtered MS2 spectrum: m/z and intensity pairs retained after matching against inventory
- Validation summary: count of matched vs. removed peaks, filtering statistics

## How to apply

Download library MS2 spectra from a public spectral database (e.g., GNPS) that includes structural annotations. Extract the complete set of m/z values from all library spectra to form the peak inventory. For each input spectrum, match its m/z peaks against the inventory using a specified mass tolerance (exact or within a defined ppm window). Retain only matched peaks and discard all others. The rationale is that training libraries are large enough to contain robust ion diversity—typical of real metabolites—while filtering eliminates noise and anomalous peaks. Although this approach theoretically biases the model toward the training set, the bias is small in practice because the training set encompasses thousands of library spectra across diverse chemical classes. The filtered spectrum is then passed to the Probability Product Kernel step for weight adjustment based on peak likelihood in the training set.

## Related tools

- **GNPS** (Source of library MS2 spectra with structural annotations for peak inventory construction) — https://gnps.ucsd.edu/
- **Chemistry Development Kit (CDK)** (Optional: parse chemical structure annotations and extract substructure information from library spectra)

## Evaluation signals

- Inventory size is in the thousands of unique m/z values (consistent with scale of GNPS library; e.g., >10,000 peaks).
- After filtering, input spectrum contains only m/z values present in the inventory (cross-check against the reference list); no peaks are retained outside the inventory.
- Filtering statistics show reasonable retention rate (e.g., 30–70% of input peaks retained, depending on spectral complexity); extreme values (near 0% or 100%) suggest misconfiguration of mass tolerance.
- Filtered spectrum output file matches schema (m/z, intensity, and optional kernel weight columns); no missing or malformed entries.
- Validation summary documents number of matched peaks, number of discarded peaks, and mass tolerance used.

## Limitations

- Training-set bias: filtering inherently biases the model toward metabolites in the library; novel or rare compounds with unique fragmentation patterns may be penalized.
- Mass tolerance sensitivity: choice of tolerance (exact vs. ppm window) significantly affects retention rate and is not fully optimized in the literature; too strict a tolerance removes valid peaks; too loose a tolerance defeats the filtering purpose.
- Library coverage gaps: metabolites from understudied organisms or chemical classes may have sparse or absent representation in GNPS, reducing the effectiveness of filtering for those samples.
- Non-microbial contamination: the GNPS training set includes metabolites from sources other than microbial organisms, which may introduce irrelevant peaks into the inventory for microbial-only studies.

## Evidence

- [other] Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations).: "Load the input MS2 spectrum (m/z and intensity pairs) and the IOKR training dataset peak list (extracted from GNPS library spectra with structural annotations)"
- [other] Retain only the matched peaks and remove all other peaks from the spectrum.: "Identify peaks in the input spectrum whose m/z values match peaks present in the training data (exact or within a specified mass tolerance). 3. Retain only the matched peaks and remove all other"
- [other] While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the bias effect is small.: "While this filtering theoretically biases the model toward the training set, in practice the approach is widely used because the training set is large enough to contain robust ion diversity and the"
- [abstract] We use library MS2 spectra from the public, community-driven GNPS knowledge base as a training set for the IOKR model.: "The IOKR model is trained on a set of spectrum-molecular fingerprint pairs. We use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model"
- [results] The training set used to build the IOKR model includes metabolites from sources other than microbial.: "the training set used to build the IOKR model includes metabolites from sources other than microbial"
