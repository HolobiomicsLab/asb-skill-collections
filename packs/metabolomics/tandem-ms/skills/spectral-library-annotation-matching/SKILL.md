---
name: spectral-library-annotation-matching
description: Use when when you have downloaded a GNPS archive (GNPS1 or GNPS2 workflows) and need to map experimental spectra to known library compounds for annotation enrichment. Apply this skill after spectral data (spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3375
  tools:
  - nplinker
  - Python
  - pytest
  - GNPS
  techniques:
  - tandem-MS
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

# spectral-library-annotation-matching

## Summary

Load and structure spectral annotations from GNPS archives by parsing annotation.tsv files to produce Annotation records mapping experimental spectra to library compounds. This enables downstream molecular family and BGC-to-metabolite linking in natural products discovery workflows.

## When to use

When you have downloaded a GNPS archive (GNPS1 or GNPS2 workflows) and need to map experimental spectra to known library compounds for annotation enrichment. Apply this skill after spectral data (spectra.mgf) and molecular family data have been loaded, to populate the annotation layer required for computing spectrum-to-compound relationships.

## When NOT to use

- GNPS archive has not been downloaded or extracted — use download and extraction steps first
- Annotation file is missing or malformed — validate archive completeness before loading
- Spectrum objects have not been loaded — load spectra.mgf via GNPSSpectrumLoader before mapping annotations

## Inputs

- Extracted GNPS archive directory
- annotations.tsv file (from GNPS molecular networking output)
- Spectrum objects (loaded from spectra.mgf)
- GNPSFormat object initialized with workflow version

## Outputs

- Annotation records (spectrum-to-compound mappings)
- Structured compound metadata linked to spectra
- Cross-validated annotation–spectrum index

## How to apply

Initialize a GNPSFormat object from the extracted GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2). Use GNPSAnnotationLoader to parse the annotations.tsv file to produce Annotation records. Validate that all loaded records contain required fields and maintain consistent cross-references between annotations and the corresponding Spectrum objects loaded from spectra.mgf. The annotation records should preserve the spectrum-to-library-compound mapping and any confidence scores or metadata present in the source file.

## Related tools

- **nplinker** (Framework providing GNPSAnnotationLoader, GNPSFormat, and annotation validation logic for GNPS archive parsing) — https://github.com/NPLinker/nplinker
- **Python** (Runtime environment for executing nplinker annotation loaders and validation (version ≥3.11))
- **GNPS** (Source of molecular networking archives containing annotations.tsv files and associated spectral data) — https://gnps.ucsd.edu

## Examples

```
from nplinker import npl; npl.load_data(gnps_dir='./gnps', workflow_version='METABOLOMICS-SNETS-V2'); annotations = npl.get_annotations()
```

## Evaluation signals

- All Annotation records contain required fields (spectrum ID, compound ID, confidence score) with no missing values
- Cross-reference consistency: every annotation spectrum_id matches a loaded Spectrum object from spectra.mgf
- Annotation records preserve all metadata columns from source annotations.tsv (e.g., library_match, compound_name)
- pytest passes on existing test suite covering annotation loading and validation workflows
- Annotation count and content match independent verification of the source GNPS archive

## Limitations

- Only supports GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows; other platforms require custom loaders
- Requires pre-downloaded and extracted GNPS archive — online/streaming mode not supported in this workflow step
- Annotation quality and coverage depend on GNPS library size and experimental spectral quality at time of networking

## Evidence

- [other] Load spectral annotations using GNPSAnnotationLoader with the annotations.tsv file to produce Annotation records mapping spectra to library compounds.: "Load spectral annotations using GNPSAnnotationLoader with the annotations.tsv file to produce Annotation records mapping spectra to library compounds."
- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version"
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)."
- [readme] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
- [other] npl.load_data(): "The GNPS loader processes downloaded GNPS archive data through npl.load_data() to generate structured spectra, molecular family, annotation, and file-mapping records"
