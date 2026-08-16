---
name: simulation-output-serialization
description: Use when after a ViMMS Environment.run() simulation completes with save_eval
  flag enabled, you have collected EvaluationData containing chemical compounds, their
  generated scans, and fragmentation events in memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3949
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_3375
  tools:
  - ViMMS
  - Python pickle module
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible
  and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive
  and modular framework for the simulation of fragmentation strategies'
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

# Serialize Simulated LC-MS/MS Output to Persistent Artifacts

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Persist the in-memory evaluation data and chemical definitions generated during a ViMMS Environment simulation run into companion pickle and mzML files, enabling linkage between simulated MS/MS scans and their source metabolite definitions for downstream evaluation and reuse.

## When to use

After a ViMMS Environment.run() simulation completes with save_eval flag enabled, you have collected EvaluationData containing chemical compounds, their generated scans, and fragmentation events in memory. Serialize this to disk when you need to: (1) preserve the mapping between mzML scan output and source chemical definitions for later analysis; (2) archive the full simulation state (chemicals, isotope patterns, fragmentation rules) alongside the output spectra; or (3) enable retrospective evaluation of acquisition strategies against the same ground truth metabolites.

## When NOT to use

- The Environment simulation was run without save_eval=True flag — the EvaluationData object will not be populated with evaluation metrics and chemical records.
- You only need the mzML output for visualization or external tool input and do not require the ground-truth chemical definitions or fragmentation metadata.
- The simulated run is exploratory and outputs will not be reused; serialization adds I/O overhead without downstream value.

## Inputs

- Environment object (post-simulation, after env.run() completes)
- EvaluationData object (in-memory, containing Compound list, generated scans, fragmentation events)
- Output directory path (writable filesystem location)

## Outputs

- Pickle file (.pickle) containing serialized EvaluationData and chemical definitions
- mzML file (.mzML) containing scan-level mass spectrometry output
- Linked artifact pair (both files with matching root filename)

## How to apply

After env.run() completes, retrieve the in-memory EvaluationData object from the Environment instance (containing the list of Compound objects, generated scans, and fragmentation event logs). Use Python's pickle module to serialize this object to a .pickle file, preserving the full object graph including chemical metadata and generated MS/MS fragmentation events. In parallel, call Environment.write_mzML() to export the scan-level output to an mzML file. Both files should be written to the same output directory with linked filenames (e.g., 'simulation_run_001.pickle' and 'simulation_run_001.mzML'). Verify both files exist, are non-empty, and can be successfully deserialized/reopened to confirm the serialization captured the complete simulation state.

## Related tools

- **ViMMS** (Simulation engine that generates in-memory EvaluationData and scan outputs; provides Environment.write_mzML() method and save_eval flag to enable serialization workflow) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Serializes EvaluationData object (containing Compound instances and fragmentation events) to persistent binary file format)

## Examples

```
import pickle
from vimms.ChemicalSampler import UniformMZSampler
from vimms.Environment import Environment
from vimms.Controller import SimpleController

env = Environment(ChemicalSampler=UniformMZSampler(...), save_eval=True)
env.run(SimpleController(), progress_bar=False)
pickle.dump(env.eval_data, open('sim_output.pickle', 'wb'))
env.write_mzML('sim_output.mzML')
```

## Evaluation signals

- Both .pickle and .mzML files exist at the output path and are non-empty (file size > 0 bytes)
- Pickle file can be successfully deserialized using pickle.load() without corruption errors
- Deserialized EvaluationData object retains the full Compound list, scan records, and fragmentation event metadata without loss
- mzML file contains valid XML structure with <scan> elements that reference the same m/z and retention time ranges as the original simulation parameters
- Filenames are linked (e.g., share a common root) and are written to the same output directory for co-location

## Limitations

- Pickle format is Python-specific and not human-readable; cross-language interoperability is limited. For integration with non-Python tools, mzML output must be used independently.
- Pickle files can be large when serializing high-cardinality EvaluationData (many compounds, many fragmentation events); no built-in compression is applied.
- The serialized EvaluationData is a snapshot at the moment of serialization; dynamic simulation state (e.g., real-time controller decisions) is not captured if they occur after env.run() returns.
- mzML and pickle files must be kept synchronized manually; if one file is lost or modified, the artifact pair is broken and cross-validation is compromised.

## Evidence

- [other] ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions for downstream analysis.: "ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions"
- [other] 1. Run an Environment simulation with save_eval flag enabled to trigger evaluation data collection. 2. After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module. 3. Write the mzML scan output to a companion file using Environment.write_mzML(). 4. Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations.: "After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module. 3. Write the"
- [readme] you can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files.: "you can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files"
