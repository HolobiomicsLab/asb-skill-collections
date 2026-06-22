---
name: mass-spectrometry-fragmentation-pattern-modeling
description: Use when when building a re-usable spectral reference library for lipidomics workflows where you need to match experimental MS/MS spectra against a comprehensive theoretical fragmentation model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - LipidIN Expeditious Querying (EQ) Module
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
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
---

# mass-spectrometry-fragmentation-pattern-modeling

## Summary

Construct and organize comprehensive lipid fragmentation libraries by enumerating all valid acyl chain compositions, regioisomeric double-bond positions, and theoretical fragment m/z values into a hierarchical index. This skill enables rapid spectral matching and annotation of unknown lipids by pre-computing all chemically feasible fragmentation patterns for a lipid class taxonomy.

## When to use

When building a re-usable spectral reference library for lipidomics workflows where you need to match experimental MS/MS spectra against a comprehensive theoretical fragmentation model. Apply this skill if you have a defined lipid class taxonomy, acyl chain composition rules (carbon count ranges, unsaturation constraints), and fragmentation rules (neutral losses, characteristic ion patterns), and you want to index millions of potential lipid structures for sub-second query performance.

## When NOT to use

- When experimental spectra require deconvolution or spectral denoising before matching—this skill assumes clean input spectra; pre-process raw mzML data with XCMS and CAMERA first.
- When lipid class taxonomy or fragmentation rules are not yet defined or validated—this skill depends on accurate composition and fragmentation knowledge; incomplete rules will produce incomplete or incorrect libraries.
- When you need real-time fragmentation prediction for novel or modified lipids not covered by predefined chain composition rules—this skill enumerates fixed compositions; out-of-scope lipids (e.g., very long chains, unusual oxidations) require model-based prediction instead.

## Inputs

- lipid class taxonomy definition (allowed classes, nomenclature rules)
- acyl chain composition rules (carbon count range per class, min/max unsaturation)
- lipid fragmentation rules (neutral loss masses, characteristic ion generation formulas)
- reference MS/MS spectra from lipid standards (for validation)

## Outputs

- hierarchical fragmentation library file (indexed by lipid class, chain composition, positional isomer)
- theoretical m/z lookup table (chain composition → fragment m/z values)
- library metadata (total entry count, coverage statistics, validation report)

## How to apply

First, define the lipid class taxonomy and acyl chain composition rules specifying carbon count ranges and degree of unsaturation constraints for each class. Second, enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition using combinatorial enumeration. Third, compute theoretical fragment ion m/z values for each chain composition using lipid fragmentation rules (e.g., neutral loss masses, characteristic ion m/z formulas). Fourth, organize the resulting entries into a hierarchical index structure (lipid class → chain composition → positional isomer) to enable efficient O(1) or O(log N) lookup during spectral querying. Finally, validate library completeness by spot-checking fragment patterns against known lipid MS/MS standards and verifying total entry count matches the expected target (e.g., 168.6 million for a comprehensive phospholipid library).

## Related tools

- **XCMS** (Pre-processes raw mass spectrometry data (mzML format) for peak alignment, matching, and feature extraction before spectral library querying)
- **CAMERA** (Performs compound spectra extraction and annotation of LC/MS data sets to generate clean input spectra for fragmentation pattern matching)
- **LipidIN Expeditious Querying (EQ) Module** (Performs secondary matching of experimental spectra against the hierarchical fragmentation library and normalizes matching scores) — https://github.com/LinShuhaiLAB/LipidIN

## Evaluation signals

- Total library entry count matches the enumerated target (e.g., 168.6 million entries for comprehensive phospholipid coverage).
- Hierarchical index structure validates: lipid class counts, chain composition counts per class, and positional isomer counts per composition all match combinatorial expectations.
- Spot-check: 20–50 randomly selected theoretical fragment patterns match experimental MS/MS spectra from known lipid standards with mass error within specified ppm tolerance (e.g., ≤5 ppm MS1, ≤10 ppm MS2).
- Query performance benchmark: spectral matching against the library completes in sub-second time (e.g., 70 billion times faster than brute-force search).
- Validation report: false discovery rate on a curated lipid standard set is ≤5.7% (estimated FDR for 8923 lipids across species).

## Limitations

- Library completeness is bounded by the predefined lipid class taxonomy and chain composition rules; lipids with chains outside the enumerated carbon/unsaturation ranges will not be covered.
- Theoretical fragment m/z values depend on accurate fragmentation rules; incorrect or incomplete fragmentation models will produce false negatives (missed annotations) and false positives (spurious matches).
- Hierarchical indexing assumes non-overlapping lipid classes and chain compositions; ambiguous or mixed ionization modes (e.g., [M+H]+ vs [M+Na]+) require separate library instances.
- Library does not model in-source fragmentation, detector saturation, or matrix suppression effects; experimental spectra with unusual intensity distributions or missing expected fragments may not match well despite correct lipid identification.

## Evidence

- [other] Define the lipid class taxonomy and acyl chain composition rules (carbon count range, degree of unsaturation constraints): "Define the lipid class taxonomy and acyl chain composition rules (carbon count range, degree of unsaturation constraints)."
- [other] Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants: "Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition."
- [other] Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation): "Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation)."
- [other] Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup: "Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup."
- [readme] LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations: "LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations."
- [other] Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards: "Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million."
