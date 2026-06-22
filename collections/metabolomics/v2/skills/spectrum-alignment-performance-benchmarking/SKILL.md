---
name: spectrum-alignment-performance-benchmarking
description: Use when you have tandem MS spectra from structurally related or known compounds and need to decide which similarity metric will maximize correct ranking of related molecules in a spectral library search.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - cosine_neutral_loss
  - spectrum_utils
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
---

# Spectrum alignment performance benchmarking

## Summary

Compare multiple spectral similarity measures (cosine, modified cosine, neutral loss) on the same dataset to evaluate their relative effectiveness for discovering structurally related molecules from tandem mass spectrometry data. This skill benchmarks retrieval performance across similarity metrics to guide selection of the most appropriate measure for a given discovery task.

## When to use

You have tandem MS spectra from structurally related or known compounds and need to decide which similarity metric will maximize correct ranking of related molecules in a spectral library search. Use this skill when you want empirical evidence for metric choice rather than assuming one metric is universally superior.

## When NOT to use

- Spectra are from completely unrelated or unknown compounds with no structural ground truth — benchmarking requires labeled or curated pairings to measure retrieval correctness.
- Your goal is real-time library search on large repositories where computational speed is the primary constraint — this skill focuses on accuracy comparison, not optimization of runtime.
- Input spectra are already pre-filtered or processed by a single similarity metric upstream — start with raw spectrum pairs to enable fair comparison.

## Inputs

- Tandem mass spectrometry spectrum pairs (USI identifiers or m/z–intensity arrays)
- Structurally related molecule annotations or ground-truth pairings
- Spectral dataset (GNPS library or custom repository)

## Outputs

- Ranked lists of candidate matches per spectrum per similarity metric
- Performance metrics per similarity measure (e.g., recall, precision, ranking accuracy)
- Comparative ranking tables and visualizations (e.g., mirror plots)

## How to apply

Load your spectral dataset and prepare spectrum pairs for comparison. Implement or load the three similarity measures: cosine similarity, modified cosine similarity (accounting for fragment intensity ratios), and neutral loss similarity (measuring differences in mass losses between precursor and fragments). Apply each measure to the same set of spectrum pairs. Evaluate retrieval performance by ranking structurally related molecules for each metric and computing performance metrics such as recall-at-rank or area under the receiver operating characteristic curve. Compile comparison results side-by-side; differences in retrieval ranking across metrics indicate which measures best preserve structural similarity for your molecular class.

## Related tools

- **cosine_neutral_loss** (Repository implementing all three spectrum similarity measures (cosine, modified cosine, neutral loss) and providing utility functions for spectrum loading, preprocessing, and mirror plot generation.) — https://github.com/bittremieux/cosine_neutral_loss
- **spectrum_utils** (Python library for reading, preprocessing, and manipulating MSMS spectra; used to load spectra from USI identifiers, set m/z ranges, and remove precursor peaks before similarity calculation.)

## Examples

```
import spectrum_utils.spectrum as sus; import plot; spectrum1 = sus.MsmsSpectrum.from_usi('mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840'); spectrum2 = sus.MsmsSpectrum.from_usi('mzspec:MSV000086109:BD5_dil2x_BD5_01_57213:scan:760'); [plot.plot_mirror(spectrum1, spectrum2, score, f'{score}.png') for score in ['cosine', 'modified_cosine', 'neutral_loss']]
```

## Evaluation signals

- All three similarity measures produce scores in the range [0, 1] for the same spectrum pairs; verify no NaN or out-of-bounds values.
- Retrieval rankings for each metric can be compared by sorting candidate matches by score; check that structurally related molecules (ground truth) rank higher in at least one metric.
- Performance metrics (e.g., recall@10, area under ROC) are computed consistently across all three measures using the same ground-truth labels and ranking methodology.
- Mirror plots generated for known analogue pairs show visually interpretable alignments; peaks aligned by each metric should reflect the measure's definition (e.g., modified cosine emphasizes shared intense peaks).
- Differences in performance metrics across metrics are statistically meaningful and reproducible when re-run on the same data with identical parameters.

## Limitations

- Similarity measures may perform differently across different molecular classes (e.g., lipids vs. peptides); benchmark results are not universally transferable.
- Ground-truth structural relatedness must be carefully curated or sourced from authoritative databases (e.g., GNPS); mislabeled or ambiguous pairings bias comparison.
- Preprocessing steps (precursor mass tolerance, m/z range, peak intensity normalization) can significantly influence relative performance; variations in preprocessing must be controlled.
- No changelog is provided for the source repository, limiting traceability of algorithmic changes across versions.

## Evidence

- [readme] Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity: "Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity"
- [intro] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [other] Evaluate retrieval performance (e.g., ranking of structurally related molecules) for each similarity measure across the dataset.: "Evaluate retrieval performance (e.g., ranking of structurally related molecules) for each similarity measure across the dataset."
- [readme] All code is available as open-source under the BSD license.: "All code is available as open-source under the BSD license."
- [intro] Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison: "Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison"
