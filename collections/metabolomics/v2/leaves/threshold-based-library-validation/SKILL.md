---
name: threshold-based-library-validation
description: Use when you have downloaded or cloned a fragmentation library repository
  (such as LipidMatch) and need to verify that it contains the expected breadth of
  coverage across both molecular diversity (distinct species count) and chemical classification
  (lipid-type category count).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - LipidMatch
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# threshold-based-library-validation

## Summary

Validate the comprehensiveness and composition of a fragmentation library by enumerating distinct molecular species and categories against pre-defined quantitative thresholds. This skill verifies whether a library meets or exceeds minimum coverage requirements (e.g., ≥500,000 species across ≥60 lipid types) to qualify for use in high-confidence lipidomics annotation workflows.

## When to use

Apply this skill when you have downloaded or cloned a fragmentation library repository (such as LipidMatch) and need to verify that it contains the expected breadth of coverage across both molecular diversity (distinct species count) and chemical classification (lipid-type category count). Use it as a validation gate before integrating the library into a peak annotation pipeline, especially when the library's documented coverage is critical to your downstream analysis confidence or when you are curating library files for a new instrument platform or lipid class set.

## When NOT to use

- Do not use this skill if you need to validate the accuracy of fragmentation predictions or match quality against experimental mass spectra; this skill only measures library scale and diversity, not prediction correctness.
- Do not apply this skill to peak-picking output or feature tables from MZmine, XCMS, MS-DIAL, or Compound Discoverer; this skill is for validating the library itself, not for matching experimental data to it.
- Do not use this skill if you only need to integrate a library into a workflow; validation of coverage is distinct from technical integration with peak-picking or annotation software.

## Inputs

- Library .csv files from a fragmentation library repository (e.g., GarrettLab-UF/LipidMatch)
- Species threshold value (numeric, e.g., 500000)
- Lipid-type category threshold value (numeric, e.g., 60)

## Outputs

- Aggregated set of distinct lipid species identifiers
- Enumerated list of distinct lipid-type categories
- Summary validation report with species count, category count, and pass/fail status for each threshold

## How to apply

Begin by cloning or downloading the library repository and locating all library files (typically in .csv format). Parse each .csv file to extract lipid species identifiers and their assigned lipid-type category labels. Aggregate all distinct species identifiers across all files using set-based deduplication to ensure no species is double-counted. Enumerate the distinct lipid-type categories present in the aggregated dataset. Compare the total species count against the species threshold (e.g., 500,000) and the category count against the category threshold (e.g., 60). Generate a summary report documenting the observed species count, category count, and pass/fail status for each threshold. The rationale is that a library with sufficient breadth is more likely to match diverse lipid structures encountered in untargeted HRMS/MS experiments across multiple acquisition modes (targeted, data-dependent, all-ion fragmentation).

## Related tools

- **LipidMatch** (The library subject being validated; provides in-silico fragmentation libraries in .csv format) — https://github.com/GarrettLab-UF/LipidMatch

## Examples

```
# Clone repository, parse all .csv library files, count distinct species and categories, and report pass/fail status against 500,000 species and 60 category thresholds; pseudocode: species = set(); categories = set(); [parse each .csv to extract species IDs and category labels, add to respective sets]; report(len(species) >= 500000, len(categories) >= 60)
```

## Evaluation signals

- Species count matches or exceeds the pre-defined threshold (e.g., 500,000+); verify via aggregated set cardinality.
- Lipid-type category count matches or exceeds the pre-defined threshold (e.g., 60+); verify via enumeration of unique category labels.
- No duplicate species identifiers appear in the aggregated output; set deduplication ensures unique count.
- All .csv files in the repository are successfully located, parsed, and included in the aggregation; no library files are skipped.
- The pass/fail report clearly documents both the observed counts and the thresholds, making it suitable for documentation or release notes.

## Limitations

- This skill validates only quantitative breadth (species count and category count); it does not assess the chemical accuracy, biological relevance, or correctness of fragmentation patterns for individual species.
- The skill assumes .csv library files follow a consistent schema with parseable species identifiers and category assignments; variations in file format or missing fields may require custom parsing logic.
- No changelog is available in the LipidMatch repository to track whether thresholds have changed across versions; practitioners should confirm thresholds against the version in use.
- The skill does not account for overlap or redundancy between categories; a species may be counted in only one category, but category interdependencies are not evaluated.

## Evidence

- [intro] Library coverage requirement: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [other] File format and parsing approach: "Parse each .csv file to extract lipid species identifiers and lipid-type category assignments"
- [other] Aggregation and deduplication method: "Aggregate distinct lipid species across all files using a set or unique count operation"
- [other] Enumeration and comparison logic: "Compare total species count against the threshold of 500,000 and lipid-type category count against 60"
- [other] Output deliverable: "Generate a summary report documenting species count, category count, and pass/fail status for each threshold"
