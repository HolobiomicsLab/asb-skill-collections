---
name: python-package-integration
description: Use when when you have LC-MS/MS data in MZmine-generated MGF and CSV files (for positive and/or negative ionization modes) and need to apply a sequence of deduplication, annotation, and dereplication steps defined in a MolNotator YAML configuration file to predict actual molecules and build.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - MolNotator
  - PyYAML
  - Cytoscape
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2021.12.21.473622v1
  title: MolNotator
evidence_spans:
- MolNotator is a Python package
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

# python-package-integration

## Summary

Integrate a specialized Python package (MolNotator) into a multi-step LC-MS/MS data processing pipeline by loading configuration from YAML, instantiating the package functions with parsed parameters, and executing them in sequence across ionization modes. This skill ensures reproducible, parameterized execution of modular metabolomics workflows.

## When to use

When you have LC-MS/MS data in MZmine-generated MGF and CSV files (for positive and/or negative ionization modes) and need to apply a sequence of deduplication, annotation, and dereplication steps defined in a MolNotator YAML configuration file to predict actual molecules and build molecular networks.

## When NOT to use

- Input data is not in MZmine MGF/CSV format or has already been processed by MolNotator (risk of re-filtering or corrupting intermediate results).
- YAML configuration file is missing, malformed, or does not reference valid adduct tables and database files in the expected directory structure.
- User requires multi-charge adduct processing; MolNotator does not implement multiple charge states.

## Inputs

- MZmine MGF file (negative ionization mode)
- MZmine CSV file (negative ionization mode)
- MZmine MGF file (positive ionization mode)
- MZmine CSV file (positive ionization mode)
- YAML parameter file (params.yaml)
- Secondary YAML database parameter files (optional, for dereplication)

## Outputs

- Deduplicated MGF and CSV files (after duplicate_filter)
- Sample-sliced MGF files (after sample_slicer)
- Annotated node and edge CSV tables (after fragnotator, adnotator, mode_merger, dereplicator)
- Final molecular network node and edge tables (after molnet)
- Cosine similarity clustering results (after cosiner)

## How to apply

Load the YAML parameter file using PyYAML to retrieve global and step-specific configuration (duplicate-filter settings, adduct tables, database file paths, output directories). Import the MolNotator functions (duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, dereplicator, cosiner, molnet) and execute them sequentially, passing the parsed params dictionary and the ion_mode argument (NEG or POS) to each function. Begin with duplicate_filter on both ionization modes to remove redundant features from the input MGF and CSV files, then proceed through sample slicing, fragment annotation, adduct annotation, mode merging, and optional dereplication against spectral/mass databases. The rationale is that MolNotator's modular design allows each step to output intermediate CSV edge and node tables suitable for visualization in Cytoscape, and the YAML-driven parameterization ensures that the same pipeline can be reused across different datasets and experiments without code modification.

## Related tools

- **MolNotator** (Python package providing duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, dereplicator, cosiner, and molnet functions for LC-MS/MS data processing and molecular network prediction) — https://github.com/ZzakB/MolNotator
- **PyYAML** (Parses YAML parameter and configuration files to retrieve pipeline settings, database paths, and adduct/fragment tables)
- **Cytoscape** (Visualization software for importing node and edge CSV tables at each intermediate step to inspect molecular networks) — https://cytoscape.org/

## Examples

```
import yaml
from MolNotator.duplicate_filter import duplicate_filter
with open('./params/params.yaml') as info:
    params = yaml.load(info, Loader=yaml.FullLoader)
duplicate_filter(params=params, ion_mode='NEG')
duplicate_filter(params=params, ion_mode='POS')
```

## Evaluation signals

- YAML file is successfully loaded with yaml.FullLoader and params dictionary contains all required keys (databases, input_files, params folder references, db_params list).
- duplicate_filter produces output MGF and CSV files with fewer features than input files (deduplicated feature count is lower for both NEG and POS modes).
- Each MolNotator function executes without raised exceptions and produces intermediate CSV edge and node tables in the working directory.
- Final node and edge CSV tables can be imported into Cytoscape without schema errors and visualize as molecular networks with predicted molecules as nodes and ions as connected features.
- Directory structure remains intact (databases, input_files, params folders exist and contain expected file types) after pipeline completion; no existing output files caused early termination.

## Limitations

- MolNotator requires a specific project directory structure (working_directory containing input_files, databases, params subdirectories); deviations cause runtime errors.
- Multi-charge adduct processing is not implemented; only single-charge ions are supported; transferring common adducts (e.g. [M+H]+) from primary to secondary tables is necessary to avoid computing bottlenecks.
- The dereplicator step depends on user-provided spectral and exact mass database files (MGF, TSV, or CSV format); missing or malformed database files will cause dereplication to fail or produce incomplete results.
- YAML parameters must reference valid file paths and adduct table column names; typos in parameter names or missing adduct tables will cause failures during execution of specific functions.

## Evidence

- [readme] MolNotator is a Python package that predicts the actual molecules present in LC-MS/MS data. The final data is represented in the form of actual molecular networks, representing the predicted molecules as nodes amidst the ions they generated.: "MolNotator is a Python package that predicts the actual molecules present in LC-MS/MS data. The final data is represented in the form of actual molecular networks"
- [readme] MolNotator depends on a python input file to be runned. The example here under can be used as a template: [code showing imports and sequential function calls with params and ion_mode arguments]: "MolNotator depends on a python input file to be runned. The example here under can be used as a template"
- [readme] The params yaml file contains all parameters to be used in the project. Each parameter has a short description as a comment and we would suggest using the default values to begin with.: "The params yaml file contains all parameters to be used in the project. Each parameter has a short description as a comment"
- [readme] After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape by importing the two tables.: "After most steps, CSV files are exported including a node table and an edge table. Networks can thus be visualized after each step using softwares like Cytoscape"
- [results] The duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes.: "The duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes."
- [readme] with open('./params/params.yaml') as info: params = yaml.load(info, Loader=yaml.FullLoader): "with open("./params/params.yaml") as info: params = yaml.load(info, Loader=yaml.FullLoader)"
- [readme] Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
