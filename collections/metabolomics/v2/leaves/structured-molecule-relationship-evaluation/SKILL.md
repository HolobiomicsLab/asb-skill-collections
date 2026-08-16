---
name: structured-molecule-relationship-evaluation
description: Use when when you have tandem mass spectra (MSMS) from related or candidate
  molecules and need to determine which similarity metric—cosine, modified cosine,
  or neutral loss— ranks structurally similar compounds in your dataset. Particularly
  useful when structural relationships are known a priori (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - cosine_neutral_loss
  - spectrum_utils
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.2c00153
  title: Neutral-loss similarity
- doi: 10.1016/1044-0305
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_neutral_loss_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.2c00153
  all_source_dois:
  - 10.1021/jasms.2c00153
  - 10.1016/1044-0305
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structured molecule relationship evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically compare cosine, modified cosine, and neutral loss spectrum similarity measures to rank and discover structurally related molecules from mass spectral data. This skill enables selection of the most effective similarity metric for a given discovery task by benchmarking retrieval performance across spectrum pairs.

## When to use

When you have tandem mass spectra (MSMS) from related or candidate molecules and need to determine which similarity metric—cosine, modified cosine, or neutral loss—best ranks structurally similar compounds in your dataset. Particularly useful when structural relationships are known a priori (e.g., analogs, congeners) and you want to validate or compare metric sensitivity.

## When NOT to use

- When spectra have not been preprocessed or validated (unknown precursor charge, uncorrected m/z calibration, or intense contaminant peaks).
- When structural ground truth is not available or unreliable, making performance benchmarking impossible.
- When working with single spectra or non-comparative scenarios where you only need one similarity score without metric validation.

## Inputs

- Tandem mass spectra (MSMS) as USI identifiers or spectrum objects
- Precursor m/z and charge state
- Spectrum intensity arrays and m/z arrays
- Ground-truth structural relationships (e.g., list of known analogs or related compounds)

## Outputs

- Similarity scores (cosine, modified cosine, neutral loss) for each spectrum pair
- Ranked lists of candidate molecules per similarity metric
- Retrieval performance metrics (e.g., ranking of true analogs, precision@k, AUC)
- Comparative performance summary and recommendation for best-performing metric

## How to apply

Load spectrum pairs from your dataset using spectrum utilities (e.g., spectrum_utils.spectrum.MsmsSpectrum). Preprocess each spectrum by setting m/z range (0 to precursor m/z), removing precursor peaks (e.g., ±0.1 Da tolerance), and normalizing intensity. Apply all three similarity measures (cosine, modified cosine, neutral loss) to each spectrum pair using the repository implementations. Rank candidate molecules by each similarity score and evaluate retrieval performance metrics (e.g., ranking position of known structural analogs, area under precision-recall curve). Compare performance across the three measures to determine which metric maximizes sensitivity for your compound class and dataset characteristics.

## Related tools

- **cosine_neutral_loss** (Implements cosine similarity, modified cosine similarity, and neutral loss similarity measures; provides plot.plot_mirror() for visual comparison of spectrum alignments under each metric) — https://github.com/bittremieux/cosine_neutral_loss
- **spectrum_utils** (Provides spectrum object model (MsmsSpectrum) for loading, parsing, and preprocessing spectra; enables m/z range setting and precursor peak removal)

## Examples

```
import spectrum_utils.spectrum as sus
import plot
spectrum1 = sus.MsmsSpectrum.from_usi("mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840")
spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz).remove_precursor_peak(0.1, "Da")
for score in ["cosine", "modified_cosine", "neutral_loss"]:
    plot.plot_mirror(spectrum1, spectrum2, score, f"{score}.png")
```

## Evaluation signals

- Verify all three similarity scores are computed and returned as numeric values in [0, 1] or equivalent normalized range.
- Confirm known structural analogs rank higher under the selected metric than under non-selected metrics.
- Check that precursor peaks have been removed and m/z ranges are consistent (0 to precursor m/z) before similarity computation.
- Validate that performance metrics (e.g., ranking position of true analogs) are consistent with reported findings from the Bittremieux et al. (2022) benchmarking study.
- Ensure mirror plots visually show expected alignment differences: cosine aligns common peaks, modified cosine accounts for fragment mass shifts, neutral loss considers mass differences between fragments.

## Limitations

- Neutral loss similarity is sensitive to accurate peak annotation and mass accuracy; poor mass calibration can inflate false positives.
- Modified cosine similarity may favor compounds with similar fragmentation patterns even if structurally distinct; cross-validation with orthogonal data is recommended.
- Performance is dataset-dependent; metric ranking may differ for different compound classes (e.g., lipids vs. alkaloids) or ionization modes.
- Requires reliable ground truth for benchmarking; if structural relationships are uncertain or incomplete, performance evaluation will be unreliable.

## Evidence

- [readme] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [readme] Similarity measures implemented and their theoretical basis: "Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity"
- [readme] Workflow for creating mirror plots and comparing metrics: "for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"), ("neutral_loss", "neutral_loss.png")]"
- [readme] Spectrum preprocessing requirements: "spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da")"
- [other] Repository implementation and tool citation: "Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison"
