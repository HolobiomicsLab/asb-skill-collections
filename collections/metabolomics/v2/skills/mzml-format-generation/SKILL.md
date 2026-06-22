---
name: mzml-format-generation
description: Use when after completing a virtual LC-MS/MS acquisition simulation using ViMMS (e.g., after calling env.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ViMMS
  - MZmine
  - GNPS
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

# mzml-format-generation

## Summary

Convert simulated LC-MS/MS acquisition scans into mzML (mass spectrometry Markup Language) format for downstream analysis, archiving, and interoperability with metabolomics software. This skill bridges virtual mass spectrometry simulation with standard data formats used in untargeted metabolomics workflows.

## When to use

After completing a virtual LC-MS/MS acquisition simulation using ViMMS (e.g., after calling env.run() on an Environment instance with a configured mass spectrometer, controller, and chemical mixture), when you need to export the raw scan data into a portable, standardized format that can be read by peak-picking tools (MZmine), spectral matching libraries (GNPS), or other downstream metabolomics software. Use this skill whenever simulation results must be archived or integrated into existing untargeted metabolomics pipelines.

## When NOT to use

- Input is already in mzML or another standard LC-MS format (NetCDF, mzXML) — convert between formats directly rather than re-simulating.
- Simulation has not yet been executed or Environment.run() failed — no scans to serialize.
- Analysis goal is purely in-memory statistical comparison of DDA vs. DIA strategies within ViMMS — file export is unnecessary overhead.

## Inputs

- Environment instance (ViMMS) containing completed LC-MS acquisition (MS1 and/or MS2 scans)
- Scan data with retention time, m/z array, intensity array, MS level, and (if MS2) precursor m/z and fragmentation metadata

## Outputs

- mzML file (XML-based mass spectrometry data format)
- Indexed mzML with scan-level metadata and data encodings (base64 or 32-bit/64-bit numeric precision)

## How to apply

After the ViMMS simulation completes and populates the Environment with MS1 and/or MS2 scans, call the Environment.write_mzML() method to serialize all acquired scans, retention times, m/z values, intensities, and fragment ions into mzML XML format. The method abstracts the low-level details of retention time indexing, scan-level metadata (MS level, precursor m/z, collision energy), and mass accuracy representation. Verify that the output file is well-formed XML and that the scan count and m/z range match expectations from the input chemical mixture (e.g., if sampling from HMDB with min_mz=100, max_mz=1000, all precursor ions in mzML should fall within that range). The mzML file can then be directly ingested by MZmine peak-picking, GNPS spectral library matching, or other standard tools without further format conversion.

## Related tools

- **ViMMS** (Simulates LC-MS/MS acquisition and provides Environment.write_mzML() method to serialize scans into mzML format.) — https://github.com/glasgowcompbio/vimms
- **MZmine** (Reads and processes mzML files for peak picking and ROI extraction using configured parameters (e.g., min_ms1_intensity threshold).)
- **GNPS** (Accepts mzML files for spectral library matching and community spectral annotation.)

## Examples

```
from vimms.Environment import Environment
env = Environment(mass_spectrometer, controller, min_rt=0, max_rt=1440)
env.run()
env.write_mzML('output_simulation.mzML')
```

## Evaluation signals

- Output file is well-formed XML and can be parsed by standard mzML validators (e.g., MS Data Tools).
- Scan count in mzML matches the number of MS1 and MS2 scans generated during env.run().
- All precursor m/z values in MS2 scans fall within the expected m/z range (e.g., 100–1000 for HMDB sampling).
- Retention time values are monotonically increasing and match the configured rt range (e.g., min_rt=0, max_rt=1440).
- mzML file successfully ingests into downstream tools (MZmine, GNPS) without format or encoding errors.

## Limitations

- mzML export captures only scan-level data; post-acquisition data processing (peak picking, feature alignment, annotation) must be performed downstream by external tools.
- File size grows linearly with scan count and spectral resolution; high-resolution full-scan simulations over long retention times can produce large files.
- mzML standard does not encode simulator-specific metadata (e.g., chemical mixture composition, controller strategy parameters); metadata must be tracked separately or stored in external documentation.
- Simulated scans lack real instrumental noise profiles and calibration artifacts present in measured LC-MS/MS data; mzML output is idealized and suitable for method prototyping but not for method validation against real-world data.

## Evidence

- [other] Execute env.run() to simulate the LC-MS acquisition process. 7. Write the resulting scans to mzML format using Environment.write_mzML().: "Execute env.run() to simulate the LC-MS acquisition process. 7. Write the resulting scans to mzML format using Environment.write_mzML()."
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies. With ViMMS, you can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files.: "With ViMMS, you can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files."
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py.: "The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py."
