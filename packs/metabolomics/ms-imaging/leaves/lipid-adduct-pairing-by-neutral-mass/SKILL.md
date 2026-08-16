---
name: lipid-adduct-pairing-by-neutral-mass
description: Use when when processing mass spectrometry imaging data with multiple adduct forms of the same lipid species, and you need to correct one adduct form (e.g. [M+H]+) for isotopic interference from a co-occurring adduct (e.g. [M+Na]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - LipidQMap
  - Cardinal
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Lipid Adduct Pairing by Neutral Mass

## Summary

Identify and match paired adduct ions (e.g. [M+H]+ and [M+Na]+) from the same neutral lipid species by comparing neutral lipid identifiers and m/z differences. This pairing is essential for applying Type II isotopic correction to remove adduct-specific overlap in mass spectrometry imaging quantitation.

## When to use

When processing mass spectrometry imaging data with multiple adduct forms of the same lipid species, and you need to correct one adduct form (e.g. [M+H]+) for isotopic interference from a co-occurring adduct (e.g. [M+Na]+). This is particularly necessary before quantitation if ion images show systematic intensity bias from unresolved isotopic overlap between adduct pairs.

## When NOT to use

- When data contains only a single adduct form per lipid species; pairing requires at least two distinct adducts for the same neutral mass.
- When raw m/z accuracy is insufficient to reliably distinguish between adjacent features; requires mass tolerance (ppm window) to be set appropriately during import.
- When the input database does not include neutral lipid identifiers or adduct form annotations; pairing logic depends on this metadata being present and consistent.

## Inputs

- Feature-by-pixel intensity matrix (float32, shape n_features × n_pixels)
- Feature metadata table (featureData group in HDF5) with columns: neutral lipid identifier, adduct form, measured m/z
- Lipid identification database with lipid class and neutral formula for each species

## Outputs

- Paired feature index table (mapping [M+H]+ feature ID to corresponding [M+Na]+ feature ID)
- Pair descriptor objects (neutral lipid ID, adduct pair type, m/z offset, expected mass difference)

## How to apply

Load the feature metadata from the HDF5 spectraData/featureData group, which includes neutral lipid identifiers (e.g. lipid class and chain composition) and measured m/z values for each feature. Match features with the same neutral lipid identifier but different adduct forms by checking that their m/z difference approximates the mass difference between the two adducts (~22 Da for [M+Na]+ vs [M+H]+, accounting for the mass difference of Na vs H). For each matched pair, record the pair identifiers and use them in downstream Type II isotopic correction to scale and subtract the [M+Na]+ intensity from the [M+H]+ intensity across all pixels. Validate pairing by verifying that paired features have consistent m/z offsets and that both adducts are present in the feature list.

## Related tools

- **LipidQMap** (Performs feature loading, metadata access, and coordinates Type II isotopic correction after pairing) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines the HDF5 container format (Cardinal::HDF5) that stores feature metadata and intensity matrices used for pairing) — https://cardinalmsi.org

## Evaluation signals

- Every [M+H]+ feature with a corresponding [M+Na]+ feature in the database is successfully matched to a partner feature with m/z difference within expected tolerance (~22 Da ± ppm window).
- Paired features have identical or near-identical neutral lipid identifiers (same lipid class and chain composition).
- No unpaired [M+H]+ or [M+Na]+ features remain in the feature list after pairing logic completes (or unpaired features are explicitly flagged as singletons).
- After Type II isotopic correction using the pair information, the corrected [M+H]+ intensities are non-negative across all pixels (clamped at zero), indicating consistent directional subtraction of the [M+Na]+ contribution.

## Limitations

- Pairing accuracy depends on accurate feature annotation in the lipid database; missing or incorrect neutral lipid identifiers will cause pairing failures.
- Mass tolerance (ppm) must be set appropriately during initial imzML import to ensure correct feature extraction; overly loose tolerance may pair unrelated features with similar m/z values.
- Works only for lipid species where both adduct forms are present in the data; sparse datasets may lack both adducts for some species, leaving those species unpaired.
- The m/z difference model assumes simple substitution (e.g., Na for H); complex modifications or multiply-charged ions require additional logic not described in the core pairing workflow.

## Evidence

- [other] Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution).: "Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution)."
- [readme] Feature metadata including neutral lipid ID, adduct form, and m/z is stored in Cardinal::HDF5 containers.: "LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions."
- [readme] Database structure includes adduct form field required for pairing logic.: "**Adducts**: the adduct forms of the species, separated by a comma if multiple."
- [other] Type II isotopic correction removes isotopic overlap contributed by [M+Na]+ adducts from [M+H]+ images.: "LipidQMap performs Type II isotopic correction by correcting [M+H]+ adducts for isotopic overlap contributed by [M+Na]+ adducts in ion images."
