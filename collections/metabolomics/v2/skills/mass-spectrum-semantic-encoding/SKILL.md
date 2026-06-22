---
name: mass-spectrum-semantic-encoding
description: Use when when you have an unknown compound's mass spectrum (m/z peaks and intensities in .mgf or equivalent format) and need to identify structurally related metabolites from a reference database by computing similarity in learned semantic space rather than direct spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0154
  tools:
  - DeepMASS2
  - Ms2Vec (neural embedding model)
derived_from:
- doi: 10.1101/2024.05.30.596727v2
  title: DeepMASS
evidence_spans:
- DeepMASS2 is a cross-platform GUI software tool, which enables deep-learning based metabolite annotation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmass_cq
    doi: 10.1101/2024.05.30.596727v2
    title: DeepMASS
  dedup_kept_from: coll_deepmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.05.30.596727v2
  all_source_dois:
  - 10.1101/2024.05.30.596727v2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-semantic-encoding

## Summary

Encode mass spectra into learned semantic vector representations using deep-learning models trained on mass spectral language, enabling similarity-based metabolite annotation and chemical space exploration for unknown compounds.

## When to use

When you have an unknown compound's mass spectrum (m/z peaks and intensities in .mgf or equivalent format) and need to identify structurally related metabolites from a reference database by computing similarity in learned semantic space rather than direct spectral matching. Use this skill when ranking candidates from molecular structure databases and want to leverage chemical space relationships.

## When NOT to use

- Input spectra are of very low quality or have fewer than ~5 informative fragments; the semantic model requires sufficient fragmentation signal to encode meaningful patterns.
- Metabolite is not represented in the reference library (references_spectrums_positive/negative.pickle); similarity ranking will not discover truly novel structural scaffolds.
- Ion mode (positive vs. negative) is unknown or misspecified; DeepMASS2 requires correct IONMODE tag to load the appropriate model and reference library.

## Inputs

- mass spectrum in .mgf format with mandatory PRECURSOR_MZ and IONMODE tags
- fragment peaks (m/z and intensity pairs)
- optional: COMPOUND_NAME tag for output naming
- optional: molecular formula (FORMULA tag) for chemical space constraint

## Outputs

- semantic vector encoding (fixed-dimensional embedding from Ms2Vec model)
- ranked list of candidate metabolites with cosine similarity scores
- .csv file with candidate metabolites, similarity scores, and chemical metadata

## How to apply

Load the unknown compound's mass spectral data (precursor m/z, ion mode, fragment peaks, intensities) into DeepMASS2. Pass the spectrum through the pre-trained deep-learning model (Ms2Vec; separate positive and negative mode models) to generate a fixed-dimensional semantic vector encoding. Compute cosine similarity between the unknown spectrum's encoding and a reference index of pre-computed encodings from known metabolites. Rank candidate metabolites by descending similarity score and optionally constrain by precursor m/z tolerance and molecular formula if available. The semantic encoding captures mass spectral language patterns learned from large GNPS datasets, so similarity reflects structural and fragmentation pattern relationships, not just peak overlap.

## Related tools

- **DeepMASS2** (Deep-learning model suite (Ms2Vec encoders and semantic similarity index) that transforms raw mass spectra into semantic vectors and ranks candidates) — https://github.com/hcji/DeepMASS2_GUI
- **Ms2Vec (neural embedding model)** (Pre-trained word2vec-like neural network that learns mass spectral language; separate models for positive and negative ion modes) — https://github.com/hcji/DeepMASS2_GUI

## Examples

```
python DeepMASS2.py with input .mgf containing PRECURSOR_MZ=517.22098, IONMODE=positive, COMPOUND_NAME=sample_001; output will be sample_001.csv with ranked metabolites and cosine similarity scores.
```

## Evaluation signals

- Similarity scores range between 0 and 1 (cosine similarity), and top candidates should have scores > 0.5 for reliable annotation; verify no NaN or out-of-range values.
- Returned candidate metabolites' precursor m/z values fall within chemical mass tolerance (typically ±5–10 ppm) of the input spectrum's PRECURSOR_MZ.
- If molecular formula is provided, verify all returned candidates match or are consistent with the input formula; semantic ranking should respect structural constraints.
- Output .csv file contains exactly one row per ranked candidate with non-null similarity score, candidate name, m/z, and formula; no duplicate rows.
- Reproducibility check: re-running the same spectrum should produce identical rankings and similarity scores (deterministic encoding and cosine distance).

## Limitations

- Performance depends heavily on reference library coverage; rare metabolites or novel scaffolds absent from GNPS may not be ranked highly.
- Semantic model is specific to fragmentation patterns in MS2 spectra; does not capture MS1-only information or adduct features beyond the precursor m/z tag.
- Ion mode must be correctly specified; mismatched IONMODE will invoke the wrong pre-trained model and reference library, leading to spurious rankings.
- No changelog documented in repository; version compatibility with input data formats and pre-computed reference indices is not formally tracked.

## Evidence

- [intro] DeepMASS2 performs deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language to predict structurally related metabolites: "DeepMASS2 performs deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language to predict structurally related metabolites"
- [other] Encode mass spectrum into semantic representation using the DeepMASS2 deep-learning model trained on mass spectral language: "Encode the mass spectrum into a semantic representation using the DeepMASS2 deep-learning model trained on mass spectral language"
- [other] Compute semantic similarity scores between unknown spectrum's encoding and reference database using cosine similarity: "Compute semantic similarity scores between the unknown spectrum's encoding and a reference database of known metabolite spectra using cosine similarity or equivalent distance metric"
- [readme] Ion Mode is required and specifies polarity of data, ensuring DeepMASS2 utilizes correct deep-learning model and reference libraries: "This specifies the polarity of the data, ensuring DeepMASS2 utilizes the correct deep-learning model (Positive vs. Negative) and reference libraries"
- [intro] Structurally related metabolites from chemical space provide valuable information about potential location and assist in ranking candidates: "these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
