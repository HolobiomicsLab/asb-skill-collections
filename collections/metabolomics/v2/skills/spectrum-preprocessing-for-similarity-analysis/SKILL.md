---
name: spectrum-preprocessing-for-similarity-analysis
description: Use when when you have raw MS/MS spectra with residual noise or low-intensity peaks and plan to calculate spectral entropy, entropy similarity, or perform spectral library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectral_similarity
  - MSEntropy
  - Entropy Search GUI
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- '.. automodule:: spectral_similarity :members:'
- These are all integrated into the [MSEntropy package
- These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_entropy_cq
    doi: 10.1038/s41592-021-01331-z
    title: Spectral entropy
  dedup_kept_from: coll_spectral_entropy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01331-z
  all_source_dois:
  - 10.1038/s41592-021-01331-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-preprocessing-for-similarity-analysis

## Summary

Preprocesses MS/MS spectra by removing low-intensity noise peaks to improve downstream spectral similarity and entropy-based compound identification. Applied before entropy similarity or other spectral comparison algorithms to ensure reliable quantification of spectral features.

## When to use

When you have raw MS/MS spectra with residual noise or low-intensity peaks and plan to calculate spectral entropy, entropy similarity, or perform spectral library matching. Apply this before any spectral comparison algorithm to maximize identification performance, especially when using entropy-based methods that are sensitive to peak intensity distributions.

## When NOT to use

- Spectra that have already undergone vendor-specific noise filtering or normalization—re-applying this threshold may over-filter and lose weak but genuine signal.
- Analysis pipelines that require retention of all detected peaks for absolute intensity quantitation or spectral imaging where weak peaks carry spatial information.
- High-resolution or high-sensitivity MS experiments where weak peaks near the 1% threshold are intentionally retained for trace-level or targeted detection.

## Inputs

- raw MS/MS spectra with peak intensity values
- peak lists (m/z, intensity pairs) from mass spectrometry experiments

## Outputs

- noise-filtered MS/MS spectra with low-intensity peaks removed
- preprocessed peak lists suitable for spectral similarity calculation

## How to apply

Load preprocessed MS/MS spectra and filter peaks by removing those with intensity less than 1% of the maximum peak intensity in the spectrum. This noise removal step is recommended before calculating spectral similarity metrics. The rationale is that low-intensity peaks contribute noise rather than signal to entropy and similarity calculations; removing them preserves the informative portion of the spectrum (peaks ≥1% max intensity) while discarding spurious signals. Apply this threshold uniformly to all input spectra prior to computing entropy similarity scores or other distance metrics.

## Related tools

- **MSEntropy** (Host package providing spectral_similarity module with preprocessing integration) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity** (Module that operates on preprocessed spectra to compute entropy similarity scores) — https://github.com/YuanyueLi/MSEntropy
- **Entropy Search GUI** (User-facing tool that applies preprocessing internally before spectral file comparison) — https://github.com/YuanyueLi/EntropySearch

## Examples

```
import numpy as np
import ms_entropy as me
peaks_raw = np.array([[69.071, 0.5], [86.066, 100], [120.0, 2.0]])
max_intensity = np.max(peaks_raw[:, 1])
peaks_filtered = peaks_raw[peaks_raw[:, 1] >= 0.01 * max_intensity]
similarity = me.spectral_entropy_similarity(peaks_filtered, peaks_reference)
```

## Evaluation signals

- Verify that all retained peaks have intensity ≥ 1% of the maximum intensity in each spectrum.
- Confirm that the number of peaks decreases (noise removed) compared to the raw spectrum, but the top-intensity peaks remain unchanged.
- Entropy similarity score for known spectrum pairs matches reference outputs after preprocessing.
- Calculated entropy similarity value falls within the expected range [0, 1] as per the spectral_similarity module specification.
- Peak counts and intensity distributions in output metadata match the filtered peak set (no peaks below 1% threshold present).

## Limitations

- The 1% intensity threshold is a general heuristic and may require adjustment for low-abundance compounds or noisy instrumentation; no adaptive threshold selection is provided.
- Preprocessing alone does not account for m/z calibration errors, isotope patterns, or in-source fragmentation artifacts that can confound spectral comparison.
- Removing low-intensity peaks is irreversible; spectra cannot be recovered to their original raw state once filtered.
- Performance improvement from preprocessing depends on the quality of the raw spectra; already clean spectra will show minimal benefit.

## Evidence

- [other] Before calculating spectral similarity, it's highly recommended to remove spectral noise: "Before calculating spectral similarity, it's highly recommended to remove spectral noise"
- [other] Peaks below 1% max intensity removed to improve identification performance: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
- [methods] Preprocessing involves filtering noise from input spectra: "Load two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered) from input files."
- [intro] Entropy similarity operates on preprocessed spectra for reliable quantification: "our package includes spectral entropy, entropy similarity, and many other functions"
