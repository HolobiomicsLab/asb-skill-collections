---
name: chemical-space-structure-ranking
description: Use when you have an unknown compound's mass spectrum (m/z peaks and
  intensities in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3474
  tools:
  - DeepMASS2
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.05.30.596727v2
  title: DeepMASS
evidence_spans:
- DeepMASS2 is a cross-platform GUI software tool, which enables deep-learning based
  metabolite annotation
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-space-structure-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank candidate metabolites from a structural database by computing semantic similarity scores between an unknown compound's mass spectrum encoding and a reference database of known metabolite spectra, using chemical space constraints to filter and prioritize structurally related candidates for annotation.

## When to use

You have an unknown compound's mass spectrum (m/z peaks and intensities in .mgf format with mandatory PRECURSOR_MZ and IONMODE tags) and need to identify likely metabolite structures by leveraging semantic similarity in mass spectral language rather than classical spectrum-to-spectrum matching. Use this skill when the goal is to narrow a molecular structure database search space by ranking candidates by predicted structural relatedness in chemical space.

## When NOT to use

- Input spectrum lacks mandatory PRECURSOR_MZ or IONMODE metadata; preprocessing or reformatting is required first.
- Unknown spectrum is from a different ion mode than the chosen reference library (e.g., positive spectrum searched against negative-mode model); use the mode-matched model or re-acquire data.
- The reference database (DeepMassStructureDB or indexed spectra) is outdated or missing; workflow cannot proceed without populated reference libraries.

## Inputs

- mass spectrum data in .mgf format with mandatory PRECURSOR_MZ and IONMODE metadata tags
- optional COMPOUND_NAME tag for output file naming
- optional FORMULA tag for chemical space filtering
- ion mode specification (positive or negative)
- reference spectrum database with indexed semantic encodings (references_spectrums_positive.pickle or references_spectrums_negative.pickle)
- reference structure database (DeepMassStructureDB-v1.1.csv)

## Outputs

- ranked list of candidate metabolites with semantic similarity scores
- .csv export file with metabolite candidates, similarity scores, and structural information
- chemical space coordinates of top-ranked candidates relative to the unknown compound

## How to apply

Load the unknown spectrum's m/z and intensity data and encode it into a semantic representation using a trained deep-learning model (Ms2Vec) that has learned mass spectral language patterns from reference libraries (GNPS). Compute cosine similarity scores between this semantic encoding and the encodings of all reference spectra indexed in the database (references_index_positive_spec2vec.bin or references_index_negative_spec2vec.bin, depending on ion mode). Optionally constrain the chemical space by filtering candidates using the precursor m/z tolerance and molecular formula (if provided) to reduce false positives. Rank candidates by similarity score in descending order and return the top-ranked metabolites with their corresponding similarity scores and structural information from DeepMassStructureDB. The ranking should prioritize high semantic similarity while respecting chemical space boundaries (mass and formula constraints).

## Related tools

- **DeepMASS2** (Core GUI software tool that implements deep-learning semantic similarity encoding of mass spectra and ranking of structurally related metabolite candidates via Ms2Vec embeddings and reference database indexing) — https://github.com/hcji/DeepMASS2_GUI

## Examples

```
python DeepMASS2.py  # loads .mgf with PRECURSOR_MZ=517.22098, IONMODE=positive, FORMULA=C25H38O9; encodes spectrum via Ms2Vec; computes cosine similarity against references_index_positive_spec2vec.bin; outputs ranked metabolites to challenge_0.csv sorted by descending similarity score.
```

## Evaluation signals

- Top-ranked metabolite candidates should have cosine similarity scores > 0.7 (or threshold appropriate to ion mode) and chemical space coordinates (precursor m/z and molecular formula) consistent with the unknown spectrum's metadata.
- Output .csv file contains expected columns (metabolite name, similarity score, structure, database ID) and matches COMPOUND_NAME tag if provided.
- Ranked candidates exhibit decreasing similarity scores in descending order with no duplicate entries.
- If molecular formula was provided as filter, all returned candidates should satisfy formula constraint; if not, precursor m/z should fall within a reasonable mass tolerance window (e.g., ±5–10 ppm depending on instrument).
- Semantic embeddings used for similarity computation match the ion mode of input spectrum (positive model for IONMODE=positive, negative model for IONMODE=negative).

## Limitations

- Ranking depends critically on quality and completeness of reference spectrum database; sparse or biased reference libraries will produce suboptimal rankings.
- Semantic similarity in mass spectral language does not guarantee structural identity; candidates should be validated by orthogonal methods (e.g., retention time, fragment ion interpretation, or standards).
- Chemical space filtering using molecular formula requires accurate mass spectrometry data and correct formula input; missing or incorrect formula tags may bypass this constraint.
- No changelog or versioning documentation is available; unclear how model updates or reference database changes affect reproducibility across time.

## Evidence

- [readme] Deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language enables prediction of structurally related metabolites: "enables deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language. This approach enables the prediction of structurally related metabolites for the unknown"
- [readme] Structurally related metabolites from chemical space provide valuable information about the potential location of unknown metabolites and assist in ranking candidates from molecular structure databases: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [other] Encode mass spectrum into semantic representation, compute similarity scores, and rank by similarity in descending order: "Encode the mass spectrum into a semantic representation using the DeepMASS2 deep-learning model trained on mass spectral language. 3. Compute semantic similarity scores between the unknown spectrum's"
- [readme] Precursor m/z and ion mode are mandatory metadata tags for DeepMASS2 input: "Precursor m/z - Required. This tag specifies the precursor ion mass-to-charge ratio. 2. Ion Mode - Required. This specifies the polarity of the data, ensuring DeepMASS2 utilizes the correct"
- [readme] Molecular formula helps constrain chemical space and improves ranking accuracy of structurally related metabolites: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites."
