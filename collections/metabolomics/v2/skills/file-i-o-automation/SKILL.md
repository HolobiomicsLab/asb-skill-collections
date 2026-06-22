---
name: file-i-o-automation
description: Use when you have MZmine-exported LC-MS/MS data (MGF spectra and CSV metadata files) in both positive and negative ionization modes and need to execute the full MolNotator pipeline from duplicate filtering through dereplication and network generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MolNotator
  - PyYAML
  - Cytoscape
derived_from:
- doi: 10.1101/2021.12.21.473622v1
  title: MolNotator
evidence_spans:
- from MolNotator.duplicate_filter import duplicate_filter
- from MolNotator.sample_slicer import sample_slicer
- import yaml
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnotator_cq
    doi: 10.1101/2021.12.21.473622v1
    title: MolNotator
  dedup_kept_from: coll_molnotator_cq
schema_version: 0.2.0
---

# file-i-o-automation

## Summary

Automate orchestration of multi-step LC-MS/MS processing pipelines by loading parameters from a YAML configuration file and sequentially invoking MolNotator modules (duplicate filtering, sample slicing, fragment annotation, adduct annotation, mode merging, dereplication, and network generation) on paired positive and negative ionization mode MGF and CSV files. This skill chains together the entire MolNotator workflow to transform raw MZmine outputs into annotated molecular networks without manual intervention between steps.

## When to use

Apply this skill when you have MZmine-exported LC-MS/MS data (MGF spectra and CSV metadata files) in both positive and negative ionization modes and need to execute the full MolNotator pipeline from duplicate filtering through dereplication and network generation. Use when the analysis goal is to identify actual molecules rather than individual ions and when you want to avoid repeated manual invocation of each processing stage.

## When NOT to use

- Input data are already processed into individual sample files (sample_slicer is redundant if per-sample MGF files already exist)
- You only have a single ionization mode and do not need mode_merger or cross-mode dereplication
- Reference database files are unavailable or you do not intend to perform dereplication against known compounds

## Inputs

- YAML configuration file (params.yaml) containing folder names, processing parameters, and database specifications
- MGF spectrum files from MZmine (one each for positive and negative ionization modes)
- CSV metadata files from MZmine corresponding to each MGF (positive and negative modes)
- Reference database files (MGF or TSV format) for dereplication
- Adduct annotation tables (TSV format, separate primary and secondary tables for each ionization mode)
- Fragment loss annotation table (fragnotator_table.tsv, two-column TSV with loss name and mass difference)

## Outputs

- Deduplicated MGF and CSV files for each ionization mode
- Per-sample sliced MGF files (one file per sample in each ionization mode)
- Node and edge CSV tables after each processing step (duplicate filtering, sample slicing, annotation stages, dereplication, cosine clustering)
- Unified molecular network (CSV node and edge tables) combining positive and negative ionization modes
- Simplified network variants (neutral nodes only, neutrals with adducts)

## How to apply

Create a project directory structure with subdirectories for `input_files` (MGF and CSV pairs for POS and NEG modes), `databases` (reference spectra in MGF or TSV format), and `params` (YAML configuration files and adduct/fragment annotation tables). Load the main `params.yaml` file using PyYAML into a dictionary. Sequentially call MolNotator functions in order: duplicate_filter, sample_slicer, fragnotator, adnotator (for each ion mode), mode_merger, and finally dereplicator and cosiner, passing the params dictionary and ion_mode ('NEG' or 'POS') to each function. Set the working directory to the project root so that relative paths in the YAML resolve correctly. After each step, CSV node and edge tables are automatically exported and can be visualized in Cytoscape. The workflow respects the ion mode designation to maintain separate processing pipelines until mode_merger unifies the results.

## Related tools

- **MolNotator** (Core Python package providing all processing modules (duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, dereplicator, cosiner, molnet) invoked in sequence) — https://github.com/ZzakB/MolNotator
- **PyYAML** (YAML parser used to load and deserialize the params.yaml configuration file into a Python dictionary for pipeline parameterization)
- **Cytoscape** (Optional downstream tool for visualization of node and edge CSV tables as molecular networks after each pipeline step) — https://cytoscape.org/

## Examples

```
import os
import yaml
from MolNotator.duplicate_filter import duplicate_filter
from MolNotator.sample_slicer import sample_slicer
from MolNotator.mode_merger import mode_merger

os.chdir('set/path/')
with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)

duplicate_filter(params=params, ion_mode="NEG")
sample_slicer(params=params, ion_mode="NEG")
mode_merger(params=params)
```

## Evaluation signals

- All intermediate CSV outputs (node and edge tables) are created in the working directory after each step without errors or missing files
- Sample slicing produces one MGF file per unique sample identifier found in the metadata, with no spectrum records lost or duplicated across sample files
- Final molecular network contains predicted neutral molecules as nodes, with edges representing adducts and in-source fragments annotated with mass differences matching the fragnotator table within specified tolerance
- Mode-merged network combines nodes from both positive and negative ionization modes with correct adduct charge signs (−1 for NEG, +1 for POS) and no mode conflicts
- Dereplicator output includes matches between experimental nodes and database entries with cosine similarity scores and mass accuracy checks consistent with params.yaml thresholds

## Limitations

- Multiple charge adducts are not supported; only single-charge ions should be processed
- Computing time can become prohibitive if all adducts are retained in the primary adduct table; the README recommends moving less abundant species to secondary tables
- The workflow assumes well-formed MZmine CSV and MGF pairs; mismatched or corrupted files will cause failures mid-pipeline
- Retain time and adduct filters for dereplication are optional and must be explicitly configured in the YAML; default parameters may not suit all experimental conditions

## Evidence

- [readme] MolNotator is a Python package that predicts the actual molecules present in LC-MS/MS data.: "MolNotator is a Python package that predicts the actual molecules present in LC-MS/MS data. The final data is represented in the form of actual molecular networks, representing the predicted"
- [readme] The workflow relies on loading a YAML parameter file and calling MolNotator functions sequentially with ion_mode designation.: "with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)

# Duplicate filtering on MZmine's MGF and CSV files (NEG):
duplicate_filter(params = params,"
- [readme] MolNotator expects a specific project structure with input_files, databases, and params subdirectories.: "MolNotator works within a user-defined project folder with a specific file structure... working_directory
|   input.py
|
|___databases
|   |   211005_MIX_LDB.mgf
|   |   211018_COLOTUS_DB.tsv
|"
- [readme] CSV node and edge tables are exported after most pipeline steps for downstream visualization.: "After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables."
- [results] Sample slicing partitions an MGF file into per-sample subsets as part of the workflow.: "The sample_slicer step accepts parameters and an ion mode designation (NEG) to slice a negative-mode MGF file into per-sample subsets as part of the MolNotator processing workflow."
- [readme] Mode merger combines positive and negative ionization mode results.: "# Use Moder Merger to merge negative and positive mode data :
mode_merger(params = params)"
- [readme] Multiple charge adducts are not supported in the current implementation.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
