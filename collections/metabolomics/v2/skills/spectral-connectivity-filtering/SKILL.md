---
name: spectral-connectivity-filtering
description: Use when you have picked peaks (coordinates and intensities) from an INADEQUATE NMR spectrum and need to cluster them into networks representing individual compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - Python
  - PyINETA
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- pyINETA is a Python package
- python run_pyineta.py <options>
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
---

# spectral-connectivity-filtering

## Summary

Filter picked peaks from INADEQUATE NMR spectra by applying network-based clustering logic to group peaks that originate from the same compound based on spectral connectivity patterns. This skill identifies peak networks meeting internal criteria before matching to a simulated metabolite database.

## When to use

You have picked peaks (coordinates and intensities) from an INADEQUATE NMR spectrum and need to cluster them into networks representing individual compounds. Use this skill when your input consists of isolated peak detections that must be grouped by their spectral connectivity before metabolite identification or database matching can proceed.

## When NOT to use

- Input is raw INADEQUATE spectrum data (use Picking module first)
- Peaks have not yet been picked or extracted from the spectrum
- You have already identified metabolites and need only visualization or summary statistics

## Inputs

- Picked peaks from PyINETA Picking module (peak coordinates and intensities)
- Peak coordinate data (chemical shift positions)
- Peak intensity values

## Outputs

- Filtered peak network assignments table
- Compound network clusters (peaks grouped by connectivity)
- Peak network metadata (network ID, constituent peaks, connectivity scores)

## How to apply

Load the picked peaks output from the PyINETA Picking module, which provides peak coordinates and intensities. Apply network-based clustering logic within the Finding module to group peaks that likely originate from the same compound based on spectral connectivity patterns—peaks are connected if they share coherence pathways indicative of a single molecular structure. Filter and retain only peak networks that meet the module's internal criteria for compound association (based on connectivity strength and network topology). Output the filtered peak network assignments as a structured table, with each row representing a distinct compound network and its constituent peaks ready for downstream database matching.

## Related tools

- **PyINETA** (Contains the Finding module that performs spectral connectivity-based network clustering and filtering of picked peaks) — https://github.com/edisonomics/PyINETA
- **Python** (Programming language in which PyINETA and its Finding module are implemented)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s find -o output_folder
```

## Evaluation signals

- Output peak network table has consistent schema with network IDs, constituent peak lists, and connectivity scores for each compound
- Number and composition of output networks is stable across runs with identical input (reproducibility check)
- Peaks within each network show stronger mutual connectivity than peaks across different networks
- All output networks meet the module's internal criteria threshold; networks below threshold are absent from output
- Downstream database matching step successfully identifies metabolites from the output networks with acceptable match scores

## Limitations

- Network clustering quality depends on peak picking accuracy; poor peak picking will produce spurious or fragmented networks
- The module's internal connectivity criteria are not fully documented; users cannot adjust filtering thresholds directly
- Compounds with very similar or overlapping peak patterns may be incorrectly merged or split depending on spectral resolution

## Evidence

- [other] Load picked peaks from the output of the PyINETA Picking module (peak coordinates and intensities). Apply network-based clustering logic within the Finding module to group peaks that likely originate from the same compound based on spectral connectivity patterns.: "Load picked peaks from the output of the PyINETA Picking module (peak coordinates and intensities). Apply network-based clustering logic within the Finding module to group peaks that likely originate"
- [readme] It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound: "filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [other] Filter and retain only peak networks meeting the module's internal criteria for compound association. Output the filtered peak network assignments as a structured table.: "Filter and retain only peak networks meeting the module's internal criteria for compound association. Output the filtered peak network assignments as a structured table."
- [intro] pyINETA is designed to filter picked peaks to identify networks of peaks ideally coming from the same compound, which it then matches to a simulated INADEQUATE database of metabolites: "pyINETA is designed to filter picked peaks to identify networks of peaks ideally coming from the same compound, which it then matches to a simulated INADEQUATE database of metabolites"
