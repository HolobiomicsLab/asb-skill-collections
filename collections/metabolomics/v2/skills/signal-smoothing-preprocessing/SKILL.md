---
name: signal-smoothing-preprocessing
description: Use when when working with raw LC-HRMS profile-mode data containing noisy
  chromatographic signals, apply this skill before peak detection. Smoothing is particularly
  needed when the signal-to-noise ratio is low or when gradient-based peak detection
  would be compromised by high-frequency noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - PeakBot
  techniques:
  - LC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: christophuv/PeakBot
  license_tier: noncommercial
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac344
  title: PeakBot
evidence_spans:
- PeakBot is a python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakbot_cq
    doi: 10.1093/bioinformatics/btac344
    title: PeakBot
  dedup_kept_from: coll_peakbot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac344
  all_source_dois:
  - 10.1093/bioinformatics/btac344
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-smoothing-preprocessing

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Apply smoothing to LC-HRMS profile-mode chromatographic signals to reduce noise and enable robust local-maxima detection. This preprocessing step is essential before gradient-descent peak-picking to ensure reliable identification of chromatographic peaks versus background artifacts.

## When to use

When working with raw LC-HRMS profile-mode data containing noisy chromatographic signals, apply this skill before peak detection. Smoothing is particularly needed when the signal-to-noise ratio is low or when gradient-based peak detection would be compromised by high-frequency noise. Use this as the first step in the PeakBot workflow to prepare data for subsequent local-maxima identification.

## When NOT to use

- Input data is already centroided or in profile-mode but has been pre-processed by another peak-picking tool
- Signal-to-noise ratio is already very high (smoothing may unnecessarily degrade peak resolution)
- The downstream workflow requires preservation of high-frequency spectral features (e.g., isotope-pattern fidelity for MS/MS annotation)

## Inputs

- LC-HRMS profile-mode data (raw chromatographic signal as function of retention time and m/z)
- Raw chromatographic signal array (1D or 2D: retention time × m/z)

## Outputs

- Smoothed chromatographic signal array (retention time × m/z with reduced noise)
- Preprocessed signal ready for gradient computation and local-maxima detection

## How to apply

Load the LC-HRMS profile-mode data (e.g., from mzML or vendor formats) and apply a smoothing algorithm to the chromatographic signal dimension (retention time axis). The smoothing reduces high-frequency noise while preserving peak shape and retention-time accuracy, enabling the subsequent gradient-descent algorithm to reliably compute gradients and identify local maxima. The smoothed signal is then used as input to the gradient computation step. No specific smoothing parameters are detailed in the source material, but the smoothing must preserve peak morphology sufficiently that estimated peak borders and centers remain accurate for the downstream matching against reference features.

## Related tools

- **PeakBot** (Parent framework that implements signal smoothing as the first step in chromatographic peak detection from LC-HRMS profile-mode data) — https://github.com/christophuv/PeakBot

## Evaluation signals

- Smoothed signal retains peak shape and does not shift retention-time positions of true peaks by more than the instrument's RT precision tolerance
- Gradient computation on smoothed signal yields stable, interpretable gradients without spurious zero-crossings in noise-only regions
- Downstream local-maxima detected on smoothed signal match reference peaks from the user-defined reference list with expected retention-time agreement
- Visual inspection: smoothed chromatogram shows clear peak definition with suppressed noise spikes; compare smoothed vs. raw signal to verify noise reduction without over-smoothing

## Limitations

- Over-smoothing may merge closely-eluting isomeric peaks or reduce peak height estimates, leading to false negatives in peak detection
- Smoothing parameters are not explicitly specified in the source material; optimal smoothing strength may require empirical tuning per LC-HRMS platform and gradient method
- Smoothing is a lossy operation; retention of sufficient spectral detail (e.g., isotope patterns) may be compromised if smoothing is applied across m/z dimension as well as RT

## Evidence

- [other] Load LC-HRMS profile-mode data from the input file. 2. Apply smoothing to the chromatographic signal.: "Load LC-HRMS profile-mode data from the input file. 2. Apply smoothing to the chromatographic signal."
- [intro] searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [other] Compute gradients and identify local maxima using gradient-descent algorithm.: "Compute gradients and identify local maxima using gradient-descent algorithm."
