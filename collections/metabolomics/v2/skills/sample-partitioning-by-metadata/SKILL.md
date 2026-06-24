---
name: sample-partitioning-by-metadata
description: Use when you have a merged MGF file (e.g., from MZmine output) containing
  MS/MS spectra from multiple biological or environmental samples, and you need to
  process each sample independently through annotation pipelines (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MolNotator
  - PyYAML
  - MZmine
  techniques:
  - LC-MS
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.12.21.473622v1
  all_source_dois:
  - 10.1101/2021.12.21.473622v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-partitioning-by-metadata

## Summary

Partition a mass spectrometry MGF file into per-sample subsets by extracting and grouping spectra according to sample identifier metadata. This skill is essential in multi-sample LC-MS/MS workflows to enable independent downstream annotation and molecular network construction for each sample.

## When to use

Apply this skill when you have a merged MGF file (e.g., from MZmine output) containing MS/MS spectra from multiple biological or environmental samples, and you need to process each sample independently through annotation pipelines (e.g., fragmentation matching, adduct assignment, dereplication) before merging results back together.

## When NOT to use

- Input is a single-sample MGF file or already contains spectra separated by sample — partitioning will produce redundant outputs.
- Sample metadata is missing or inconsistent in the MGF file — the function requires a reliably populated sample identifier field for each spectrum.
- The downstream workflow does not require per-sample processing (e.g., global network construction without sample-level resolution).

## Inputs

- MGF (Mascot Generic Format) file from MZmine containing MS/MS spectra with sample metadata
- YAML parameter configuration file (params.yaml) with input paths, output directory, and column mappings
- Ion mode designation string ('NEG' or 'POS')

## Outputs

- Per-sample MGF files written to the output directory, each containing only spectra from a single sample
- Partitioned spectral data indexed by sample identifier

## How to apply

Load the project configuration parameters from a YAML file (e.g., params.yaml), then invoke the sample_slicer function with the params dictionary and the ion_mode designation ('NEG' or 'POS' for negative or positive ionization mode). The function reads the input MGF file specified in params, extracts the sample identifier from each spectrum's metadata, groups spectra by that identifier, and writes each group to a separate output MGF file in the designated output directory. The YAML configuration must specify input file paths, output directory, and any relevant sample metadata fields to enable correct partitioning.

## Related tools

- **MolNotator** (Provides the sample_slicer function that partitions MGF files by sample metadata) — https://github.com/ZzakB/MolNotator
- **PyYAML** (Parses the YAML configuration file to load project parameters and file paths)
- **MZmine** (Upstream tool producing the merged MGF and CSV input files)

## Examples

```
import yaml
from MolNotator.sample_slicer import sample_slicer
with open('./params/params.yaml') as f:
    params = yaml.load(f, Loader=yaml.FullLoader)
sample_slicer(params=params, ion_mode='NEG')
```

## Evaluation signals

- Each output MGF file contains only spectra from a single sample (verify by checking sample metadata fields across all spectra in each file).
- The number of output files matches the number of unique sample identifiers in the input MGF file.
- The total number of spectra across all output files equals the number of spectra in the input file (no data loss or duplication).
- All output files are valid MGF format and can be parsed by downstream tools (fragnotator, adnotator).
- Output directory structure matches the specification in params.yaml with correct naming convention (e.g., {sample_id}_NEG.mgf or {sample_id}_POS.mgf).

## Limitations

- Requires that sample identifiers are present and consistently formatted in the MGF file metadata; missing or malformed identifiers will cause spectra to be dropped or assigned to incorrect partitions.
- Single-charge ions only; multiple charge adduct processing is not implemented in MolNotator.
- The skill does not validate that samples are biologically or experimentally meaningful — it performs purely syntactic partitioning based on the metadata field specified in params.yaml.

## Evidence

- [other] The sample_slicer step accepts parameters and an ion mode designation (NEG) to slice a negative-mode MGF file into per-sample subsets as part of the MolNotator processing workflow.: "sample_slicer function from MolNotator with params and ion_mode set to 'NEG' to slice the input MGF file by sample identifier"
- [readme] Writing output files requires invoking sample_slicer with configuration loaded from YAML.: "Write each sample's spectrum records to a separate output MGF file in the designated output directory."
- [readme] Configuration workflow documented in README.: "with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)

# Slicing the negative mode MGF file
sample_slicer(params = params,
           ion_mode = "NEG")"
- [readme] Ion mode is a required parameter.: "# Slicing the positive mode MGF file
sample_slicer(params = params,
           ion_mode = "POS")"
- [readme] Sample partitioning is a prerequisite step for independent sample processing.: "Global networks containing all samples are produced at each step, but they can be divided to contain only the data for each specific sample."
