---
name: metabolomics-scan-metadata-linking
description: Use when after running a ViMMS Environment simulation with save_eval flag enabled, when you need to preserve the link between each simulated MS/MS scan in the output mzML file and its source chemical definition, fragmentation parameters, and evaluation metrics for later analysis, comparison, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ViMMS
  - Python pickle module
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive and modular framework for the simulation of fragmentation strategies'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms_cq
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.03990
  all_source_dois:
  - 10.21105/joss.03990
  - 10.1021/acs.analchem.0c03895
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-scan-metadata-linking

## Summary

Persist evaluation metadata and chemical definitions alongside simulated LC-MS/MS scans in mzML output by serializing in-memory EvaluationData objects to pickle files. This enables downstream traceability between generated MS/MS fragmentation events and their source chemical compounds for comparative acquisition strategy evaluation.

## When to use

After running a ViMMS Environment simulation with save_eval flag enabled, when you need to preserve the link between each simulated MS/MS scan in the output mzML file and its source chemical definition, fragmentation parameters, and evaluation metrics for later analysis, comparison, or validation of acquisition strategies.

## When NOT to use

- If evaluation data collection was not enabled during the simulation (save_eval=False); re-run the simulation with save_eval=True.
- If you only need the mzML scans without any metadata linking to source chemicals or fragmentation events; standard mzML export alone is sufficient.
- If the simulated environment has not completed (env.run() has not finished); serialization requires a completed run with populated EvaluationData.

## Inputs

- ViMMS Environment object (after env.run() with save_eval=True)
- EvaluationData object (in-memory, containing chemicals, scans, fragmentation events)
- Simulated LC-MS/MS acquisition run with controller-generated scans

## Outputs

- Pickle file (.p extension) containing serialized EvaluationData object
- mzML file containing simulated MS/MS scans with scan-level metadata
- Bidirectional linkage: scan IDs in mzML reference chemical definitions in pickle

## How to apply

Enable evaluation data collection by setting save_eval=True when creating and running the ViMMS Environment. After env.run() completes, the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) must be serialized to a pickle file using Python's pickle module via the save_obj function. Write the corresponding mzML scan output to a companion file using Environment.write_mzML(). Verify both files exist and are accessible—the pickle file provides the chemical and fragmentation metadata while the mzML file contains the actual scan data. The linkage between files is maintained through scan identifiers that reference back to source chemicals and their properties.

## Related tools

- **ViMMS** (Simulates fragmentation strategies and generates EvaluationData; provides Environment class, save_obj function, and write_mzML() method for scan serialization) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Serializes the in-memory EvaluationData object to a persistent binary file for later retrieval and linkage to mzML scans)

## Examples

```
import pickle; from vimms.ChemicalSampler import UniformMZFormulaSampler; from vimms.Environment import Environment; env = Environment(ms_level=2, save_eval=True); env.run(chemicals_file='chemicals.p'); pickle.dump(env.evaluation_data, open('evaluation_data.p', 'wb')); env.write_mzML('output.mzML')
```

## Evaluation signals

- Both pickle and mzML files are created and are non-empty after the workflow completes
- Pickle file deserializes without error and contains a valid EvaluationData object with populated chemicals, scans, and fragmentation metadata
- Scan IDs or indices in the mzML precursor/fragment records are traceable to chemical entries in the EvaluationData pickle
- Chemical properties (mass, retention time, fragmentation events) from pickle match the scan metadata (m/z, RT, intensity patterns) in mzML for the same chemical
- Files are written to the expected output directory and are accessible for downstream evaluation workflows (e.g., comparison against spectral libraries)

## Limitations

- Pickle format is Python-specific; requires Python environment to deserialize, limiting interoperability with non-Python analysis pipelines.
- Large simulations may generate very large pickle files, consuming significant disk space; no built-in compression or selective serialization offered in the documented workflow.
- The linkage between pickle and mzML relies on scan ID consistency; any mismatch or reordering during export may break traceability.
- Evaluation data collection (save_eval=True) introduces runtime and memory overhead during simulation; not suitable for resource-constrained prototyping runs.

## Evidence

- [other] ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions for downstream analysis.: "ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions"
- [other] Run an Environment simulation with save_eval flag enabled to trigger evaluation data collection.: "Run an Environment simulation with save_eval flag enabled to trigger evaluation data collection"
- [other] After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module.: "serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module"
- [other] Write the mzML scan output to a companion file using Environment.write_mzML(). Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations.: "Write the mzML scan output to a companion file using Environment.write_mzML(). Verify both the pickle and mzML files exist and are accessible"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data"
