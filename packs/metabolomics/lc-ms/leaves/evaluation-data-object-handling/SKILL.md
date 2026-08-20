---
name: evaluation-data-object-handling
description: Use when after completing an Environment simulation run with save_eval flag enabled, when you need to preserve the EvaluationData object containing scan provenance, chemical source definitions, and fragmentation events for later inspection, validation, or reanalysis without re-running the full.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ViMMS
  - Python pickle module
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Evaluation-Data Object Handling

## Summary

Serialize and persist ViMMS in-memory evaluation data (chemicals, generated scans, fragmentation events) alongside simulated mzML output using Python pickle files, enabling reproducible linkage between scan metadata and source chemical definitions for downstream analysis.

## When to use

After completing an Environment simulation run with save_eval flag enabled, when you need to preserve the EvaluationData object containing scan provenance, chemical source definitions, and fragmentation events for later inspection, validation, or reanalysis without re-running the full simulation.

## When NOT to use

- If save_eval flag was not set during Environment.run(), the EvaluationData object will be empty or unavailable; use only after re-running with save_eval=True.
- If you only need the mzML output for downstream spectral matching or chemical annotation without requiring source chemical provenance; mzML alone may be sufficient.
- If the output directory lacks write permissions or disk space is insufficient to store both pickle and mzML files; serialize only to a network or backup location first.

## Inputs

- ViMMS Environment object (post-simulation)
- in-memory EvaluationData object
- simulated scan collection
- chemical object definitions

## Outputs

- pickle file (serialized EvaluationData object)
- mzML file (MS scan data)
- paired artifact metadata for validation

## How to apply

Execute the ViMMS Environment.run() method with save_eval=True to trigger collection of evaluation metadata into an in-memory EvaluationData object. Upon completion, serialize this object to a pickle file using Python's pickle module (e.g., pickle.dump(eval_data, file)). Simultaneously, write the simulated mass spectrometry scan data to an mzML companion file using Environment.write_mzML(). Verify both files are created and accessible in the output directory, then validate that the pickle file can be deserialized and contains expected keys (chemicals, scan list, fragmentation tree) before proceeding to downstream evaluation operations. This dual-artifact approach ensures scan identifiers in the mzML remain traceable to their source chemical objects and acquisition parameters.

## Related tools

- **ViMMS** (Core simulation framework; provides Environment class, run() method with save_eval flag, write_mzML() method, and EvaluationData object structure for serialization.) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Serialization backend for persisting EvaluationData object to binary format for storage and later deserialization.)

## Examples

```
import pickle
from vimms.Controller import SimpleController
env = Environment(controller=SimpleController(), chem_list=chemicals)
env.run(save_eval=True)
with open('evaluation_data.pkl', 'wb') as f:
    pickle.dump(env.eval_data, f)
env.write_mzML('output.mzML')
```

## Evaluation signals

- Both output files (pickle and mzML) exist in the specified output directory and have non-zero file size.
- Pickle file can be successfully deserialized using pickle.load() without corruption or version mismatch errors.
- Deserialized EvaluationData object contains expected top-level keys: 'chemicals', 'scans', 'fragmentation_events' or equivalent structure.
- Scan identifiers and m/z values in the mzML file match scan metadata in the deserialized EvaluationData object (spot-check sample of scans).
- Chemical object IDs referenced in the EvaluationData match the chemical pool used to initialize the Environment simulation.

## Limitations

- Pickle format is Python-specific and not portable across Python versions or platforms with different endianness; consider version pinning or alternative serialization (e.g., JSON) for long-term archival.
- Large EvaluationData objects (many chemicals, long simulation duration) can produce multi-gigabyte pickle files; disk space must be pre-allocated and I/O performance may degrade.
- Pickle does not preserve all custom class attributes if ViMMS classes are refactored; serialized objects may fail to load after major framework updates.
- The mzML file may not fully capture all internal ViMMS simulation state (e.g., controller decision trees, gradient profiles); use EvaluationData pickle for complete reproducibility.

## Evidence

- [other] ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions for downstream analysis.: "ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions"
- [other] After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module.: "After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module."
- [other] Write the mzML scan output to a companion file using Environment.write_mzML().: "Write the mzML scan output to a companion file using Environment.write_mzML()."
- [other] Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations.: "Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations."
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
