---
name: unknown-sample-reference-comparison
description: Use when you have a preprocessed unknown sample spectrum (m/z peaks and
  intensities) from high-throughput mass spectrometry (DI-MS, ASAP-MS, or ambient
  ionization methods) and need to identify the species or authenticate a sample against
  a curated reference database of known spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3502
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  techniques:
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unknown-sample-reference-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign candidate species scores to unknown mass spectrometry samples by computing similarity metrics between preprocessed unknown spectra and a reference database of known species spectra. This skill enables automated species authentication through ranked candidate lists with match scores.

## When to use

You have a preprocessed unknown sample spectrum (m/z peaks and intensities) from high-throughput mass spectrometry (DI-MS, ASAP-MS, or ambient ionization methods) and need to identify the species or authenticate a sample against a curated reference database of known spectra. Apply this skill when the goal is to rank candidate matches rather than perform de novo identification.

## When NOT to use

- Reference database is absent, incomplete, or not appropriate for the sample type (e.g., plant reference database used for microbial unknowns).
- Unknown sample spectrum is raw or unpreprocessed; preprocessing (peak picking, normalization, m/z alignment) must precede database search.
- The goal is structural elucidation or compound annotation of novel unknowns; this skill ranks known species, not discovers new compounds.

## Inputs

- preprocessed unknown sample spectrum (m/z peaks and intensities)
- reference species database (known spectra with m/z features and intensities)
- species identifiers and accession numbers

## Outputs

- ranked candidate species list (CSV or TSV)
- columns: rank, species name, reference_id, similarity_score
- visual outputs for candidate discrimination

## How to apply

Load the preprocessed unknown sample spectrum and the reference species database containing known spectra with m/z features and intensities. For each reference spectrum in the database, compute a similarity score using a distance or correlation metric such as cosine similarity or Euclidean distance on aligned m/z features. Rank all reference entries by descending similarity score. Output the full scored candidate list with columns for rank, species name, reference identifier, and similarity score in tabular format (CSV or TSV). The scoring algorithm integrates automatic peak identification to focus the comparison on relevant m/z peaks, improving discrimination accuracy.

## Related tools

- **RapidMass** (integrates data pre-processing, analysis, and database search scoring; provides automatic peak identification and user-friendly visual interface for candidate ranking and species authentication) — github.com/Katherine00689/RapidMass

## Evaluation signals

- Output tabular format contains exactly five columns (rank, species, reference_id, similarity_score, and optionally accession details) with no missing values.
- Similarity scores are bounded within a valid metric range (e.g., [0, 1] for normalized cosine similarity or [0, ∞) for Euclidean distance) and monotonically decrease by rank.
- Known or positive control samples return the correct reference species in the top-ranked candidates (rank ≤ 5 for easily confused plant materials, per validation).
- Visual outputs (e.g., spectral overlay plots or heatmaps) clearly distinguish high-scoring matches from low-scoring candidates.
- All reference database entries are scored and ranked; no reference spectra are skipped or omitted from the candidate list.

## Limitations

- Performance depends on the quality, completeness, and relevance of the reference database; easily confused or morphologically similar species may produce ambiguous scores.
- Alignment of m/z features between unknown and reference spectra requires consistent preprocessing and calibration; instrument-specific variations (DI-MS vs. ASAP-MS vs. AI-MS) may affect score reliability.
- No changelog or version history documented; stability and reproducibility across software updates cannot be tracked.
- Similarity metrics (cosine similarity, Euclidean distance) are sensitive to peak intensity normalization and m/z tolerance; threshold choice for candidate acceptance is not specified in the article.

## Evidence

- [other] For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric (e.g., cosine similarity or Euclidean distance on aligned m/z features).: "For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric (e.g., cosine similarity or Euclidean"
- [other] RapidMass integrates data pre-processing, analysis, and evaluation to enable direct discrimination of unknown sample species through database search algorithms that produce candidate scores with visual outputs.: "integrates data pre-processing, analysis, and evaluation to enable direct discrimination of unknown sample species through database search algorithms that produce candidate scores with visual outputs"
- [other] Return results in a tabular format (CSV or TSV) with columns for rank, species, reference_id, and similarity_score.: "Return results in a tabular format (CSV or TSV) with columns for rank, species, reference_id, and similarity_score."
- [intro] RapidMass offers several database search algorithms to achieve unknown sample scoring.: "RapidMass offers several database search algorithms to achieve unknown sample scoring"
- [readme] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
