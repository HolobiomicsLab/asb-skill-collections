---
name: molecular-family-graph-construction
description: Use when you have downloaded and extracted a GNPS archive (from METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow/feature_based_molecular_networking_workflow for GNPS2) and need to construct a queryable molecular family graph.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - pytest
  - GNPS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-022-01444-3
  all_source_dois:
  - 10.1186/s40168-022-01444-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-family-graph-construction

## Summary

Construct a graph of molecular families from GNPS molecular networking data by loading and validating family relationships from structured tab-separated files. This skill transforms raw GNPS archive outputs into validated graph edges that represent spectral similarity clusters for downstream natural product linking.

## When to use

Apply this skill when you have downloaded and extracted a GNPS archive (from METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow/feature_based_molecular_networking_workflow for GNPS2) and need to construct a queryable molecular family graph to support genomics–metabolomics correlation analysis. Use this skill as part of the data loading pipeline before computing NPLinker scores or performing strain-compound predictions.

## When NOT to use

- GNPS archive has not been extracted or is corrupted (missing molecular_families.tsv file).
- Spectrum data has not been loaded or validated prior to family graph construction (missing Spectrum objects for cross-reference).
- Workflow version identifier is incorrect or unsupported (not one of the five supported GNPS1/GNPS2 workflows).
- Molecular family file contains non-numeric or out-of-range similarity scores (outside [0, 1]).

## Inputs

- GNPS archive (extracted directory)
- GNPS workflow version identifier (string: METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow)
- molecular_families.tsv file (tab-separated, containing spectrum pair IDs and similarity metrics)
- Previously loaded Spectrum object pool (for cross-reference validation)

## Outputs

- MolecularFamily graph edges (spectrum pair → similarity score relationships)
- Validated molecular family graph structure (nodes = spectra, edges = family relationships)
- Cross-reference validation report (spectra matched, missing IDs flagged)

## How to apply

Initialize a GNPSFormat object by specifying the extracted GNPS archive path and workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow). Load the molecular_families.tsv file using GNPSMolecularFamilyLoader to parse spectral pair relationships and their similarity scores. Construct MolecularFamily graph edges with nodes representing spectra and edge weights representing cosine similarity or other GNPS-computed metrics. Validate all edges for completeness (no missing spectrum IDs, all similarity scores within expected range [0, 1]). Cross-reference loaded family edges against the previously loaded Spectrum records to ensure referential integrity—every spectrum ID in family edges must correspond to a Spectrum object in the spectra pool. The rationale is that valid graph construction depends on upstream spectral loading and downstream consistency checking; premature graph construction before spectrum validation will propagate missing-data errors.

## Related tools

- **nplinker** (Provides GNPSFormat, GNPSMolecularFamilyLoader, and MolecularFamily classes for archive parsing and graph construction) — https://github.com/NPLinker/nplinker
- **GNPS** (Generates molecular networking archives and molecular_families.tsv files containing spectral cluster relationships) — https://gnps.ucsd.edu
- **pytest** (Validates graph construction correctness via automated unit and integration tests)

## Examples

```
from nplinker import GNPSFormat, GNPSMolecularFamilyLoader; gnps = GNPSFormat.gnps_format_from_archive('/path/to/gnps', workflow_version='FEATURE-BASED-MOLECULAR-NETWORKING'); families = GNPSMolecularFamilyLoader(gnps).load()
```

## Evaluation signals

- All edges in the molecular family graph reference valid spectrum IDs that exist in the Spectrum object pool (referential integrity check).
- All similarity scores in edges fall within the expected range [0.0, 1.0] with no NaN or missing values.
- Graph node count matches the number of unique spectrum IDs referenced in molecular_families.tsv.
- Cross-reference validation reports zero missing spectrum IDs; any missing IDs are flagged with spectrum ID and family edge index for debugging.
- Graph loads and queries without errors (e.g., `npl.load_data()` completes without exception; edges are iterable and filterable by similarity threshold).

## Limitations

- Graph construction requires a prior call to GNPSSpectrumLoader; missing spectra will cause referential integrity failures.
- Currently supports only GNPS1 (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING) and GNPS2 (classical_networking_workflow, feature_based_molecular_networking_workflow) workflow outputs; other GNPS versions or non-GNPS molecular networking formats are not supported.
- Similarity scores are derived from GNPS cosine-similarity metrics and do not reflect post-hoc or user-customized scoring; custom edge weights cannot be injected after graph construction without loader re-initialization.
- No discussion of edge-case handling or failure modes (e.g., duplicate edges, self-loops, disconnected components) is provided in available documentation.

## Evidence

- [other] Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv file to produce MolecularFamily graph edges.: "Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv file to produce MolecularFamily graph edges."
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)."
- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version"
- [other] The GNPS loader processes downloaded GNPS archive data through npl.load_data() to generate structured spectra, molecular family, annotation, and file-mapping records for downstream analysis.: "The GNPS loader processes downloaded GNPS archive data through npl.load_data() to generate structured spectra, molecular family, annotation, and file-mapping records for downstream analysis."
