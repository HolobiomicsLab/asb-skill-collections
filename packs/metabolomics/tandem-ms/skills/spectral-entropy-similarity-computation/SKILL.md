---
name: spectral-entropy-similarity-computation
description: Use when you need to measure the similarity between two MS/MS spectra as a continuous value that reflects both peak presence/absence and intensity patterns, particularly when comparing noisy versus denoised spectrum variants, or when ranking candidate reference library matches during compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectral_denoising
  - ms_entropy
  - pandas
  - RDkit
  - numpy
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- ms_entropy==1.3.3
- '- ``ms_entropy==1.3.3``'
- pandas==2.2.3
- '- ``pandas==2.2.3``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_denoising_cq
    doi: 10.1038/s41592-025-02646-x
    title: Spectral Denoising
  dedup_kept_from: coll_spectral_denoising_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02646-x
  all_source_dois:
  - 10.1038/s41592-025-02646-x
  - 10.1038/s41592-023-02012-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Entropy Similarity Computation

## Summary

Compute the entropy_similarity metric between query MS/MS spectra and reference spectra to quantify spectral resemblance while accounting for noise and intensity distributions. This metric enables comparison of spectral quality before and after denoising, and ranks library matches in denoising search workflows.

## When to use

Use this skill when you need to measure the similarity between two MS/MS spectra as a continuous value that reflects both peak presence/absence and intensity patterns, particularly when comparing noisy versus denoised spectrum variants, or when ranking candidate reference library matches during compound identification. Essential when evaluating whether electronic or chemical denoising improved spectral fidelity.

## When NOT to use

- Input spectra are already aligned to a common m/z grid or have been normalized to a fixed intensity scale independently — entropy_similarity assumes raw peak pairs.
- Your goal is to perform rapid similarity screening where computational cost is critical; entropy-based metrics are slower than simple dot-product cosine similarity on large libraries.
- Spectra lack sufficient peaks (< 5 fragment ions) for entropy estimation to be statistically meaningful.

## Inputs

- query_peaks (numpy array of shape [n, 2], columns: m/z and intensity)
- reference_peaks (numpy array of shape [m, 2], columns: m/z and intensity)
- precursor_mz (float, optional; used to exclude precursor region)

## Outputs

- entropy_similarity_score (float, range typically [0, 1])

## How to apply

Load a query spectrum (m/z and intensity pairs) and a reference spectrum from MSP files using sd.read_msp(). Extract the peaks array and precursor_mz from each. Call entropy_similarity(query_peaks, reference_peaks, pmz=precursor_mz) to compute the entropy-based similarity score. The pmz parameter optionally removes the precursor ion region (typically the last few m/z values) to focus on fragment ions. Repeat this computation for variants of the query spectrum: raw/noisy, electronically denoised, chemically denoised, and combined spectral denoised. Compare all resulting similarity values to establish whether denoising improved fidelity toward the reference. Higher entropy_similarity values (closer to 1.0) indicate better match; baseline or documented thresholds from the reference library help interpret results.

## Related tools

- **spectral_denoising** (Python package providing entropy_similarity() function and spectrum I/O (read_msp) for loading and comparing spectra) — https://github.com/FanzhouKong/spectral_denoising
- **ms_entropy** (Dependency providing core entropy computation and spectral_entropy() function used to assess spectrum quality) — https://pypi.org/project/ms_entropy/
- **numpy** (Array operations for peak data manipulation and intensity distribution handling)

## Examples

```
entropy_score = sd.entropy_similairty(peak_with_noise, peak, pmz=pmz); print(f'Entropy similarity: {entropy_score:.2f}')
```

## Evaluation signals

- Entropy_similarity score for noisy spectrum is lower than for its denoised counterparts (raw < electronic-denoised < formula-denoised ≤ combined-denoised).
- Entropy_similarity of denoised spectrum versus reference matches or exceeds documented baseline values from NIST23 or similar reference libraries.
- Score is between 0 and 1 (or normalized equivalently); values outside this range indicate computational error.
- When pmz is provided, the precursor ion region is excluded from calculation; verify by checking that the highest m/z peaks near pmz do not dominate the similarity score.
- Comparison of entropy_similarity values aligns with visual inspection of head-to-tail spectra plots (sd.head_to_tail_plot in Jupyter) — high similarity corresponds to strong peak overlap.

## Limitations

- Entropy_similarity computation requires sufficient peak density; spectra with very few ions or extremely low dynamic range may yield unreliable scores.
- The pmz parameter is optional; if omitted, precursor ions are not excluded and may artificially inflate similarity if present in both spectra.
- Score interpretation is relative to the reference spectrum chosen; different reference standards or library sources may yield different absolute scores for the same query.
- Python version must be 3.8 to 3.12; RDkit dependency (used by spectral_denoising) is not compatible with Python 3.13.
- No built-in threshold for 'good match' is provided; users must establish baselines empirically against known compound identifications.

## Evidence

- [other] research_question: "What are the entropy similarity values computed by the entropy_similarity function for noisy MS/MS spectra compared to their electronic-denoised, chemical-denoised, and spectral-denoised counterparts?"
- [other] workflow_step_computation: "Compute entropy_similarity() between noisy spectrum and clean reference spectrum (removing precursor region if pmz provided)"
- [other] workflow_step_comparison: "Compute entropy_similarity() between each denoised variant and the clean reference"
- [intro] finding_integration: "Integrating such process into spectra matching process, we developed denoising search, which psudo-denoise spectra based on molecular information fetched from reference databases"
- [readme] readme_usage_example: "print(f'the entropy similarity of contaminated spectrum and the raw spectrum is {entropy_similairty(peak_with_noise,peak,  pmz = pmz):.2f}')"
