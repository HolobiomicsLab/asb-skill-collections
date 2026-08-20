---
name: chemical-fragmentation-event-tracking
description: Use when when running a ViMMS Environment simulation with save_eval flag enabled and you need to correlate fragmentation events in the output mzML file back to their originating chemical compounds for downstream evaluation, optimization, or validation of acquisition strategies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - ViMMS
  - Python pickle module
  - MZMine
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

# Chemical Fragmentation Event Tracking

## Summary

Track and persist fragmentation events and their source chemical definitions during simulated mass spectrometry acquisitions, enabling post-run linkage between generated MS/MS scans and the chemicals that produced them. This skill is essential for evaluating data-dependent acquisition strategies where understanding which chemical gave rise to which fragmentation spectrum is necessary for validation and optimization.

## When to use

When running a ViMMS Environment simulation with save_eval flag enabled and you need to correlate fragmentation events in the output mzML file back to their originating chemical compounds for downstream evaluation, optimization, or validation of acquisition strategies. Use this when your analysis goal requires tracing MS/MS spectra to specific metabolites or testing whether expected chemicals were successfully fragmented during the virtual run.

## When NOT to use

- If you are replaying an existing LC-MS/MS run from real data and do not need to validate which chemicals were fragmented (evaluation data is unnecessary in pure data replay scenarios).
- If your evaluation goal is only cosmetic visualization and you do not need programmatic linkage between scans and chemicals for downstream analysis.
- If storage or I/O performance is critical and you cannot afford to persist both pickle and mzML files for every simulation.

## Inputs

- ViMMS Environment object with save_eval=True after simulation completion
- In-memory EvaluationData object containing fragmentation events
- Generated scan list with precursor m/z, retention time, and intensity data

## Outputs

- Pickle file (.p) containing serialized EvaluationData artifact
- Companion mzML file with scan-level fragmentation spectra
- Linked scan metadata enabling traceability from mzML back to chemical definitions

## How to apply

Enable evaluation data collection by setting the save_eval flag when instantiating the ViMMS Environment. After env.run() completes and fragmentation events have been collected in memory, serialize the in-memory EvaluationData object (which contains the list of chemicals sampled, all generated scans with their fragmentation events, and chemical metadata) to a pickle file using Python's pickle module. Write the companion mzML scan output using Environment.write_mzML() to a file with matching metadata. The EvaluationData object maintains a bidirectional link: each scan in the mzML carries metadata (e.g., precursor m/z, retention time, scan index) that can be matched back to entries in the EvaluationData structure. Verify both files exist and are accessible; the pickle file preserves the full chemical definitions and fragmentation event log, while the mzML contains the serialized spectra for external tool compatibility.

## Related tools

- **ViMMS** (Primary simulation framework; provides Environment object, fragmentation event generation, and EvaluationData container; orchestrates collection of chemical definitions and scan data during run) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Serialization mechanism for persisting in-memory EvaluationData object and chemical definitions to disk)
- **MZMine** (Post-processing tool referenced for peak picking and spectral matching; evaluation helpers rely on MZMine parameters in PeakPicking.py)

## Examples

```
from vimms.Environment import Environment; env = Environment(mass_spec, controller, chemicals, save_eval=True); env.run(); env.write_mzML('output.mzML'); save_obj(env.eval_data, 'eval_data.p')
```

## Evaluation signals

- Both pickle and mzML companion files exist and are non-empty after env.run() + serialization
- Pickle file deserializes without error and contains EvaluationData object with non-empty chemicals list and scan event log
- mzML file is valid XML/binary and contains scan entries with precursor m/z and retention time metadata matching entries in EvaluationData
- Bidirectional lookup succeeds: select a scan from mzML, retrieve its metadata (precursor m/z, RT), find corresponding entry in EvaluationData.chemicals and confirm fragmentation event(s) are logged
- Fragmentation event count in EvaluationData matches the number of MS/MS scans written to mzML (or exceeds it if some events were filtered)

## Limitations

- Pickle files are Python-specific and not portable across Python versions or platforms without risk; for cross-platform or long-term archival, supplementary conversion to JSON or CSV is recommended.
- The evaluation data artifact can be large if the simulation covers many chemicals or long chromatographic runs; disk I/O and memory overhead scale linearly with run complexity.
- EvaluationData linkage assumes deterministic ordering and matching of scans by index and retention time; if mzML is post-processed (reordered, filtered) without corresponding updates to the pickle, traceability is broken.
- Fragmentation event tracking is only accurate if the ViMMS controller and chemical fragmentation model are correctly configured; garbage-in, garbage-out applies to event quality.

## Evidence

- [other] Run an Environment simulation with save_eval flag enabled to trigger evaluation data collection. After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module.: "Run an Environment simulation with save_eval flag enabled to trigger evaluation data collection. After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals,"
- [other] ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions for downstream analysis.: "ViMMS uses the save_obj function to persist evaluation data and chemical objects to pickle files, enabling linkage between simulated scans in the generated mzML and their source chemical definitions"
- [other] Write the mzML scan output to a companion file using Environment.write_mzML(). Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations.: "Write the mzML scan output to a companion file using Environment.write_mzML(). Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations."
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`.: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`."
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
