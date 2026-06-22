---
name: cross-workflow-format-translation
description: Use when you have downloaded a GNPS archive from either GNPS1 (https://gnps.ucsd.edu) or GNPS2 (https://gnps2.org) and need to parse spectra (spectra.mgf), molecular family networks (molecular_families.tsv), spectral library annotations (annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# cross-workflow-format-translation

## Summary

Translate GNPS molecular networking archive data from heterogeneous workflow versions (GNPS1 classical/feature-based, GNPS2 workflows) into unified structured records (Spectrum, MolecularFamily, Annotation, FileMapping objects) for downstream computational linking of genomics and metabolomics.

## When to use

You have downloaded a GNPS archive from either GNPS1 (https://gnps.ucsd.edu) or GNPS2 (https://gnps2.org) and need to parse spectra (spectra.mgf), molecular family networks (molecular_families.tsv), spectral library annotations (annotations.tsv), and sample-to-strain mappings (file_mappings.tsv/.csv) into a machine-readable format compatible with NPLinker's data mining pipeline. Apply this skill when the GNPS workflow version is known (e.g., METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2) and you need to validate cross-references between spectra, families, and annotations before linking to genomic data.

## When NOT to use

- Input is not a GNPS molecular networking output (e.g., raw LC-MS/MS data in mzML or mzXML format); use a spectral feature detection tool (e.g., MZmine, xcms) first.
- GNPS workflow version is unknown or undocumented; without workflow metadata (METABOLOMICS-SNETS, FEATURE-BASED-MOLECULAR-NETWORKING, etc.), the parser cannot correctly interpret column semantics in annotations.tsv or molecular_families.tsv.
- File mappings (strain-to-spectrum links) are missing or incomplete; if you have only spectra and molecular families but no provenance to genomic samples, defer file-mapping loading and adjust validation scope.

## Inputs

- GNPS archive directory (downloaded and extracted)
- spectra.mgf (MSn spectral data in MGF format)
- molecular_families.tsv (network edge list)
- annotations.tsv (spectrum-to-library-compound mappings)
- file_mappings.tsv or file_mappings.csv (strain/sample identifiers)

## Outputs

- Spectrum objects (with m/z arrays, retention times, scan metadata)
- MolecularFamily graph edges (spectrum pair relationships)
- Annotation records (spectrum–library-compound associations with match scores)
- FileMapping records (strain/sample-to-spectrum provenance)

## How to apply

Initialize a GNPSFormat object by calling gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions with the extracted GNPS archive path and the target workflow version identifier. Load spectra using GNPSSpectrumLoader on spectra.mgf to produce Spectrum objects with mass-to-charge ratios, retention times, and fragmentation patterns. Load molecular family graph edges using GNPSMolecularFamilyLoader on molecular_families.tsv, which encodes network connectivity between related spectra. Load spectral annotations using GNPSAnnotationLoader on annotations.tsv to map each spectrum to reference library compounds with match scores and metadata. Load file mappings using GNPSFileMappingLoader on file_mappings.tsv (or .csv) to establish strain-to-spectrum provenance links. Validate all loaded records for completeness: confirm no required fields are missing, verify cross-references are internally consistent (e.g., all annotation spectrum IDs exist in the Spectrum collection), and ensure molecular family edges reference only known spectra. Use pytest to confirm validation passes before downstream linking operations.

## Related tools

- **nplinker** (Python framework that orchestrates GNPS loader components (GNPSSpectrumLoader, GNPSMolecularFamilyLoader, GNPSAnnotationLoader, GNPSFileMappingLoader) to transform GNPS archive formats into structured data objects (Spectrum, MolecularFamily, Annotation, FileMapping) for genomics-metabolomics linking) — https://github.com/NPLinker/nplinker
- **GNPS** (Source metabolomics platform that produces molecular networking outputs in TSV and MGF formats (both GNPS1 at https://gnps.ucsd.edu and GNPS2 at https://gnps2.org)) — https://gnps.ucsd.edu
- **pytest** (Testing framework used to validate that loaded records are complete, cross-references are consistent, and no required fields are missing)

## Examples

```
from nplinker import GNPSFormat, GNPSSpectrumLoader, GNPSMolecularFamilyLoader, GNPSAnnotationLoader, GNPSFileMappingLoader; gnps = GNPSFormat.from_archive('/path/to/gnps_archive', workflow_version='FEATURE-BASED-MOLECULAR-NETWORKING'); spectra = GNPSSpectrumLoader(gnps).load(); families = GNPSMolecularFamilyLoader(gnps).load(); annotations = GNPSAnnotationLoader(gnps).load(); mappings = GNPSFileMappingLoader(gnps).load()
```

## Evaluation signals

- No missing required fields in Spectrum, MolecularFamily, Annotation, or FileMapping records; inspect record.validate() or schema assertions for null/empty checks.
- All annotation spectrum IDs exist in the loaded Spectrum collection; perform set intersection of annotation.spectrum_id and {s.id for s in spectra_list}.
- All molecular family edge endpoints (both spectrum indices) reference known spectra; verify edge.spectrum_a and edge.spectrum_b are in the Spectrum ID set.
- File mapping strain/sample identifiers match at least one spectrum file source; cross-check FileMapping.sample_id against spectra metadata to confirm no orphaned mappings.
- pytest test suite passes (existing tests still work), confirming parser output schema and type consistency.

## Limitations

- Parser requires explicit GNPS workflow version specification (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2); mismatched version labels will produce incorrect column mappings or schema violations.
- Cross-references between spectra, families, and annotations are validated for existence and consistency but not for semantic correctness (e.g., a spectrum may be marked as annotated even if match score is very low); domain-specific filtering (e.g., cosine similarity > 0.7) must be applied downstream.
- File mappings require exact string matching between sample identifiers in file_mappings.tsv and spectrum metadata; inconsistent naming or encoding (e.g., whitespace, case sensitivity, special characters) will silently create orphaned records.
- No automatic handling of GNPS workflow updates or schema drifts; if GNPS modifies MGF or TSV column headers between versions, loader configurations must be manually updated.

## Evidence

- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or"
- [other] Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects. Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv file to produce MolecularFamily graph edges. Load spectral annotations using GNPSAnnotationLoader with the annotations.tsv file to produce Annotation records.: "Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects. Load molecular families using GNPSMolecularFamilyLoader with the molecular_families.tsv"
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "python framework for data mining microbial natural products by integrating genomics and metabolomics data"
