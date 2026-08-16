---
name: fragment-ion-theoretical-mass-calculation
description: Use when when building a comprehensive lipid fragment ion library covering
  all chain composition and positional isomer variants (e.g., 168.6 million entries).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - XCMS
  - CAMERA
  techniques:
  - LC-MS
  - NMR
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-theoretical-mass-calculation

## Summary

Compute theoretical m/z values for lipid fragment ions across all regioisomeric chain compositions and double-bond positional variants using systematic lipid fragmentation rules. This enables construction of comprehensive spectral libraries for high-throughput lipid annotation via spectral matching.

## When to use

When building a comprehensive lipid fragment ion library covering all chain composition and positional isomer variants (e.g., 168.6 million entries). Essential when you need to enumerate theoretical fragment patterns for acyl chains within specified carbon count ranges and unsaturation constraints, prior to hierarchical indexing for spectral querying.

## When NOT to use

- Input is a single experimental mass spectrum requiring real-time annotation—use expeditious querying (EQ) module instead to match observed peaks against the pre-built library.
- Lipid identifications are already confirmed by orthogonal methods (e.g., NMR, chromatographic standards); library generation is not needed for validation.
- Fragmentation patterns are highly matrix-dependent or instrument-specific; theoretical calculations may not generalize without empirical recalibration.

## Inputs

- lipid class taxonomy and acyl chain composition rules (carbon count range, degree of unsaturation constraints)
- lipid fragmentation rule specifications (neutral loss patterns, characteristic ion types, ionization mode: positive/negative [M+CH3COO]−/[M+COOH]−)
- known lipid standards (for validation spot-checks)

## Outputs

- 168.6 million entry lipid fragmentation hierarchical library indexed by (lipid class, chain composition, positional isomer)
- theoretical m/z values for each fragment ion variant
- hierarchical lookup index structure

## How to apply

For each valid acyl chain composition (defined by carbon count and degree of unsaturation), enumerate all regioisomeric double-bond positions. Apply lipid fragmentation rules to each variant—specifically neutral loss mechanisms (e.g., loss of fatty acid) and characteristic ion generation (e.g., [M-H]−, [M+CH3COO]−, [M+COOH]−)—to compute theoretical fragment m/z values. Organize these calculations in a hierarchical index structure (lipid class → chain composition → positional isomer variant) for efficient O(1) or near-constant-time lookup during spectral matching. Validate the completeness of the generated library by cross-referencing spot-checked fragment patterns against known lipid standards and confirming the total entry count matches the target enumeration.

## Related tools

- **XCMS** (mass spectrometry data processing and peak detection for validation against experimental standards)
- **CAMERA** (compound spectra extraction and annotation for validation of theoretical fragment patterns)

## Evaluation signals

- Total entry count in the generated library matches the target (168.6 million entries), confirming complete enumeration of all chain composition and positional isomer variants.
- Spot-checked fragment m/z values match known lipid standards within specified mass tolerance (e.g., 5–10 ppm for MS1, 10 ppm for MS2).
- Hierarchical index structure supports O(1) or near-constant lookup time; query latency remains <1 ms per spectrum peak for 70 billion spectral queries in <1 second.
- Cross-validation: regioisomeric variants for a given chain composition produce unique, distinguishable m/z patterns that enable downstream false-positive filtering (e.g., 5.7% FDR in LCI module).
- Library covers expected lipid diversity across species and lipid classes (e.g., OxPC, OxPG, OxPI, OxPS, OxTG) without artificial gaps or duplicates.

## Limitations

- Theoretical m/z calculations assume ideal fragmentation rules; in-source fragmentation, loss of water/ammonia, and matrix-dependent adducts may not be fully captured.
- Enumeration becomes computationally expensive for very high carbon counts or extreme unsaturation ranges; practical limits were not explicitly stated in the article.
- Validation against known standards is spot-check only; comprehensive validation of all 168.6 million entries is computationally infeasible.
- Fragment ion predictions do not account for oxidative modifications (OxPE, OxPC) without explicit augmentation; separate spectral uploads to Zenodo were required for oxidized lipid variants.

## Evidence

- [intro] LipidIN features a 168.6 million lipid fragmentation hierarchical library that encompasses all potential chain compositions and carbon-carbon double bond locations.: "LipidIN features a 168.6 million lipid fragmentation hierarchical library that encompasses all potential chain compositions and carbon-carbon double bond locations"
- [other] Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition.: "Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition"
- [other] Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation).: "Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation)"
- [other] Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup.: "Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup"
- [other] Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million.: "Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million"
