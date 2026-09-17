---
name: metabolite-network-format-conversion
description: Use when after downloading GNPS molecular networking results (from GNPS1
  or GNPS2 workflows), use this skill to extract and standardize the compressed archive
  into named, canonicalized files (spectra.mgf, molecular_families.tsv, annotations.tsv,
  file_mappings.tsv/.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - nplinker
  - Python
  - GNPS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_2_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-network-format-conversion

## Summary

Convert GNPS molecular networking output files into a standardized internal format suitable for downstream computational analysis in NPLinker. This skill bridges GNPS workflow heterogeneity by detecting workflow version and remapping workflow-specific output files to a consistent schema.

## When to use

After downloading GNPS molecular networking results (from GNPS1 or GNPS2 workflows), use this skill to extract and standardize the compressed archive into named, canonicalized files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv/.csv) before passing the data to NPLinker's analysis pipeline. Trigger conditions: you have a GNPS task ID, a downloaded .zip archive from GNPS servers, and need access to spectra and molecular family data for integrated genomics-metabolomics analysis.

## When NOT to use

- If GNPS data has already been downloaded and extracted into the target gnps directory with correct file naming — re-extraction will be redundant and may overwrite existing work.
- If molecular networking input is available from sources other than GNPS (e.g., local spectral clustering results that do not conform to GNPS workflow output structure) — the GNPS-specific extraction logic will not apply.
- If the GNPS task ID is invalid or the GNPS servers are unreachable — download will fail; use cached or pre-downloaded archives instead.

## Inputs

- GNPS task ID (string identifier)
- Download directory path (local filesystem directory)
- Compressed GNPS archive file (.zip) from GNPS1 or GNPS2 servers

## Outputs

- spectra.mgf file (MGF spectrum format)
- molecular_families.tsv (tab-separated molecular family clusters)
- annotations.tsv (tab-separated spectral annotations)
- file_mappings.tsv or .csv (sample-to-spectrum file mappings)
- gnps directory (target output directory with standardized file layout)

## How to apply

Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers and obtain the archive file path. Next, instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify the GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, or FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2). The extractor then renames the workflow-specific output files according to the mapping table for the detected version. This two-step process ensures that regardless of GNPS workflow type, the extracted files follow a unified naming convention enabling consistent downstream access to spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings.tsv or .csv.

## Related tools

- **nplinker** (Orchestrates GNPS data retrieval and extraction via GNPSDownloader and GNPSExtractor classes; provides standardized file interface for downstream molecular networking analysis) — https://github.com/NPLinker/nplinker
- **GNPS** (Source platform providing molecular networking workflow results (GNPS1 at https://gnps.ucsd.edu and GNPS2 at https://gnps2.org) whose outputs are downloaded and converted) — https://gnps.ucsd.edu
- **Python** (Programming language used to instantiate GNPSDownloader and GNPSExtractor objects and invoke download() and extraction methods)

## Examples

```
from nplinker.gnps import GNPSDownloader, GNPSExtractor; dl = GNPSDownloader('task_id_12345', './download'); archive_path = dl.download(); ex = GNPSExtractor(archive_path, './gnps'); ex.extract()
```

## Evaluation signals

- Archive download completes without network errors and archive file path is returned by GNPSDownloader.download().
- Extraction creates the gnps output directory with all four required files present: spectra.mgf, molecular_families.tsv, annotations.tsv, and file_mappings.tsv or .csv.
- File naming matches the standardized convention (not workflow-specific names like 'spec.mgf' or 'network_pairs.tsv').
- GNPS workflow version is correctly detected and the mapping table for that version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1 or classical_networking_workflow, feature_based_molecular_networking_workflow for GNPS2) is applied.
- Extracted spectra.mgf is a valid MGF format file and molecular_families.tsv contains tab-separated cluster membership data suitable for npl.load_data() ingestion.

## Limitations

- The skill is specific to GNPS1 and GNPS2 workflows; other molecular networking platforms (e.g., MS-DIAL, local clustering pipelines) will not be recognized by the workflow version detection logic.
- Network connectivity to GNPS servers (gnps.ucsd.edu or gnps2.org) is required for the download step; offline or archived data must be pre-downloaded.
- If the GNPS workflow output structure changes in future GNPS versions, the mapping table and file detection logic may require updates to remain compatible.
- The extraction assumes all required files are present in the GNPS archive; corrupted or incomplete GNPS results will cause extraction to fail or produce incomplete outputs.

## Evidence

- [other] NPLinker uses a two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory, enabling access to molecular networking results for subsequent computational analysis.: "two-step process: Download GNPS data & get the path to the downloaded archive, then Extract GNPS data to `gnps` directory"
- [other] Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers and obtain the archive file path.: "Instantiate GNPSDownloader with a GNPS task ID and download directory path, then invoke the download() method to retrieve the compressed archive from GNPS servers"
- [other] Instantiate GNPSExtractor with the downloaded archive path and target gnps directory path, then invoke extraction to identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected GNPS workflow version (METABOLOMICS-SNETS, METABOLOMICS-SNETS-V2, FEATURE-BASED-MOLECULAR-NETWORKING for GNPS1; classical_networking_workflow or feature_based_molecular_networking_workflow for GNPS2).: "identify and rename the workflow-specific files (spectra.mgf, molecular_families.tsv, annotations.tsv, file_mappings.tsv or .csv) according to the mapping table for the detected GNPS workflow version"
- [readme] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
