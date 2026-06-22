---
name: spectrum-subset-extraction
description: Use when after duplicate filtering of MZmine-exported MGF and CSV files, when you have combined spectra from multiple samples in a single MGF and need to segregate them by sample identifier before fragment annotation or adduct assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MolNotator
  - PyYAML
  - MZmine
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-subset-extraction

## Summary

Partition a mass spectrometry MGF file into per-sample subsets to enable independent annotation and analysis of spectra grouped by sample identifier. This step facilitates downstream processing in untargeted LC-MS/MS metabolomics workflows where sample-level granularity is required.

## When to use

After duplicate filtering of MZmine-exported MGF and CSV files, when you have combined spectra from multiple samples in a single MGF and need to segregate them by sample identifier before fragment annotation or adduct assignment. Typically applied in both negative and positive ionization modes as part of the MolNotator pipeline.

## When NOT to use

- Input MGF file does not contain sample identifier metadata or identifiers are missing from spectrum headers
- Spectra have already been segregated by sample (sample_slicer is redundant)
- Analysis goal is global network construction across all samples without sample-level segregation

## Inputs

- params dictionary (loaded from YAML configuration file)
- Ion mode designation ('NEG' or 'POS')
- Input MGF file (duplicate-filtered, from MZmine output)

## Outputs

- Per-sample MGF files (one file per unique sample identifier)
- Output directory containing partitioned spectrum subsets

## How to apply

Load the params dictionary from the YAML configuration file using PyYAML. Call the sample_slicer function from MolNotator with the params object and ion_mode parameter set to either 'NEG' or 'POS' to specify ionization mode. The function reads the input MGF file path from params, extracts the sample identifier field from each spectrum record, and groups spectra by that identifier. Write each sample's spectrum records to a separate output MGF file in the designated output directory. The sample identifiers are typically populated by MZmine during initial data export.

## Related tools

- **MolNotator** (Provides sample_slicer function to partition MGF spectra by sample identifier) — https://github.com/ZzakB/MolNotator
- **PyYAML** (Loads YAML parameter configuration files into Python dictionaries)
- **MZmine** (Generates initial MGF and CSV files with sample metadata)

## Examples

```
from MolNotator.sample_slicer import sample_slicer; import yaml; params = yaml.load(open('./params/params.yaml'), Loader=yaml.FullLoader); sample_slicer(params=params, ion_mode='NEG')
```

## Evaluation signals

- Number of output MGF files equals the number of unique sample identifiers in input
- Sum of spectrum record counts across all per-sample MGF files equals the total count in the input MGF
- Each output MGF file contains only spectra belonging to one sample identifier
- Output MGF files are valid and parseable by downstream tools (fragnotator, adnotator)
- Output directory structure and file naming match the params-specified output path and sample naming conventions

## Limitations

- Requires sample identifier field to be present in MGF spectrum headers; missing or malformed identifiers may result in spectra being discarded or grouped incorrectly
- Ion mode parameter must match the actual polarity of the input MGF (mismatch does not prevent execution but produces incorrect results)
- Single-charge ions only; multiple charge adduct processing is not implemented
- Output file naming and organization depend on correct YAML parameter configuration

## Evidence

- [other] The sample_slicer step accepts parameters and an ion mode designation (NEG) to slice a negative-mode MGF file into per-sample subsets as part of the MolNotator processing workflow.: "sample_slicer step accepts parameters and an ion mode designation (NEG) to slice a negative-mode MGF file into per-sample subsets"
- [other] Load the params dictionary from the YAML configuration file using PyYAML. Call the sample_slicer function from MolNotator with params and ion_mode set to 'NEG' to slice the input MGF file by sample identifier. Write each sample's spectrum records to a separate output MGF file in the designated output directory.: "Load the params dictionary from the YAML configuration file using PyYAML. Call the sample_slicer function from MolNotator with params and ion_mode set to 'NEG' to slice the input MGF file by sample"
- [readme] sample_slicer(params = params, ion_mode = "NEG") ... sample_slicer(params = params, ion_mode = "POS"): "sample_slicer(params = params, ion_mode = "NEG") # Slicing the negative mode MGF file ... sample_slicer(params = params, ion_mode = "POS") # Slicing the positive mode MGF file"
- [readme] Global networks containing all samples are produced at each step, but they can be divided to contain only the data for each specific sample.: "Global networks containing all samples are produced at each step, but they can be divided to contain only the data for each specific sample"
- [readme] Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions"
