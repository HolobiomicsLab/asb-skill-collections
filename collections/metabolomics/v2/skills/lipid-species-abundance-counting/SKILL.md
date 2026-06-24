---
name: lipid-species-abundance-counting
description: Use when you have access to a lipidomics library repository (e.g., LipidMatch
  .csv files) and need to audit or report the total number of distinct lipid species
  and lipid-type categories present.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - LipidMatch
  techniques:
  - mass-spectrometry
  license_tier: open
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

# lipid-species-abundance-counting

## Summary

Count and enumerate distinct lipid species and their type categories within in-silico fragmentation libraries to verify library comprehensiveness. This skill validates that a lipidomics reference resource meets predefined thresholds for species diversity and lipid-type coverage.

## When to use

Apply this skill when you have access to a lipidomics library repository (e.g., LipidMatch .csv files) and need to audit or report the total number of distinct lipid species and lipid-type categories present. Use it specifically when stakeholders or publication standards require documented evidence that the library contains at least a target number of species (e.g., 500,000) across a minimum number of lipid-type categories (e.g., 60+).

## When NOT to use

- Input is experimental mass spectrometry data (raw .raw, .mzML, .mzXML, or .netCDF files) rather than a library repository — use peak picking and fragment matching instead.
- Goal is to identify and annotate lipids in a specific sample rather than audit library completeness — use LipidMatch fragmentation matching workflow instead.
- Library files are already pre-counted or summarized — this skill is redundant if the repository already publishes aggregated species and category counts in documentation.

## Inputs

- LipidMatch .csv library files (or equivalent lipidomics library in tabular format with lipid species identifiers and lipid-type assignments)
- Target thresholds for species count and lipid-type category count

## Outputs

- Summary report documenting total distinct lipid species count
- Summary report documenting total distinct lipid-type category count
- Pass/fail status for each threshold comparison
- Aggregated inventory of unique lipid species and categories

## How to apply

Clone or download the target library repository and locate all .csv library files. Parse each .csv file to extract lipid species identifiers and their assigned lipid-type categories. Aggregate all species identifiers using a set or unique-count operation to eliminate duplicates across files. Enumerate the distinct lipid-type categories present in the aggregated dataset. Compare the total unique species count against the target threshold (e.g., 500,000) and the category count against the minimum threshold (e.g., 60). Document pass/fail status for each threshold metric. The rationale is that in-silico fragmentation libraries must offer sufficient breadth to support comprehensive lipid identification across diverse experimental samples; this skill provides a reproducible, quantitative audit trail.

## Related tools

- **LipidMatch** (Source library repository containing in-silico fragmentation libraries in .csv format to be parsed and counted) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- Total unique species count matches or exceeds the published threshold (e.g., 500,000+) when aggregating across all library files.
- Total distinct lipid-type categories meets or exceeds the published threshold (e.g., 60+) when enumerating all category labels.
- No duplicate species identifiers are counted; set-based aggregation produces consistent unique counts on repeated runs.
- All .csv files in the repository are successfully parsed and included in the aggregation (file discovery completeness check).
- Pass/fail status for each threshold is documented and matches the expected outcome stated in the repository README or publication.

## Limitations

- This skill does not validate the biochemical accuracy or fragmentation correctness of individual lipid species in the library — it only counts entries.
- The skill assumes .csv files are well-formed and consistently formatted; malformed or inconsistently structured files may lead to incomplete or erroneous counts.
- Duplicate or redundant species entries within files or across files may not be immediately obvious; deduplication logic must handle species identifier normalization (e.g., case sensitivity, whitespace).
- The skill provides no information about the distribution of species across lipid types, metabolic relevance, or applicability to specific sample types or instrument platforms.
- LipidMatch does not currently support Waters files, so species coverage for Waters-based workflows may be incomplete if cross-platform harmonization is needed.

## Evidence

- [other] Library comprehensiveness validation: "LipidMatch contains in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [other] Workflow steps for counting: "1. Clone or download the LipidMatch GitHub repository (GarrettLab-UF/LipidMatch). 2. Locate and load all .csv library files from the repository. 3. Parse each .csv file to extract lipid species"
- [other] Reporting output format: "Generate a summary report documenting species count, category count, and pass/fail status for each threshold"
- [readme] Repository file format and accessibility: "The link at the bottom of this page contains a manual, lipid libraries in .csv format, a batch file for lipidomics with MZmine processing, and LipidMatch software/scripts."
