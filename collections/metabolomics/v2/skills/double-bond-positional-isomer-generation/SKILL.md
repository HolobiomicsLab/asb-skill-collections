---
name: double-bond-positional-isomer-generation
description: Use when when constructing a comprehensive lipid spectral reference library
  that must disambiguate lipids differing only in carbon-carbon double-bond position
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - XCMS
  - CAMERA
  - LipidIN
  techniques:
  - LC-MS
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

# double-bond-positional-isomer-generation

## Summary

Systematically enumerate all regioisomeric double-bond position variants for acyl chain compositions within defined carbon count and unsaturation constraints, generating theoretical m/z fragment ions for each positional isomer to populate a hierarchical lipid fragmentation library.

## When to use

When constructing a comprehensive lipid spectral reference library that must disambiguate lipids differing only in carbon-carbon double-bond position (e.g., OA 18:1 Δ9 vs. OA 18:1 Δ11), and you need to precompute all valid positional isomers for a given lipid class, carbon count range, and unsaturation level before matching unknown MS/MS spectra.

## When NOT to use

- Input spectra are already matched to a curated spectral database with known positional assignments — use spectral matching directly rather than regenerating isomer variants.
- Lipid standard reference materials are unavailable for validation — library completeness cannot be verified without spot-checking against known standards.
- Analysis requires only broad lipid class annotation without positional isomer discrimination (e.g., 'phosphatidylcholine' is sufficient) — the full positional enumeration adds computational overhead without benefit.

## Inputs

- Lipid class taxonomy definition (list of lipid classes and their nomenclature rules)
- Acyl chain composition rules (carbon count range, unsaturation degree constraints per class)
- Lipid fragmentation rules (neutral loss patterns, characteristic ions for each class)

## Outputs

- Hierarchical lipid fragmentation library indexed by (lipid class, chain composition, positional isomer, fragment m/z)
- Complete enumeration of all valid double-bond positional variants for each chain composition
- Theoretical m/z values for all fragment ions derived from positional isomers

## How to apply

First, define the lipid class taxonomy and acyl chain composition rules by specifying valid carbon count ranges and degree-of-unsaturation constraints for each lipid class. Second, enumerate all valid acyl chain structures by iterating over all permissible carbon counts and unsaturation levels; for each composition, systematically generate all regioisomeric double-bond position variants (e.g., for C18:1, generate Δ1, Δ2, ..., Δ17). Third, apply lipid fragmentation rules (neutral loss patterns, characteristic ion generation) to compute theoretical m/z values for each double-bond variant. Fourth, organize the resulting entries into a hierarchical index structure (lipid class → chain composition → positional isomer → fragment m/z) for efficient O(log n) lookup during spectral querying. Fifth, validate library completeness by spot-checking fragment patterns of known standards and verifying the entry count matches the target (e.g., 168.6 million entries).

## Related tools

- **XCMS** (Peak alignment, matching, and preprocessing of mzML mass spectrometry data prior to spectral querying against positional isomer library)
- **CAMERA** (Compound spectra extraction and annotation from LC/MS data sets to group isotopologues and adducts before matching against fragmentation library)
- **LipidIN** (Integration framework housing the 168.6 million entry hierarchical library and expeditious querying module for matching preprocessed spectra against enumerated positional isomers) — https://github.com/LinShuhaiLAB/LipidIN

## Evaluation signals

- Library entry count matches target (e.g., 168.6 million entries); subset counts match combinatorial expectation (e.g., number of C18:1 Δn variants = 17 for each lipid class).
- Spot-checked fragment ion m/z values for known lipid standards align with measured fragmentation patterns within ppm tolerance (e.g., ±5 ppm MS1, ±10 ppm MS2).
- Hierarchical index structure supports efficient querying (~70 billion spectral comparisons in <1 second per the README), implying correct indexing and no orphaned entries.
- False discovery rate on annotated lipids is consistent with expected background (e.g., 5.7% FDR across 8923 lipids in the LipidIN application).
- Positional isomers within a composition produce distinguishable fragment profiles; cosine similarity between different Δ positions shows statistically significant separation.

## Limitations

- Enumeration scales combinatorially with carbon count range and unsaturation limits; very large ranges may exceed practical memory/storage (e.g., C0–C50 with up to 15 double bonds).
- Double-bond regioisomerism alone cannot distinguish stereoisomerism (cis vs. trans); library does not enumerate or disambiguate E/Z geometry variants.
- Theoretical m/z fragments assume standard lipid fragmentation rules; non-standard or oxidized lipids may require manual rule extension (README mentions OxPC, OxPG, OxPI, OxPS added separately).
- Positional assignment accuracy depends on MS/MS spectral resolution and fragment ion intensity ratios; low-resolution or noisy spectra may not support definitive isomer discrimination.

## Evidence

- [other] Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition.: "Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition."
- [other] Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation).: "Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation)."
- [other] Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup.: "Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup."
- [readme] 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations: "168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"
- [other] Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million.: "Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million."
