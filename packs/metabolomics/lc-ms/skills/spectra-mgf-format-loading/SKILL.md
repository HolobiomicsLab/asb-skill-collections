---
name: spectra-mgf-format-loading
description: Use when when you have downloaded a GNPS molecular networking archive (GNPS1 or GNPS2 workflow output) and need to reconstruct spectral records for integration with genomic data (BGCs, antiSMASH results) or for computing molecular family links and spectral similarity scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
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

# spectra-mgf-format-loading

## Summary

Load and parse mass spectrometry spectral data from MGF (Mascot Generic Format) files into structured Spectrum objects for downstream molecular networking and annotation analysis. This skill extracts fragmentation spectra, precursor masses, and metadata from GNPS archive outputs.

## When to use

When you have downloaded a GNPS molecular networking archive (GNPS1 or GNPS2 workflow output) and need to reconstruct spectral records for integration with genomic data (BGCs, antiSMASH results) or for computing molecular family links and spectral similarity scores. Apply this skill as the first data-loading step after archive extraction and before molecular family or annotation loading.

## When NOT to use

- Input spectra are already in a native database format (e.g., mzML, mzXML) — use format conversion tools first.
- Spectral data comes from a non-GNPS source without clear MGF formatting — verify file structure and GNPS compatibility.
- You only need molecular family edges or annotations without spectral records — load those independently using GNPSMolecularFamilyLoader or GNPSAnnotationLoader.

## Inputs

- spectra.mgf file (from extracted GNPS archive)
- GNPS workflow version identifier (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING, classical_networking_workflow, or feature_based_molecular_networking_workflow)

## Outputs

- Spectrum objects (structured records with precursor m/z, retention time, fragment peaks, and metadata)
- Validated spectral dataset ready for molecular family linking and annotation mapping

## How to apply

Initialize a GNPSFormat object from the extracted GNPS archive by specifying the workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, or FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2). Pass the spectra.mgf file path to GNPSSpectrumLoader, which parses each spectrum entry—including precursor m/z, retention time, fragmentation peaks, and scan metadata—and produces structured Spectrum objects. Validate that all Spectrum records contain required fields (precursor mass, fragment peaks) and that spectrum identifiers are consistent with cross-references in downstream molecular_families.tsv and annotations.tsv files. Confirm that no spectra are missing or have malformed peak lists before proceeding to molecular family or annotation loading.

## Related tools

- **nplinker** (Provides GNPSSpectrumLoader class, GNPSFormat helper functions, and npl.load_data() API for parsing and loading MGF spectral data from GNPS archives) — https://github.com/NPLinker/nplinker
- **GNPS** (Source of molecular networking archives containing spectra.mgf files and workflow metadata for GNPS1 and GNPS2) — https://gnps.ucsd.edu

## Examples

```
from nplinker import load_data; spectra = load_data(gnps_dir='./gnps', gnps_version='METABOLOMICS-SNETS-V2')
```

## Evaluation signals

- All Spectrum objects have non-null precursor m/z and fragment peak lists with plausible m/z values (typically 50–2000 m/z range).
- Spectrum identifiers match entries in molecular_families.tsv and annotations.tsv files with no orphaned or missing cross-references.
- No spectra have duplicate identifiers and all required metadata fields (scan number, retention time if available) are populated.
- Retention time values (if present) are numeric and fall within the experimental acquisition window (typically 0–60+ minutes).
- Peak intensity values are non-negative and in a consistent scale (e.g., raw counts or normalized 0–100 or 0–1 range).

## Limitations

- MGF parser assumes GNPS-compliant formatting; non-standard peak list delimiters or metadata fields may cause parse failures.
- Spectrum loading does not perform spectral cleaning, normalization, or denoising — input MGF quality depends on upstream GNPS processing.
- Cross-reference validation only checks existence of identifiers; semantic correctness (e.g., whether spectrum mass matches annotated compound mass) is not verified at load time.
- Large GNPS archives (>100k spectra) may require substantial memory; batch or streaming loading strategies are not documented in provided context.

## Evidence

- [other] Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects.: "Load spectral data using GNPSSpectrumLoader with the spectra.mgf file to produce structured Spectrum objects."
- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "specifying the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)."
