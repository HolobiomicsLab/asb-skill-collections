---
name: mass-spectrometry-library-search-retrieval
description: Use when when you have an unknown MSMS spectrum (precursor m/z and fragment
  ions) and need to discover structurally related compounds from a spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - cosine_neutral_loss
  - spectrum_utils
  techniques:
  - CE-MS
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

# Mass Spectrometry Library Search Retrieval

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank and retrieve structurally related molecules from mass spectral libraries using spectrum similarity measures (cosine, modified cosine, or neutral loss similarity). This skill enables identification of unknown compounds by comparing their MSMS spectra against a reference library ranked by spectral alignment quality.

## When to use

When you have an unknown MSMS spectrum (precursor m/z and fragment ions) and need to discover structurally related compounds from a spectral library. Use this skill when traditional database lookups are insufficient and you want to rank library spectra by similarity rather than exact precursor mass match, particularly for untargeted metabolomics or natural product discovery workflows.

## When NOT to use

- Input spectra are already matched to library entries via exact precursor mass or retention time — use direct database lookup instead.
- Only MS1 (precursor) data is available; this skill requires MSMS fragmentation spectra.
- Library contains very few spectra (< 10 reference compounds) — retrieval ranking is not meaningful at minimal scale.

## Inputs

- query MSMS spectrum (precursor m/z, charge, fragment ions with intensities)
- spectral library or set of reference MSMS spectra (same format as query)
- similarity measure selection (cosine | modified_cosine | neutral_loss)

## Outputs

- ranked list of library spectra with similarity scores
- mirror plots or annotated spectrum comparisons (optional visual output)
- retrieval performance metrics (if ground-truth structural relationships are known)

## How to apply

Load or prepare spectrum pairs: a query spectrum (unknown compound) and library spectra (reference compounds). Select one of three similarity measures based on your analyte class and library composition: cosine similarity for general-purpose spectral comparison, modified cosine similarity when neutral losses are informative but peaks need flexibility in m/z alignment, or neutral loss similarity when characteristic neutral losses define structural relationships. Calculate the chosen similarity metric for the query spectrum against all library spectra, producing ranked scores. Retrieve and rank library matches by descending similarity score; compounds ranked highest represent the best spectral alignment candidates for structural identification. Evaluation should consider whether top-ranked matches are known analogs or structurally plausible candidates.

## Related tools

- **cosine_neutral_loss** (Reference implementation providing cosine, modified cosine, and neutral loss similarity calculators for spectrum comparison and mirror plot generation) — https://github.com/bittremieux/cosine_neutral_loss
- **spectrum_utils** (Utility library for loading, processing, and manipulating MSMS spectra objects (MsmsSpectrum class) from USI identifiers or local data) — https://github.com/bittremieux/spectrum_utils

## Examples

```
import spectrum_utils.spectrum as sus; import plot; usi1="mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840"; usi2="mzspec:MSV000086109:BD5_dil2x_BD5_01_57213:scan:760"; spectrum1=sus.MsmsSpectrum.from_usi(usi1); spectrum2=sus.MsmsSpectrum.from_usi(usi2); plot.plot_mirror(spectrum1, spectrum2, "modified_cosine", "output.png")
```

## Evaluation signals

- Top-ranked library spectra correspond to known structural analogs or compounds with identical or very similar fragmentation patterns (visual inspection of mirror plots).
- Similarity scores are in expected range (0–1 for normalized measures) and show clear separation between true matches and unrelated spectra.
- Retrieval ranking is consistent across multiple query spectra from the same compound class or with the same precursor ion.
- Modified cosine similarity ranks matches with peak m/z shifts (due to neutral losses) higher than standard cosine when such shifts are genuine fragmentation artifacts.
- Neutral loss similarity identifies matches where characteristic neutral losses (e.g., loss of water, CO2) are preserved across query and library spectra.

## Limitations

- Similarity scores depend heavily on spectral quality and preprocessing (removal of precursor peaks, m/z range selection, intensity normalization); poor-quality spectra will rank lower even if structurally related.
- Modified cosine similarity introduces a free parameter (fragment m/z tolerance) that must be tuned for the mass spectrometer's resolution; different settings produce different rankings.
- Neutral loss similarity is most effective for compound classes with well-defined, reproducible neutral losses; spectra from diverse compound classes may show ambiguous neutral loss patterns.
- Large libraries (thousands of spectra) require efficient computational implementation; naive pairwise scoring can be slow; pre-filtering by precursor m/z or ion mode is recommended.
- The skill assumes library spectra are from the same ionization mode and collision energy as the query spectrum; cross-mode or cross-energy comparisons may produce uninformative low scores.

## Evidence

- [intro] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [readme] Cosine similarity, Modified cosine similarity, Neutral loss similarity are implemented measures: "Similarity measures that are currently implemented are: - Cosine similarity - Modified cosine similarity - Neutral loss similarity"
- [readme] Method to generate ranked comparisons with mirror plots: "Code example to create mirror plots using different similarity measures: ... for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"),"
- [readme] Spectrum preprocessing workflow for library comparison: "spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da")"
- [readme] Original cosine similarity reference: "Stein, S. E. & Scott, D. R. Optimization and testing of mass spectral library search algorithms for compound identification. Journal of the American Society for Mass Spectrometry 5, 859–866 (1994)"
