---
name: spectral-file-format-conversion
description: Use when when you have a GNPS molecular networking job archive (downloaded as a .zip or compressed archive) and need to prepare metabolomics spectra and molecular family data for NPLinker integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - nplinker
  - Python
  - GNPSDownloader
  - GNPSExtractor
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-file-format-conversion

## Summary

Extract and standardize spectral data from GNPS molecular networking job archives into NPLinker-compatible file formats (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv/csv). This skill bridges heterogeneous GNPS workflow outputs (GNPS1 vs. GNPS2, METABOLOMICS-SNETS vs. FEATURE-BASED-MOLECULAR-NETWORKING) into a unified input schema for downstream metabolomics data integration.

## When to use

When you have a GNPS molecular networking job archive (downloaded as a .zip or compressed archive) and need to prepare metabolomics spectra and molecular family data for NPLinker integration. Specifically: you have a GNPS task ID, access to the GNPS download URL, and you need to decompose the archive into the four standard NPLinker files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) to feed into npl.load_data().

## When NOT to use

- Input is not from GNPS (e.g., spectra already in a non-GNPS format or from a different molecular networking platform).
- The four required output files already exist in the correct NPLinker format and naming scheme in the target directory.
- The GNPS job failed or the archive is corrupted and does not contain valid spectra.mgf or molecular_families data.

## Inputs

- GNPS task ID (string identifier for a GNPS molecular networking job)
- GNPS job archive (compressed .zip or .tar.gz file downloaded from GNPS)

## Outputs

- spectra.mgf (MS/MS spectral data in MGF format)
- molecular_families.tsv (molecular networking clusters/groups)
- annotations.tsv (metabolite annotations and spectral assignments)
- file_mappings.tsv or file_mappings.csv (link between spectra and samples)

## How to apply

First, initialize a GNPSDownloader with the GNPS task ID and a local downloads directory path, then call its download() method to fetch the job archive and retrieve its file path. Second, initialize a GNPSExtractor with the downloaded archive path and a target gnps directory path; the extractor identifies the GNPS workflow type (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1, or classical_networking_workflow, feature_based_molecular_networking_workflow for GNPS2) and extracts the relevant data files. Third, rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv). Finally, verify that all four required files are present, accessible, and correctly named in the gnps directory; this ensures downstream data loading will succeed.

## Related tools

- **GNPSDownloader** (Fetches GNPS molecular networking job archive from GNPS server and returns local file path) — https://github.com/NPLinker/nplinker
- **GNPSExtractor** (Decompresses archive and identifies GNPS workflow type to extract constituent spectra and molecular family files) — https://github.com/NPLinker/nplinker
- **nplinker** (Python framework integrating the download, extraction, and standardization workflow for GNPS data into metabolomics-genomics data mining) — https://github.com/NPLinker/nplinker

## Examples

```
from nplinker.gnps import GNPSDownloader, GNPSExtractor; downloader = GNPSDownloader(task_id='task_001', downloads_dir='./downloads'); archive_path = downloader.download(); extractor = GNPSExtractor(archive_path, gnps_dir='./gnps'); extractor.extract()
```

## Evaluation signals

- All four required files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) are present and readable in the gnps directory.
- spectra.mgf contains valid MS/MS spectrum records with precursor m/z and fragment ion data in MGF format.
- molecular_families.tsv contains cluster IDs and spectra membership, with structure consistent with GNPS output.
- file_mappings.tsv or file_mappings.csv correctly links spectrum identifiers to sample/file names.
- npl.load_data() successfully ingests the four files without schema or format errors.

## Limitations

- The skill requires network connectivity to download from GNPS servers (GNPS1 at https://gnps.ucsd.edu or GNPS2 at https://gnps2.org); offline or restricted access will fail.
- Workflow type detection relies on identifying expected file structures within the archive; non-standard or malformed archives may not decompose correctly.
- The skill assumes the GNPS job completed successfully; incomplete or failed GNPS runs will produce incomplete or missing output files.
- File naming and directory structure are rigid; deviations from the four standard file names will cause downstream npl.load_data() to fail.

## Evidence

- [other] GNPSDownloader fetches a GNPS molecular networking job archive and returns its file path: "Initialize a GNPSDownloader with the GNPS task ID and a downloads directory path, then call the download() method to fetch the job archive and retrieve its local file path."
- [other] GNPSExtractor decomposes archive based on workflow type: "Initialize a GNPSExtractor with the downloaded archive path and the target gnps directory path, then call the extraction method to decompress the archive and identify the relevant data files based on"
- [other] Files must be renamed to standard NPLinker names: "Rename and move the extracted files to the standard NPLinker names (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or file_mappings.csv) in the gnps directory."
- [other] Verification step ensures all files present: "Verify that all four required files are present and accessible in the gnps directory with correct naming and format."
- [readme] NPLinker integrates genomics and metabolomics data: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
