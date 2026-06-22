---
name: strain-spectrum-mapping-linkage
description: Use when when you have downloaded and extracted a GNPS archive (from GNPS1 or GNPS2 workflows) and need to establish which spectral records (from spectra.mgf) were generated from which bacterial strains or samples. The file_mappings.tsv or file_mappings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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

# strain-spectrum-mapping-linkage

## Summary

Load and validate strain-to-spectrum file mappings from GNPS archive data to establish the linkage between microbial strains and their corresponding mass spectrometry records. This is a prerequisite step for integrating genomics and metabolomics data in natural product discovery workflows.

## When to use

When you have downloaded and extracted a GNPS archive (from GNPS1 or GNPS2 workflows) and need to establish which spectral records (from spectra.mgf) were generated from which bacterial strains or samples. The file_mappings.tsv or file_mappings.csv file in the archive provides this critical linkage and must be loaded before computing strain-to-metabolite links.

## When NOT to use

- GNPS data has not yet been downloaded and extracted to a directory
- The GNPS workflow version is unknown or not specified (cannot determine appropriate schema)
- file_mappings.tsv or file_mappings.csv is missing or corrupted in the archive

## Inputs

- GNPS archive (downloaded and extracted)
- file_mappings.tsv or file_mappings.csv from GNPS output
- Previously loaded Spectrum objects (for cross-reference validation)

## Outputs

- Strain-to-spectrum mapping records
- Validated file mapping structure with no missing required fields

## How to apply

Initialize a GNPSFormat object from the extracted GNPS archive by calling gnps_format_from_archive() or gnps_format_from_file_mapping(), specifying the correct GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, or FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2). Then use GNPSFileMappingLoader with the file_mappings.tsv or file_mappings.csv file to produce strain-to-spectrum mapping records. Validate that all loaded records contain no missing required fields and that cross-references are consistent between the mapping records and the previously loaded Spectrum objects from spectra.mgf.

## Related tools

- **nplinker** (Provides GNPSFileMappingLoader class and helper functions (gnps_format_from_archive, gnps_format_from_file_mapping) to load and validate strain-spectrum mappings from GNPS archives) — https://github.com/NPLinker/nplinker
- **GNPS** (Generates the file_mappings.tsv/csv output file that maps sample/strain identifiers to spectral records) — https://gnps.ucsd.edu, https://gnps2.org
- **Python** (Language in which nplinker and the GNPSFileMappingLoader are implemented (requires ≥3.11))

## Examples

```
from nplinker import GNPSFormat, GNPSFileMappingLoader; gnps_fmt = GNPSFormat.gnps_format_from_archive('path/to/extracted/gnps', workflow_version='METABOLOMICS-SNETS-V2'); loader = GNPSFileMappingLoader(gnps_fmt); mappings = loader.load('path/to/file_mappings.tsv')
```

## Evaluation signals

- All records loaded from file_mappings.tsv/csv have no missing required fields (strain identifier, spectrum identifier, or equivalent)
- Cross-references between mapping records and Spectrum objects are consistent (every mapped spectrum ID corresponds to a loaded Spectrum)
- No duplicate strain-spectrum pairs exist in the loaded mapping
- Validation step completes without errors or warnings when called on the loaded mapping records
- The number of loaded mapping records matches the expected number of strain-spectrum pairs in the GNPS archive

## Limitations

- File format (TSV vs. CSV) must match the GNPS workflow version used; incorrect format selection will cause parsing failures
- Validation depends on prior successful loading of spectra.mgf via GNPSSpectrumLoader; incomplete or corrupted spectral data will cause cross-reference validation to fail
- The mapping file structure differs between GNPS1 and GNPS2 workflows; GNPSFormat object must be initialized with the correct workflow version to parse correctly

## Evidence

- [other] Load file mappings using GNPSFileMappingLoader with file_mappings.tsv (or .csv) to produce strain-to-spectrum mapping records.: "Load file mappings using GNPSFileMappingLoader with file_mappings.tsv (or .csv) to produce strain-to-spectrum mapping records"
- [other] Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version: "Initialize GNPSFormat object from an extracted or downloaded GNPS archive using gnps_format_from_archive() or gnps_format_from_file_mapping() helper functions, specifying the GNPS workflow version"
- [other] Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations).: "Validate all loaded records for completeness (no missing required fields, consistent cross-references between spectra and families and annotations)"
- [other] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
