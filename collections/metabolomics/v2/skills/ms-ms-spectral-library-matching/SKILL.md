---
name: ms-ms-spectral-library-matching
description: Use when you have experimental MS/MS spectra from nontargeted metabolomics
  data and need to assign molecular identities or identify structurally related analogs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - masscube
  - Python
  - TandemMatch
  - Mirador
  - PeakQC
  techniques:
  - LC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
- doi: 10.1021/jasms.4c00146
  title: ''
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
- masscube is an integrated Python package
- 'TandemMatch: MS/MS spectral library matching with support for MSP and CSV library
  formats.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  - 10.1021/jasms.4c00146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-ms-spectral-library-matching

## Summary

Annotate experimental MS/MS spectra by matching them against a reference spectral library using both identity search (exact or high-confidence matches) and fuzzy/analog search (similarity-based matching for structurally related compounds). This skill disambiguates unknown metabolites by leveraging known fragmentation patterns.

## When to use

You have experimental MS/MS spectra from nontargeted metabolomics data and need to assign molecular identities or identify structurally related analogs. Use this skill when you have access to a curated spectral library reference and want to move beyond peak detection to confident annotation of feature groups, isotopes, adducts, and in-source fragments.

## When NOT to use

- Your spectral library is incomplete, biased, or mismatched to your sample type (e.g., plant library applied to bacterial metabolites)—results will be unreliable or misleading.
- You have no reference spectral library or only MS1-level data; identity search requires library spectra with fragmentation patterns.
- Your MS/MS spectra are of very low quality (high noise, poor fragmentation) or from novel compounds not represented in any library; fuzzy search may yield spurious low-confidence matches.

## Inputs

- experimental MS/MS spectra (mz-intensity pairs, scan metadata)
- reference spectral library (library spectra with known identities, fragmentation patterns, and metadata)

## Outputs

- annotated spectrum records with assigned identities
- match type annotations (identity vs. analog)
- confidence scores per match
- merged identity and fuzzy search results ranked by confidence

## How to apply

Load experimental MS/MS spectra and a reference spectral library into masscube. First, perform identity search by matching experimental spectra against library spectra using exact or high-confidence similarity scoring to detect direct matches. Then, perform fuzzy/analog search to identify compounds with similar fragmentation patterns but different molecular identities—this captures structurally related analogs and novel metabolites. Merge the two result sets, prioritizing high-confidence identity matches while retaining fuzzy matches as secondary annotations. Emit annotated spectrum records containing the original spectrum data, assigned identity or analog annotation, match type (identity or analog), and confidence score. Use the combined results to build a reliable annotation table for downstream metabolomic analysis.

## Related tools

- **masscube** (integrated Python package that implements identity search and fuzzy/analog search workflows for MS/MS spectrum annotation against spectral libraries) — https://github.com/huaxuyu/masscube/

## Evaluation signals

- All experimental spectra receive either an identity match or an analog (fuzzy) match with a confidence score; no spectra are left unannotated if library coverage is adequate.
- Identity matches have higher confidence scores than fuzzy matches for the same compound; ranking is monotonic by match type and statistical similarity metric.
- For benchmarked spectra (e.g., standards in the library), identity search recovers the correct compound identity with ≥95% accuracy and high cosine similarity (or equivalent metric).
- Fuzzy search results identify structurally plausible analogs (confirmed by chemical taxonomy or experimental co-annotation) rather than random false positives.
- Reproducibility: re-running the same spectra and library against masscube yields identical annotations and confidence scores.

## Limitations

- Identity search relies on spectral library completeness and quality; rare metabolites or novel compounds absent from the library will not be annotated.
- Fuzzy/analog search threshold for 'similarity' is user-configurable and affects sensitivity and specificity; too lenient thresholds yield false analogs, while too strict thresholds miss genuine structural relatives.
- MS/MS fragmentation can be instrument-dependent (e.g., collision energy, ionization mode); matches are most reliable within the same instrument type and acquisition method as the library.
- No changelog is publicly available, limiting visibility into algorithm updates or changes in matching behavior across versions.

## Evidence

- [other] masscube implements MS/MS spectrum annotation through two complementary search strategies: "masscube implements MS/MS spectrum annotation through two complementary search strategies: identity search for direct spectral library matching and fuzzy search (analog search) for similarity-based"
- [other] identity search by matching experimental spectra against library spectra using exact or high-confidence similarity scoring: "Perform identity search by matching experimental spectra against library spectra using exact or high-confidence similarity scoring."
- [other] fuzzy/analog search to identify structurally related compounds with similar fragmentation patterns but different molecular identities: "Perform fuzzy/analog search to identify structurally related compounds with similar fragmentation patterns but different molecular identities."
- [other] Merge identity and fuzzy search results, prioritizing high-confidence matches: "Merge identity and fuzzy search results, prioritizing high-confidence matches."
- [readme] Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search): "Annotation of MS/MS spectra via identity search and fuzzy search (i.e. analog search)."
