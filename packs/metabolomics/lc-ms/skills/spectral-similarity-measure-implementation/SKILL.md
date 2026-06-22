---
name: spectral-similarity-measure-implementation
description: Use when you have MSMS spectra from two or more compounds and need to identify which are structurally related. Use this skill when you want to rank spectrum pairs by similarity to discover novel analogs or validate structural assignments in untargeted metabolomics or natural products discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3960
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - cosine_neutral_loss
  - spectrum_utils
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-measure-implementation

## Summary

Implement and apply cosine, modified cosine, and neutral loss similarity measures to compare MSMS spectra for discovery of structurally related molecules. This skill enables quantitative ranking of spectrum pairs by their similarity, supporting library search and molecular networking workflows.

## When to use

You have MSMS spectra from two or more compounds and need to identify which are structurally related. Use this skill when you want to rank spectrum pairs by similarity to discover novel analogs or validate structural assignments in untargeted metabolomics or natural products discovery. Apply it specifically when spectrum pairs require alignment-independent comparison or when neutral loss patterns (characteristic of compound class fragmentation) should be weighted equally with fragment peak matching.

## When NOT to use

- Input spectra are not preprocessed (precursor peak not removed, m/z range not normalized) — preprocessing is a prerequisite and this skill assumes valid input.
- You need spectrum de novo structure elucidation or chemical formula assignment — this skill only ranks similarity; it does not infer chemical structures or provide molecular annotations.
- Spectra are from different ionization modes or instrument types without cross-calibration — similarity scores are only meaningful for directly comparable spectra.

## Inputs

- MSMS spectrum pair(s) as MsmsSpectrum objects with precursor m/z, precursor charge, and fragment peaks (m/z and intensity)
- Spectral dataset or library with multiple MSMS spectra (e.g., GNPS-LIBRARY or MSV entries with USI identifiers)
- Preprocessed spectra with m/z range set and precursor peak removed

## Outputs

- Similarity score (float, range 0–1) for each spectrum pair under each similarity measure
- Ranked list of candidate molecules ordered by similarity score to query spectrum
- Mirror plot or comparison visualization showing fragment peak alignment under each similarity measure
- Performance metrics (e.g., retrieval rank of known structurally related molecules, recall@k)

## How to apply

Load two or more preprocessed MSMS spectra as MsmsSpectrum objects (precursor m/z, charge state, and fragment peaks with intensities specified). For each spectrum pair, compute one of three similarity scores: (1) cosine similarity, which treats peak m/z and intensity as vectors and calculates their dot product normalized by magnitude; (2) modified cosine similarity, which allows small m/z offsets (typically 0.1 Da) between matching fragments to account for measurement error; or (3) neutral loss similarity, which matches fragment pairs derived from the same neutral loss mass rather than absolute fragment m/z. Preprocess spectra by setting m/z range (0 to precursor m/z), removing the precursor peak (typically ±0.1 Da tolerance), and normalizing intensities. Apply all three measures to the same spectrum pairs to enable comparative evaluation of their ranking performance; score interpretations range from 0 (no similarity) to 1 (identical spectra). Rank candidate molecules by their similarity score to the query spectrum to assess retrieval effectiveness.

## Related tools

- **cosine_neutral_loss** (Implements cosine similarity, modified cosine similarity, and neutral loss similarity measures; provides plot and utility functions for spectrum preprocessing and mirror plot generation) — github.com/bittremieux/cosine_neutral_loss
- **spectrum_utils** (Provides MsmsSpectrum class for loading, preprocessing (m/z range setting, precursor removal), and manipulating spectrum data; accessed via sus.MsmsSpectrum.from_usi())

## Examples

```
import spectrum_utils.spectrum as sus; import plot; spectrum1 = sus.MsmsSpectrum.from_usi("mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840"); spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz).remove_precursor_peak(0.1, "Da"); plot.plot_mirror(spectrum1, spectrum2, "neutral_loss", "output.png")
```

## Evaluation signals

- Similarity scores are bounded in [0, 1] for all three measures and identical spectra score 1.0
- Known structurally related molecule pairs (e.g., analog/parent compound pairs) rank higher under all three measures than random unrelated spectra
- Modified cosine similarity recovers matches with m/z offsets (±0.1 Da) that cosine similarity misses, and neutral loss similarity ranks matches with shared fragmentation patterns higher than cosine
- Mirror plot visually aligns matched fragment peaks between spectra; alignment quality improves moving from cosine to modified cosine to neutral loss for structurally related pairs
- Retrieval performance (e.g., rank of true match in top-k results, recall@10) is consistent across multiple spectrum pairs and shows expected ranking differences between the three measures

## Limitations

- Similarity measures are insensitive to absolute fragment intensities if normalized; absolute intensity differences (e.g., due to instrument variation or ionization efficiency) do not affect cosine or neutral loss scores but may indicate true chemical differences.
- Modified cosine similarity requires careful selection of m/z tolerance (typically 0.1 Da); values that are too large will cause spurious matches, while too-small tolerances may miss genuine peaks.
- Neutral loss similarity is effective only when spectra exhibit characteristic neutral losses (e.g., loss of water or ammonia); compounds with few or non-specific neutral losses may not benefit from this measure.
- Similarity measures do not account for spectral quality, dynamic range compression, or missing fragments due to instrumental limitations; low signal-to-noise spectra may produce unreliable scores.

## Evidence

- [readme] Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity: "Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity"
- [intro] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [intro] Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison: "Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison"
- [readme] for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"), ("neutral_loss", "neutral_loss.png")]: plot.plot_mirror(spectrum1, spectrum2, score, filename): "for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"), ("neutral_loss", "neutral_loss.png")]: plot.plot_mirror(spectrum1, spectrum2,"
- [readme] spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da"): "spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da")"
