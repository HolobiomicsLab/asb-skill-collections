---
name: multimodal-spectral-alignment-by-molecular-identifier
description: Use when you have parsed spectral data from four distinct modalities (NMR, HSQC, COSY, IR) stored as separate numpy arrays or DataFrames with normalized chemical shifts and intensity ranges, and you need to create paired multimodal training records where each molecule's spectra across all.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3407
  tools:
  - pandas
  - numpy
  - Python
  - Python (standard library)
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmst_cq
    doi: 10.1002/ange.202517611
    title: MMST
  dedup_kept_from: coll_mmst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/ange.202517611
  all_source_dois:
  - 10.1002/ange.202517611
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multimodal-spectral-alignment-by-molecular-identifier

## Summary

Align and co-register spectral data across multiple modalities (NMR, HSQC, COSY, IR) for individual molecules by matching molecular identifiers, creating joint training records that pair each molecule with its complete spectroscopic profile. This skill ensures multimodal tensors are properly synchronized for downstream transformer-based structure prediction.

## When to use

You have parsed spectral data from four distinct modalities (NMR, HSQC, COSY, IR) stored as separate numpy arrays or DataFrames with normalized chemical shifts and intensity ranges, and you need to create paired multimodal training records where each molecule's spectra across all modalities are jointly indexed and validated for completeness before model ingestion.

## When NOT to use

- Input spectral data has not yet been parsed into uniform array format or normalized across modalities—preprocess and normalize first before alignment.
- Molecular identifiers are inconsistent or non-existent across modalities (e.g., one modality uses SMILES, another uses InChI)—reconcile identifier schemas first.
- You only have data from one or two spectroscopic modalities—this skill requires all four (NMR, HSQC, COSY, IR) to be present to create complete joint records.

## Inputs

- parsed NMR spectral arrays (numpy or pandas, normalized chemical shifts and intensities)
- parsed HSQC spectral arrays (numpy or pandas, normalized chemical shifts and intensities)
- parsed COSY spectral arrays (numpy or pandas, normalized chemical shifts and intensities)
- parsed IR spectral arrays (numpy or pandas, normalized intensity ranges)
- molecular identifier mapping (list or dict linking each spectrum file or index to a unique molecule ID)

## Outputs

- joint training records (list of dicts or structured DataFrame/HDF5, each row: molecule_id → (NMR_tensor, HSQC_tensor, COSY_tensor, IR_tensor))
- aligned multimodal tensor batch (numpy array or PyTorch tensor, shape: [n_molecules, 4, spectrum_length])
- modality coverage report (dict or log: n_molecules_complete, n_molecules_incomplete, missing_modality_counts)

## How to apply

Index each spectral modality (NMR, HSQC, COSY, IR) by molecular identifier—typically a molecule name, SMILES string, or unique compound code. For each molecule present in the curated dataset, retrieve its spectrum from each of the four modalities. Verify that all four modalities are present for that molecule; exclude any molecule lacking a complete spectroscopic profile. Concatenate or stack the aligned spectral tensors along a modality dimension, ensuring shape consistency (e.g., all spectra for a given modality have the same chemical shift resolution and normalized intensity scale). Construct a joint training record—a dictionary or row mapping the molecular identifier to a tuple or structured array containing the aligned NMR, HSQC, COSY, and IR tensors. Validate the output by checking that no NaN or infinite values exist in the aligned tensors and that the modality coverage is complete (100% of molecules have all four spectra).

## Related tools

- **pandas** (Index and merge spectral DataFrames by molecular identifier; validate completeness and structure of aligned records)
- **numpy** (Construct and validate aligned multimodal tensor arrays; check for NaN/infinite values and enforce shape consistency across modalities)
- **Python (standard library)** (Implement alignment logic: iterate over molecular IDs, retrieve spectra from four modalities, construct joint records)

## Evaluation signals

- All molecules in the output joint records have entries for exactly four modalities (NMR, HSQC, COSY, IR); no missing or null modality tensors.
- Output tensor arrays have consistent shape within each modality (e.g., all NMR spectra have the same chemical shift resolution); shape mismatches logged and investigated.
- No NaN or infinite values remain in the aligned tensor arrays after alignment (verified via numpy.isnan(), numpy.isinf()).
- Molecular identifier mapping is one-to-one and complete: every molecule in the curated dataset appears exactly once in the joint training records.
- Modality coverage report shows 100% of molecules have all four spectra; any excluded molecules are explicitly documented with reason (missing modality, quality filter, duplicate removal).

## Limitations

- Alignment quality depends on the consistency and uniqueness of molecular identifiers across all four modality datasets; non-standardized or ambiguous identifiers (e.g., duplicate molecule names) will produce incorrect pairings.
- Requires all four spectroscopic modalities (NMR, HSQC, COSY, IR) to be present for each molecule; molecules with incomplete modality coverage are excluded, potentially reducing training set size if modality availability is uneven.
- Chemical shift scales and intensity normalizations must be harmonized before alignment; mismatches in preprocessing (e.g., different ppm ranges or intensity normalization schemes across modalities) can corrupt multimodal tensor alignment.
- Alignment does not account for temporal or experimental condition metadata (e.g., temperature, solvent); if such metadata varies across modalities for the same molecule, the joint record conflates conditions and may mislead downstream analysis.
- Computational memory scales with the number of molecules and spectrum resolution; very large datasets or high-resolution spectra may require batched or streaming alignment approaches not detailed in the core workflow.

## Evidence

- [other] Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities.: "Align multi-modal spectra by molecular identifier and create joint training records pairing each molecule with its complete spectroscopic profile across all four modalities."
- [other] The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data used by the MultiModalSpectralTransformer for molecular structure prediction.: "The DataGenerationPipeline integrates four spectroscopic modalities—NMR, HSQC, COSY, and IR—as input sources for generating multimodal training data"
- [other] Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities.: "Parse NMR, HSQC, COSY, and IR spectral files into standardized numpy arrays or pandas DataFrames, normalizing chemical shift scales and intensity ranges across modalities."
- [other] Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays.: "Validate pipeline output shape, data type, and modality coverage; verify that no NaN or infinite values remain in tensor arrays."
- [other] Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors.: "Implement a DataGenerationPipeline class with methods to load, preprocess, batch, and augment (if applicable) the curated multimodal tensors."
