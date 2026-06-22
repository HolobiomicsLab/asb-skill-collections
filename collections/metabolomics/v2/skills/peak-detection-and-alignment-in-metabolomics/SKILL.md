---
name: peak-detection-and-alignment-in-metabolomics
description: Use when after generating simulated mzML output from ViMMS and you need to compare it against real acquisition data. Specifically, use it when you have paired real and simulated mzML files from the same sample (e.g., Beer1pos) and must evaluate whether a fragmentation strategy (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - OpenMS
  - VIMMS
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
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

# peak-detection-and-alignment-in-metabolomics

## Summary

Peak detection and alignment extracts ion intensity peaks from LC-MS/MS mzML data and matches them across real and simulated acquisitions to compare fragmentation coverage and chemical detection. This skill is essential for validating whether simulated MS/MS strategies reproduce the same metabolite signals as experimental data.

## When to use

Apply this skill after generating simulated mzML output from ViMMS and you need to compare it against real acquisition data. Specifically, use it when you have paired real and simulated mzML files from the same sample (e.g., Beer1pos) and must evaluate whether a fragmentation strategy (e.g., Top-N DDA) captures the same chemicals and fragmentation patterns. This is required to benchmark new acquisition methods before deploying them on real instruments.

## When NOT to use

- Input mzML files are from different sample types or acquisition modes (e.g., comparing beer DDA with urine metabolite list); alignment will be meaningless.
- Only simulated mzML is available without corresponding real experimental data; coverage evaluation requires paired real–simulated comparisons.
- Raw mzML files have not been processed through the same chemical extraction pipeline (e.g., one uses ChemicalMixtureFromMZML and the other uses arbitrary formula sampling); peaks will not align reliably.

## Inputs

- Real mzML file (LC-MS/MS acquisition data)
- Simulated mzML file (ViMMS Environment output)
- Peak picking parameters (MZMine configuration)
- MS1 and MS/MS tolerance thresholds
- Intensity filter thresholds

## Outputs

- Peak lists (m/z, retention time, intensity) for real and simulated data
- Matched peak pairs with alignment scores
- Fragmentation coverage report (percentage of real chemicals recovered)
- Intensity correlation metrics
- Summary comparison table (real vs. simulated signals)

## How to apply

Extract peak lists from both real and simulated mzML files using OpenMS-based peak detection with consistent parameters (e.g., MZMine settings). Load the mzML files and apply peak picking to identify MS1 and MS/MS signals. Match peaks between real and simulated datasets using MS1 tolerance (1 ppm), MS/MS tolerance (0.05 ppm), and require a minimum of 3 matching peaks per putative chemical. Filter results by intensity thresholds (e.g., min_ms1_intensity = 1.75E5) and ROI parameters (e.g., min_roi_length=3) to exclude noise. Quantify fragmentation coverage by counting how many chemicals detected in real data also appear in the simulated data with comparable intensity and MS/MS fragmentation patterns. Report metrics such as percentage of real chemicals recovered, intensity correlation, and number of matching MS/MS peaks per chemical.

## Related tools

- **OpenMS** (Processes mzML output from simulation or real acquisition to compute fragmentation coverage using peak picking and spectral matching)
- **VIMMS** (Generates simulated mzML output that is input to this peak detection workflow for comparison against real data) — https://github.com/glasgowcompbio/vimms
- **Python** (Scripting language for orchestrating peak extraction, matching, and coverage calculation workflows)

## Examples

```
from vimms.evaluation import extract_peaks_from_mzml, match_peaks_between_files; real_peaks = extract_peaks_from_mzml('beer_real.mzML'); sim_peaks = extract_peaks_from_mzml('beer_simulated.mzML'); matched = match_peaks_between_files(real_peaks, sim_peaks, ms1_tol=1, ms2_tol=0.05, min_match_peaks=3, min_intensity=1.75e5)
```

## Evaluation signals

- Peak lists from real and simulated mzML files are non-empty and contain m/z, RT, and intensity columns in consistent format.
- Matched peak pairs have MS1 Δm/z ≤ 1 ppm and MS/MS Δm/z ≤ 0.05 ppm, confirming alignment fidelity.
- Fragmentation coverage (% of real chemicals found in simulated data) is reported as a single numeric value; typical success is >60–70% for well-tuned Top-N strategies on metabolite-rich samples.
- Intensity correlation between matched real and simulated peaks is computed (Pearson or Spearman r); r > 0.5 indicates good quantitative agreement.
- For each matched chemical, the number of matching MS/MS peaks and their intensity ratios are logged; missing peaks suggest incomplete fragmentation in simulation or real data.

## Limitations

- Peak detection relies on MZMine parameters (defined in PeakPicking.py) which may require tuning for sample type; suboptimal settings reduce alignment sensitivity.
- MS/MS matching (MS1 tolerance 1 ppm, MS/MS tolerance 0.05 ppm, minimum 3 matching peaks) is strict and may reject true matches in low-abundance or noisy regions.
- Fragmentation coverage depends critically on how well simulated chemicals match real acquisition chemicals; if ChemicalMixtureFromMZML extraction is incomplete or inaccurate, coverage will be artificially low.
- Intensity thresholds (e.g., min_ms1_intensity = 1.75E5) are sample-dependent; threshold must be re-optimized for different sample matrices (beer vs. urine vs. plasma).
- No changelog available in this article for versioning of peak-picking algorithms; reproducibility across ViMMS releases may vary.

## Evidence

- [results] Extract peaks from both real and simulated mzML files using OpenMS-based peak detection with consistent parameters.: "Extract peaks from both real and simulated mzML files using OpenMS-based peak detection with consistent parameters"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
- [results] Filter spectra matching with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks: "matching_ms1_tol = 1, matching_ms2_tol = 0.05, matching_min_match_peaks = 3"
- [results] Filter by MS1 intensity threshold 1.75E5: "min_ms1_intensity = 1.75E5"
- [other] Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
- [results] Compare fragmentation coverage and intensity metrics between real and simulated datasets and generate a summary report.: "Compare fragmentation coverage and intensity metrics between real and simulated datasets and generate a summary report"
