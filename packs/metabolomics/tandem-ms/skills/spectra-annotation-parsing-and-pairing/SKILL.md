---
name: spectra-annotation-parsing-and-pairing
description: Use when when loading MS/MS spectra from MGF files for FIDDLE model training or evaluation, or when preparing spectrum–annotation pairs for rescore model data augmentation (TCN train/test sets).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msfiddle
  - FIDDLE (research codebase)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectra-annotation-parsing-and-pairing

## Summary

Parse MS/MS spectrum metadata (precursor m/z, adduct type, collision energy, formula annotations) from MGF files and pair spectra with their reference annotations to prepare data for model training, evaluation, and rescore augmentation. This step bridges raw spectral data and ground-truth labels required for supervised learning and benchmark evaluation.

## When to use

When loading MS/MS spectra from MGF files for FIDDLE model training or evaluation, or when preparing spectrum–annotation pairs for rescore model data augmentation (TCN train/test sets). Specifically needed when the annotation source contains FORMULA, SMILES, or other reference ground-truth fields that must be extracted and aligned with corresponding spectrum peaks and precursor properties.

## When NOT to use

- Input spectra are already in preprocessed tensor or NumPy array format with metadata embedded as separate objects — skip parsing and use the array directly.
- Spectra lack required MGF fields (PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) — preprocessing or field imputation must occur first.
- Ground-truth annotations are stored in a separate database or CSV file not co-located with spectrum data — use a database join or cross-reference lookup instead.

## Inputs

- MGF file with TITLE, PEPMASS, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY, and optional FORMULA/SMILES fields
- Peak list (m/z–intensity pairs) within MGF IONS sections
- Reference annotations (molecular formula, SMILES) embedded in MGF header

## Outputs

- Parsed spectrum objects (ID, m/z array, intensity array, precursor_mz, adduct, collision_energy, ground_truth_formula)
- Spectrum–annotation pairs ready for model training or evaluation
- Augmented/balanced train and test sets with positive and negative examples (for rescore workflows)

## How to apply

Load MGF records and extract required metadata fields: TITLE (spectrum identifier), PRECURSOR_MZ, PRECURSOR_TYPE (adduct), COLLISION_ENERGY, and ground-truth FORMULA or SMILES annotations. Parse peak lists (m/z–intensity pairs) from the IONS section. For each spectrum, validate that required fields are present (title, precursor_mz, precursor_type, collision_energy are mandatory); missing fields should trigger logging or skipping. Store parsed spectra as annotated objects (spectrum ID, peak array, precursor properties, reference formula). During rescore augmentation workflows, use these parsed pairs to cap positive examples per molecular formula, generate cross-spectrum negatives within defined precursor m/z windows, and downsample to achieve 1:1 positive:negative ratio before model training.

## Related tools

- **msfiddle** (Wraps MGF parsing and spectrum–annotation pairing for formula prediction; CLI and Python API accept MGF input and perform parsing internally) — https://github.com/josiehong/msfiddle
- **FIDDLE (research codebase)** (Full model training and evaluation codebase; includes data loading and parsing scripts (prepare_augment_rescore.py) for TCN and rescore augmentation) — https://github.com/JosieHong/FIDDLE

## Examples

```
msfiddle --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- All required MGF fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) are successfully extracted for 100% of input spectra with no missing values.
- Peak lists are correctly parsed from IONS sections: m/z and intensity arrays have matching length and numeric values within expected ranges (m/z > 0, intensity ≥ 0).
- Ground-truth formula annotations are present in ≥95% of spectra and match valid chemical formula syntax (e.g., C[0-9]+H[0-9]+ patterns).
- Precursor m/z values align with neutral mass calculated from adduct type and formula annotation (e.g., [M+H]+ precursor = formula_mass + 1.007 within ±5 ppm).
- Positive–negative example ratio in augmented rescore dataset matches target 1:1 ratio after downsampling; no spectra are duplicated or lost.

## Limitations

- MGF parsing depends on strict field naming and formatting; malformed or non-standard MGF variants may cause parse failures.
- Ground-truth formula annotations may be absent or incorrect in public spectral libraries (e.g., GNPS); validation against theoretical mass is recommended.
- Cross-spectrum negative generation using precursor m/z windowing is sensitive to window size; overly broad windows may introduce spurious negatives, while narrow windows may yield insufficient negatives for class balance.
- Collision energy and adduct type are required but may be missing or mis-labeled in legacy datasets, limiting applicability to modern standardized libraries (Orbitrap, Q-TOF).

## Evidence

- [readme] The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`: "The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`"
- [other] Load TCN train and test set spectra and annotations. Cap positive examples per molecular formula to enforce class balance constraints. Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio.: "Load TCN train and test set spectra and annotations. Cap positive examples per molecular formula to enforce class balance constraints. Generate cross-spectrum negatives by pairing spectra within a"
- [readme] Peak lists (m/z–intensity pairs) from the IONS section must be extracted along with spectrum title and precursor properties.: "41.0148 0.329893 
41.9986 89.226766 
55.8055 0.200544"
- [readme] Ground-truth FORMULA and SMILES fields are embedded in the MGF header for reference annotation and validation.: "SMILES=[H]c1c([H])n([H])c(=O)n([H])c1=O
FORMULA=C4H4N2O2"
