---
name: gnps-molecular-networking-data-parsing
description: Use when you have downloaded a GNPS archive from either GNPS1 (https://gnps.ucsd.edu) or GNPS2 (https://gnps2.org) and need to programmatically load and validate its contents (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3520
  tools:
  - nplinker
  - Python
  - pytest
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

# gnps-molecular-networking-data-parsing

## Summary

Parse GNPS (Global Natural Products Social Molecular Networking) archive downloads into structured records for spectra, molecular families, annotations, and file mappings. This skill transforms raw GNPS workflow outputs into validated, interconnected data objects suitable for downstream natural product–genome linking analysis.

## When to use

You have downloaded a GNPS archive from either GNPS1 (https://gnps.ucsd.edu) or GNPS2 (https://gnps2.org) and need to programmatically load and validate its contents (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv) into an in-memory representation before computing spectral-to-genomic links or performing comparative metabolomics analysis.

## When NOT to use

- GNPS data has not yet been downloaded or extracted to a local directory — use GNPS web interface or API first.
- Input archive is from a non-standard GNPS workflow version not listed (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow) — clarify workflow type before parsing.
- You require only raw spectral peak lists without molecular family or annotation context — use a simpler .mgf parser instead.

## Inputs

- GNPS archive directory (extracted)
- spectra.mgf file (Mascot Generic Format spectral data)
- molecular_families.tsv file (molecular family graph edges)
- annotations.tsv file (spectral-to-library-compound mappings)
- file_mappings.tsv or file_mappings.csv file (strain-to-spectrum mappings)
- GNPS workflow version identifier string

## Outputs

- Spectrum objects (validated spectral records)
- MolecularFamily graph edges
- Annotation records (spectra-to-library mappings)
- File mapping records (strain-to-spectrum associations)
- Validation report (completeness and cross-reference consistency)

## How to apply

Use NPLinker's GNPS loader component to reconstruct the archive into structured records. First, initialize a GNPSFormat object from the extracted archive path using gnps_format_from_archive() or gnps_format_from_file_mapping(), specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, or FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2). Then sequentially invoke GNPSSpectrumLoader on spectra.mgf to produce Spectrum objects, GNPSMolecularFamilyLoader on molecular_families.tsv to produce graph edges, GNPSAnnotationLoader on annotations.tsv to link spectra to library compounds, and GNPSFileMappingLoader on file_mappings.tsv (or .csv) to map strains to spectra. Finally, validate all loaded records for completeness, verifying that no required fields are missing and cross-references between spectra, families, and annotations are consistent.

## Related tools

- **nplinker** (Python framework providing GNPSFormat, GNPSSpectrumLoader, GNPSMolecularFamilyLoader, GNPSAnnotationLoader, and GNPSFileMappingLoader components for parsing and validating GNPS archives) — https://github.com/NPLinker/nplinker
- **pytest** (Unit testing framework for validating completeness and consistency of parsed records)
- **Python** (Runtime language (≥3.11) for executing GNPS loader code)

## Examples

```
from nplinker import GNPSFormat; gnps = GNPSFormat.from_archive('./gnps_archive', workflow_version='METABOLOMICS-SNETS-V2'); spectra = gnps.spectra; families = gnps.molecular_families; annotations = gnps.annotations; assert len(spectra) > 0 and len(families) > 0 and len(annotations) > 0
```

## Evaluation signals

- All Spectrum objects contain required fields (ID, m/z array, intensity array) and no null values.
- MolecularFamily edges have valid cross-references to spectrum IDs on both ends; no dangling references.
- Annotation records link each annotated spectrum to at least one library compound with valid cosine similarity or other scoring metric.
- File mapping records establish 1:N relationships between strains and spectra; verify cardinality matches the input file.
- Run pytest on the loader module to confirm existing tests still pass after parsing; check for parser exceptions and schema violations.

## Limitations

- Supports only GNPS1 and GNPS2 workflow outputs; other molecular networking formats require separate parsers.
- Validates cross-reference consistency but does not perform spectral quality filtering, outlier detection, or annotation reliability scoring — those are downstream steps.
- File mapping parsing requires well-formed TSV/CSV headers and consistent column naming; malformed headers will cause parser errors.
- Molecular family edge validation depends on consistent node identifiers across spectra.mgf and molecular_families.tsv; mismatched IDs will result in missing edges or validation failures.

## Evidence

- [other] The GNPS loader processes downloaded GNPS archive data through npl.load_data() to generate structured spectra, molecular family, annotation, and file-mapping records for downstream analysis.: "The GNPS loader processes downloaded GNPS archive data through npl.load_data() to generate structured spectra, molecular family, annotation, and file-mapping records for downstream analysis."
- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version"
- [other] Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects.: "Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects."
- [other] Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv file to produce MolecularFamily graph edges.: "Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv file to produce MolecularFamily graph edges."
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)."
