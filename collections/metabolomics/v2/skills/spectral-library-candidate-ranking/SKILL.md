---
name: spectral-library-candidate-ranking
description: Use when after MS2Deepscore has selected the top 2000 candidate spectra from a library based on spectral similarity, and you need to re-rank these candidates to surface the single match (either exact or analogue) rather than rely on raw spectral similarity alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3371
  tools:
  - MS2Query
  - MS2Deepscore
  - Python (pytest, setuptools)
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-candidate-ranking

## Summary

Rank MS/MS library candidate matches by combining structural similarity (InChIKey score) and spectral neighbourhood density into a unified score using machine learning. This skill is essential when a library search produces multiple candidate spectra and you need to identify the most reliable match—both for exact matches and structural analogues—by distinguishing true positives from false positives.

## When to use

After MS2Deepscore has selected the top 2000 candidate spectra from a library based on spectral similarity, and you need to re-rank these candidates to surface the single best match (either exact or analogue) rather than rely on raw spectral similarity alone. Apply this skill when your query spectrum has multiple plausible library candidates and you require a confidence score (0–1 range) to filter unreliable hits.

## When NOT to use

- Query spectrum is already a library spectrum (no re-ranking needed).
- Library spectra lack InChIKey or structural annotations; the model requires these metadata to compute InChIKey scores.
- You need all candidate matches ranked, not filtered by confidence—the skill deliberately discards low-scoring hits rather than passing through exhaustive rankings.

## Inputs

- top 2000 candidate spectra from library (ranked by MS2Deepscore similarity)
- query MS/MS spectrum
- library spectra with InChIKey annotations and pre-computed embeddings
- candidate match metadata (match IDs, precursor m/z, InChIKey layers)

## Outputs

- ranked candidate list with ms2query_model_prediction scores (0–1 range)
- single best-match library spectrum per query
- precursor m/z difference for each candidate
- molecular class estimates for top matches
- CSV results file with complete metadata

## How to apply

The MS2Query random forest model combines five features—including InChIKey score (average structural similarity across matched InChIKey layers) and neighbourhood score (density and proximity of similar candidates in spectral feature space)—to re-rank the top 2000 MS2Deepscore candidates. For each candidate, the model predicts a match confidence score between 0 and 1. Retain only candidates exceeding your reliability threshold: scores > 0.7 indicate high-confidence exact matches or analogues; 0.6–0.7 require caution; scores < 0.6 should generally be discarded. Use precursor m/z difference to separate exact matches from analogues if needed. The algorithm performs no precursor m/z prefiltering, allowing true analogues with shifted precursor masses to be ranked appropriately.

## Related tools

- **MS2Query** (orchestrates candidate ranking via random forest model combining InChIKey and neighbourhood scores; implements the complete re-ranking workflow) — https://github.com/iomega/ms2query
- **MS2Deepscore** (pre-filters library to top 2000 candidates via deep learning spectral similarity; inputs to the ranking step)
- **Python (pytest, setuptools)** (validates output record structure, score ranges, and end-to-end ranking correctness via unit tests)

## Examples

```
from ms2query.run_ms2query import run_complete_folder; from ms2query.ms2library import create_library_object_from_one_dir; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- Output CSV contains ms2query_model_prediction column with all scores in [0, 1] range with no missing or out-of-range values.
- Each query spectrum produces exactly one top-ranked match; verify no queries have tied scores or missing best matches.
- InChIKey score and neighbourhood score are both present and contribute meaningfully to the final prediction (inspect feature importance or model weights).
- Threshold validation: candidates with score > 0.7 should yield high manual curation accuracy; scores 0.6–0.7 show mixed utility; scores < 0.6 show predominantly false positives (via spot-check or benchmarking against known standards like Cosine Score).
- Precursor m/z differences correctly distinguish exact matches (Δ ≈ 0) from analogues; verify this column is populated and used for post-hoc filtering if needed.

## Limitations

- MS2Query does not perform peak picking or clustering; if your input contains many redundant MS/MS spectra per feature, pre-process with MZmine or equivalent to avoid inflated computational cost and ambiguous results.
- The model was trained on the GNPS library (2021-12-15 snapshot); performance on compounds outside GNPS or with unusual ionization states may degrade.
- No strict minimum confidence threshold is provided in the literature; threshold selection (0.6, 0.7, or higher) depends on your precision–recall tradeoff and research goal; generic guidance ('> 0.7') may not suit all applications.
- Neighbourhood score depends on the density and similarity of nearby candidates in the pre-selected top 2000; sparse regions of chemical space may produce unreliable neighbourhood scores.

## Evidence

- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [other] Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers.: "Compute average InChIKey score for each candidate by aggregating structural similarity metrics across matched InChIKey layers."
- [other] Compute neighbourhood score for each candidate by evaluating the density and proximity of similar candidates in the spectral feature space.: "Compute neighbourhood score for each candidate by evaluating the density and proximity of similar candidates in the spectral feature space."
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue.: "This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1."
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be"
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference."
