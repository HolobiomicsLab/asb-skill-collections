---
name: hierarchical-database-indexing
description: Use when when you have a large combinatorial chemical space (e.g., all
  regioisomeric positions of lipid double bonds across carbon counts and saturation
  levels) and need to query it repeatedly against experimental mass spectrometry spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - XCMS
  - CAMERA
  - LipidIN Expeditious Querying (EQ) Module
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# hierarchical-database-indexing

## Summary

Construct and organize a massive enumerated library (e.g., 168.6 million lipid entries) into a hierarchical index structure that maps chemical compositions and structural variants to their theoretical fragmentation patterns, enabling sub-second lookups during spectral annotation.

## When to use

When you have a large combinatorial chemical space (e.g., all regioisomeric positions of lipid double bonds across carbon counts and saturation levels) and need to query it repeatedly against experimental mass spectrometry spectra. Apply this skill if spectral matching currently requires linear or slow secondary searches and if false positives from incomplete or flat libraries are degrading annotation accuracy.

## When NOT to use

- Input is a pre-existing flat or unstructured spectral database already in use; hierarchical indexing incurs upfront computational cost and is justified only if lookup speed or accuracy is the bottleneck.
- Chemical space is small or query frequency is low; hierarchical indexing overhead (memory, index construction) outweighs benefits.
- Fragmentation rules for your domain are unknown or poorly defined; the quality of the library depends on rule accuracy, and guessing rules will produce false positives.

## Inputs

- Lipid class taxonomy definition (carbon count ranges, unsaturation rules)
- Fragmentation ruleset (neutral loss patterns, characteristic ion generation rules)
- Known lipid standards (for validation)
- Mass spectrometry spectral data (mzML format, e.g., MS1 m/z and MS2 fragment patterns)

## Outputs

- Hierarchical database index (lipid class → chain composition → positional isomer)
- Theoretical m/z library with fragmentation patterns
- Fast lookup table or index structure (e.g., .rda, compiled data format)
- Validation report (entry count, spot-check results against standards)

## How to apply

First, define the chemistry taxonomy (lipid class rules, acyl chain carbon count ranges, degree-of-unsaturation constraints). Enumerate all valid structures by iterating over carbon counts and unsaturation levels, generating all positional isomers for each composition. For each structure, compute theoretical m/z fragment ions using domain rules (e.g., neutral loss, characteristic ion patterns). Organize the full enumerated set into a multilevel hierarchical index—typically lipid class → chain composition → positional isomer—that allows fast prefix-matching and range queries. Validate completeness by spot-checking fragment patterns against known standards and verifying entry count. This design, as demonstrated in LipidIN, reduces spectral querying from billions of candidate comparisons to sub-second lookups via greedy secondary matching algorithms primed with hierarchical structure.

## Related tools

- **XCMS** (Processes mass spectrometry data (mzML format) for peak alignment, matching and identification; used upstream to generate experimental spectral data queried against the hierarchical library.)
- **CAMERA** (Extracts and annotates compound spectra from LC/MS datasets; integrates with spectral querying to refine candidate annotations.)
- **LipidIN Expeditious Querying (EQ) Module** (Implements secondary matching algorithm and normalization against the hierarchical lipid fragmentation library to perform ~70 billion spectral queries in <1 second.) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
load(paste(getwd(),'/MS1_MS2_library.rda',sep='')); source(paste(getwd(),'/EQ.r',sep='')); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Entry count matches target enumeration (e.g., 168.6 million lipids); verify by statistical sampling or checksum of enumerated compositions.
- Hierarchical index structure preserves all regioisomeric variants; validate by confirming that known lipid standards map to correct branch paths (lipid class → chain composition → positional isomer).
- Fragment ion m/z values for sampled entries match published or experimentally confirmed standards; spot-check ≥5 lipid standards across multiple lipid classes.
- Query latency is <1 second for spectral datasets; measure end-to-end time for 70 billion candidate queries (as reported in LipidIN).
- False discovery rate on annotated lipids is acceptable (LipidIN reports 5.7% FDR over 8923 lipids); validate via orthogonal method (e.g., retention time model, independent MS/MS confirmation).

## Limitations

- Library completeness depends on accuracy of fragmentation rules; if rules are incomplete or incorrect, regioisomers and chain compositions will be missed or misidentified.
- Memory footprint scales with chemical space size; LipidIN's 168.6 million entries require substantial storage (e.g., .rda format compression); practical deployment may require distributed indexing for larger chemical ontologies.
- Hierarchical index must be rebuilt if taxonomy or fragmentation rules change; maintenance burden increases with rule complexity and scope.
- Data format conversion for hierarchical indexing is computationally intensive; LipidIN reports ~2 minutes conversion time for mzML to indexed .rda format per file.

## Evidence

- [intro] LipidIN features a 168.6 million lipid fragmentation hierarchical library that encompasses all potential chain compositions and carbon-carbon double bond locations.: "168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"
- [other] Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition.: "Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants"
- [other] Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup.: "Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup"
- [intro] Expeditious querying module speeds up to around 70 billion times' spectral querying in less than 1 second.: "expeditious querying module speeds up to around 70 billion times' spectral querying in less than 1 second"
- [readme] This task involves searching a 4-level hierarchical library, which is efficient in terms of querying. However, the data format conversion process for the LCI module takes approximately 2 minutes.: "searching a 4-level hierarchical library, which is efficient in terms of querying. However, the data format conversion process for the LCI module takes approximately 2 minutes"
