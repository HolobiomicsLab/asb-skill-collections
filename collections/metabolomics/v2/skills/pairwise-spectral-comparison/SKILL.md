---
name: pairwise-spectral-comparison
description: Use when you have a collection of preprocessed mass spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to quantify similarity relationships across all pairs—for instance, to identify redundant spectra in a library, cluster related compounds, or perform spectral library searches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - Python
  - Spec2Vec
  - MS2DeepScore
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pairwise-spectral-comparison

## Summary

Compute similarity scores between all pairs of mass spectra using matchms' built-in similarity measures (Cosine, molecular fingerprint-based, or metadata-related assessments). This skill enables large-scale spectral comparisons and is essential for identifying related or duplicate spectra in spectral libraries.

## When to use

Apply this skill when you have a collection of preprocessed mass spectra (in mzML, mzXML, msp, MGF, or JSON format) and need to quantify similarity relationships across all pairs—for instance, to identify redundant spectra in a library, cluster related compounds, or perform spectral library searches.

## When NOT to use

- Input spectra are not preprocessed or peak-filtered; conduct basic peak filtering and metadata cleaning first.
- You require only single-query-to-library searches rather than all-pairs comparisons; use targeted library search methods instead.
- Spectra are in unsupported formats (not mzML, mzXML, msp, MGF, or JSON); convert or reformat first.

## Inputs

- Preprocessed mass spectra collection (mzML, mzXML, msp, MGF, or JSON format)
- Spectrum metadata (if using metadata-related similarity measures)
- Selected similarity measure (Cosine, fingerprint-based, or metadata-based)

## Outputs

- Pairwise similarity scores matrix (CSV or pickle format)
- Spectrum identifiers as row and column labels
- Structured scores output suitable for filtering and clustering

## How to apply

Load preprocessed spectra into matchms from a supported file format. Select an appropriate similarity measure: Cosine-based scores for peak-overlap similarity, molecular fingerprint-based comparisons for structural relationships, or metadata-related assessments for compound attribute matching. Apply the chosen measure to all spectrum pairs to generate a pairwise similarity scores matrix. Construct a structured output (CSV or pickle) with spectrum identifiers as row and column labels to enable downstream filtering, clustering, or search operations. The choice of similarity measure should align with your research question: Cosine similarity is computationally efficient and suitable for initial pre-selection of candidates, while fingerprint-based measures capture deeper structural similarity.

## Related tools

- **matchms** (Core library implementing pairwise similarity measures (Cosine, fingerprint-based, metadata) and scores matrix output) — https://github.com/matchms/matchms
- **Python** (Runtime environment for executing matchms workflows and manipulating similarity scores matrices)
- **Spec2Vec** (Optional extension for advanced spectrum similarity measures tailored for matchms) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional extension for deep learning-based spectrum similarity measures integrated with matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import Spectrum, Cosine
from matchms.importing import load_from_msp
spectra = list(load_from_msp('spectra.msp'))
similarity_measure = Cosine()
scores = [[similarity_measure(spectra[i], spectra[j]).score for j in range(len(spectra))] for i in range(len(spectra))]
import pandas as pd
df = pd.DataFrame(scores, index=[s.metadata['spectrum_id'] for s in spectra], columns=[s.metadata['spectrum_id'] for s in spectra])
df.to_csv('pairwise_similarity_scores.csv')
```

## Evaluation signals

- Scores matrix dimensions match the number of input spectra (n × n symmetry).
- Scores are bounded within expected range (e.g., 0–1 for normalized Cosine or fingerprint similarity).
- Diagonal elements equal expected self-similarity (typically 1.0 for normalized measures).
- Output file is present in the named location and matches the specified format (CSV or pickle).
- Spot-checks of known spectral pairs (e.g., duplicate or highly related spectra) show high similarity scores, while unrelated pairs show low scores.

## Limitations

- Computing all-pairs scores for very large spectral libraries (several hundred thousand spectra) requires sparse handling of scores and efficient similarity measures to avoid memory exhaustion.
- Choice of similarity measure significantly impacts interpretation: Cosine similarity captures peak overlap but may miss structural similarity; fingerprint-based measures are computationally more expensive but capture deeper compound relationships.
- Metadata-related similarity measures depend on data quality and completeness of metadata fields; incomplete or noisy metadata may yield uninformative scores.
- Preprocessing quality directly affects results; poorly filtered peaks or incorrect metadata cleaning will propagate into the similarity matrix.

## Evidence

- [other] Apply the cosine similarity measure to compute pairwise scores between all spectrum pairs.: "Apply the cosine similarity measure to compute pairwise scores between all spectrum pairs"
- [other] Matchms applies molecular fingerprint-based comparisons as one of several pairwise similarity measures available for comparing extensive amounts of spectra.: "Matchms implements molecular fingerprint-based comparisons as one of several pairwise similarity measures available for comparing extensive amounts of spectra"
- [readme] Its ability to apply various pairwise similarity measures encompasses not only common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related assessments.: "its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra. This encompasses not only common Cosine-related scores but also molecular fingerprint-based"
- [other] Load preprocessed spectra from the input file using matchms and construct a scores matrix with spectrum identifiers as row and column labels.: "Load preprocessed spectra from the input file (peak-filtered spectra or reference spectral library) using matchms. Apply the cosine similarity measure to compute pairwise scores between all spectrum"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats.: "Matchms enhances efficiency by using faster similarity measures for initial pre-selection and supports storing results in sparse data formats"
