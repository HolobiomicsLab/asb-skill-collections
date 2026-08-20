---
name: file-format-writing-mzml
description: Use when after completing an Environment simulation or replay with scan-level MS2 acquisition control, and evaluation data has been collected in memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3172
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

# file-format-writing-mzml

## Summary

Serialize simulated or replayed mass spectrometry scan data from a ViMMS Environment into the standard mzML (mzXML Markup Language) format for downstream analysis and archival. This enables portable exchange of LC-MS/MS scan metadata, fragmentation spectra, and retention time information with external metabolomics tools.

## When to use

After completing an Environment simulation or replay with scan-level MS2 acquisition control, and evaluation data has been collected in memory. Use this skill when you need to export simulated or replayed scan results into a standard, interoperable format for spectral matching, metabolite identification, or validation against reference libraries (e.g., GNPS-NIST14-MATCHES).

## When NOT to use

- If evaluation data has not been collected (save_eval flag was not enabled during environment setup); write_mzML() requires populated scan metadata.
- If the goal is to persist the in-memory EvaluationData object itself (chemicals, fragmentation events, and scan-source linkage) for reuse—use pickle serialization instead, which preserves full Python object state.
- If you need to compare or filter scans before export; write_mzML() commits all collected scans to the file without intermediate curation.

## Inputs

- ViMMS Environment object (post-simulation, with populated scan list)
- EvaluationData artifact (in-memory, containing collected scans and fragmentation events)
- Simulated or replayed LC-MS/MS run metadata (retention times, m/z ranges, isolation windows)

## Outputs

- mzML file (XML-formatted mass spectrometry data)
- Companion mzML scan records (linked to source chemical definitions and fragmentation metadata)

## How to apply

After env.run() completes and the in-memory scan list is populated, invoke Environment.write_mzML() to serialize all collected scans (MS1 survey scans, MS2 fragmentation scans, retention times, m/z values, intensities, and precursor ion information) into a companion mzML file. The method writes structured XML-based scan records linked to the chemical definitions and fragmentation events captured during the simulation. Verify that the output file is well-formed XML and that all scan indices, precursor m/z windows, and isolation windows match the simulated acquisition parameters (e.g., isolation width, collision energy settings). Cross-check that the number of MS2 scans in the mzML matches the number of precursor ions targeted by the controller strategy.

## Related tools

- **ViMMS** (Mass spectrometry simulation framework; provides Environment.write_mzML() method to serialize scan data into mzML format) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Alternative serialization format for persisting in-memory EvaluationData objects alongside mzML output files)

## Examples

```
env.write_mzML('output_simulation.mzML'); import pickle; pickle.dump(env.evaluation_data, open('evaluation_data.p', 'wb'))
```

## Evaluation signals

- Output mzML file exists at the specified path and is valid XML (parseable by standard mzML readers).
- Number of MS2 scans in the mzML equals the number of precursor ions targeted by the acquisition controller strategy.
- All scan indices, retention times, precursor m/z, and isolation windows in the mzML match the simulation metadata and environment parameters.
- The mzML file can be successfully ingested by downstream tools (e.g., MZmine peak picking, GNPS spectral matching) without schema or encoding errors.
- Cross-validation: scan count in mzML matches the length of the Environment's scan list; fragmentation event counts align with collected EvaluationData.

## Limitations

- The write_mzML() method requires that evaluation data has been collected during the Environment run (save_eval=True); unevaluated runs will produce an incomplete or empty mzML file.
- The method serializes only the scans present in the Environment's in-memory scan list at the time of the call; scans cannot be selectively filtered or pruned before export without modifying the Environment object.
- The mzML output is linked to the specific simulation parameters and controller strategy used; replay of the same data with different strategies will produce different mzML files (e.g., different MS2 precursor selections).

## Evidence

- [other] After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module. Write the mzML scan output to a companion file using Environment.write_mzML().: "After env.run() completes, serialize the in-memory EvaluationData object (containing chemicals, generated scans, and fragmentation events) to a pickle file using Python's pickle module. Write the"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies. With ViMMS, you can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files.: "extract the scan results as mzML files"
- [other] Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations.: "Verify both the pickle and mzML files exist and are accessible for subsequent evaluation operations."
