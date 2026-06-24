---
name: command-line-tool-execution
description: Use when you have tandem MS/MS spectrum data in standard peak file formats
  (mzML, mzXML, or MGF) and need to cluster spectra based on precursor mass and fragment
  ion similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0091
  tools:
  - falcon
  - falcon-ms
  - spectrum-utils
  - LipoCLEAN
  - MS-DIAL
  - Rust
  - cargo
  - Parquet
  - ZIP
  - pyarrow
  - arrow
  - Galaxy Genomics Framework
  - SECIMTools suite
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
- doi: 10.1021/acs.analchem.4c04040
  title: ''
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
- doi: 10.1186/s12859-018-2134-1
  title: ''
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
- LipoCLEAN is a command line tool
- can be run in a standalone mode or via Galaxy Genomics Framework
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  - build: coll_cyproduct_cq
    doi: 10.1021/acs.jcim.1c00144
    title: CyProduct
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  - build: coll_lipoclean
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  - build: coll_mzpeak_cq
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  - build: coll_secimtools_cq
    doi: 10.1186/s12859-018-2134-1
    title: SECIMTools
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  - 10.1021/acs.analchem.4c04040
  - 10.1021/acs.jproteome.5c00435
  - 10.1186/s12859-018-2134-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# command-line-tool-execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute a bioinformatics command-line tool with specified parameters on input data files to produce analysis output. This skill involves installing the tool, configuring runtime parameters, invoking the command with appropriate file paths and tolerances, and verifying successful execution.

## When to use

You have tandem MS/MS spectrum data in standard peak file formats (mzML, mzXML, or MGF) and need to cluster spectra based on precursor mass and fragment ion similarity. Use this skill when you want to apply falcon's fast nearest-neighbor clustering to datasets containing millions of spectra, particularly in bottom-up proteomics workflows.

## When NOT to use

- Input spectra are already pre-clustered or a clustering result already exists — use this skill only on raw, unclustered peak files.
- Data is from top-down proteomics or metabolomics without adjustment of min_peaks, min_mz_range, min_mz, and max_mz settings — default preprocessing is tuned for bottom-up proteomics.
- Running on Windows — falcon is available only on Linux and OSX platforms.

## Inputs

- Peak files in mzML, mzXML, or MGF format containing tandem MS/MS spectra
- Python 3.8+ environment with pip
- Command-line parameters specifying precursor tolerance, fragment tolerance, clustering threshold (eps), and preprocessing options

## Outputs

- Comma-separated file (.csv) with cluster assignments (one MS/MS spectrum per row with corresponding cluster label)
- Optional MGF file containing representative spectra for each cluster

## How to apply

Install falcon-ms and spectrum-utils==0.3.5 via pip in a Python 3.8+ environment on Linux or OSX. Prepare input peak files in mzML, mzXML, or MGF format. Invoke the falcon command-line tool with the input directory/files and configure key parameters: precursor_tol (typically 20 ppm for high-resolution data), fragment_tol (typically 0.05 Da), and eps (0.05–0.15 for pure clustering, up to 0.30 for aggressive clustering). Adjust spectrum preprocessing settings (min_peaks, min_mz_range, min_mz, max_mz, scaling) based on your data type (default settings suit bottom-up proteomics; reduce thresholds for metabolomics). The tool will output cluster assignments to a CSV file (one spectrum per row with cluster label) and optionally export cluster representative spectra to MGF format.

## Related tools

- **falcon-ms** (Primary spectrum clustering tool; performs feature hashing, nearest neighbor indexing, and density-based clustering on tandem MS/MS spectra) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Dependency for spectrum I/O and preprocessing; version 0.3.5 required)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Tool executes without errors and completes without hanging or exceptions on the input peak files.
- Output CSV file is non-empty and contains one row per input spectrum with a numeric or categorical cluster label in the final column.
- Output CSV column structure matches expected format: one spectrum identifier per row with cluster assignment.
- Representative spectra MGF file (if exported) is valid and contains valid MS/MS spectrum records with peaklists.
- Cluster assignments are reproducible when the same command is re-run with identical parameters and input files.

## Limitations

- The eps (maximum cosine distance) parameter is sensitive to spectral preprocessing choices and data characteristics; ideal values depend on your spectrum preprocessing configuration and must be tuned empirically (0.05–0.30 range suggested, with 0.05–0.15 for pure results).
- Default preprocessing settings (min_peaks=5, min_mz_range=250, min_mz=101, max_mz=500) are optimized for bottom-up proteomics; metabolomics and top-down data require manual adjustment of these thresholds.
- Precursor mass tolerance and fragment mass tolerance must be specified correctly for your instrument and data acquisition method; mismatched tolerances will degrade clustering quality.
- Output is a sparse pairwise distance matrix computed via nearest neighbor indexing; the accuracy depends on the n_probe, n_neighbors, and low_dim parameters (defaults are sensible but can be tuned by advanced users for speed–accuracy trade-offs).

## Evidence

- [readme] falcon requires Python 3.8+ and is available on the Linux and OSX platforms.: "falcon requires Python 3.8+ and is available on the Linux and OSX platforms."
- [readme] pip install falcon-ms spectrum-utils==0.3.5: "pip install falcon-ms spectrum-utils==0.3.5"
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line.: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line."
- [readme] precursor_tol: The precursor mass tolerance and unit (in ppm or Dalton) to compare spectra to each other. fragment_tol: The fragment mass tolerance (in Dalton) used during spectrum comparison.: "precursor_tol: The precursor mass tolerance and unit (in ppm or Dalton) to compare spectra to each other. fragment_tol: The fragment mass tolerance (in Dalton) used during spectrum comparison."
- [readme] eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used.: "eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more"
- [readme] The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly.: "The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly."
- [readme] falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10: "falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10"
