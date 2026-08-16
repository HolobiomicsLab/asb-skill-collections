---
name: deep-learning-spectral-language-model
description: Use when when you have an unknown compound's mass spectrum (m/z peaks and intensities in .mgf or equivalent format with mandatory PRECURSOR_MZ and IONMODE tags) and need to identify structurally related metabolites from a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - DeepMASS2
  techniques:
  - NMR
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-spectral-language-model

## Summary

Encode mass spectra into semantic vector representations using a deep-learning model trained on mass spectral language, then compute cosine similarity scores against reference metabolite databases to rank and predict structurally related metabolites for unknown compounds. This approach leverages chemical space to improve candidate ranking and annotation confidence.

## When to use

When you have an unknown compound's mass spectrum (m/z peaks and intensities in .mgf or equivalent format with mandatory PRECURSOR_MZ and IONMODE tags) and need to identify structurally related metabolites from a reference database. Use this skill specifically when semantic similarity in chemical space—rather than exact mass matching or spectral similarity alone—is expected to improve ranking of candidate metabolites.

## When NOT to use

- When your input spectrum lacks mandatory precursor m/z or ion mode metadata; DeepMASS2 requires these to select the correct model and filter candidates.
- When the compound is outside the chemical space covered by the reference databases (e.g., synthetic polymers, organometallics); the model cannot reliably rank candidates it has never encountered during training.
- When you need deterministic, threshold-based spectral matching (e.g., for regulatory compliance) rather than probabilistic semantic similarity; deep-learning predictions carry inherent uncertainty.

## Inputs

- Mass spectrum data (m/z peaks and intensities)
- Precursor m/z value (mandatory)
- Ion mode: 'positive' or 'negative' (mandatory)
- Compound name or identifier (recommended for output naming)
- Molecular formula (optional, improves ranking accuracy)
- .mgf file or compatible format with required metadata tags

## Outputs

- Ranked list of predicted structurally related metabolites
- Cosine similarity scores for each candidate
- Output CSV file with results named after the compound (if COMPOUND_NAME provided)
- Semantic vector encoding of the unknown spectrum

## How to apply

Load the unknown compound's mass spectrum including m/z peaks, intensities, precursor m/z, and ion mode (positive or negative). Pass the spectrum through the DeepMASS2 deep-learning model to encode it into a semantic vector representation learned from mass spectral language. Compute cosine similarity scores between the unknown spectrum's encoding and a reference database of known metabolite spectra (either positive or negative mode as appropriate). Rank candidate metabolites by similarity score in descending order. Optionally constrain the chemical space using the molecular formula (if available) to improve ranking accuracy. Return the top-ranked structurally related metabolites with their corresponding similarity scores as predictions.

## Related tools

- **DeepMASS2** (Deep-learning model and semantic similarity engine that encodes mass spectra into learned vector representations and computes cosine similarity against reference libraries for metabolite annotation) — https://github.com/hcji/DeepMASS2_GUI

## Examples

```
conda activate deepmass && python DeepMASS2.py  # Specify input .mgf with PRECURSOR_MZ, IONMODE=positive, and optional COMPOUND_NAME and FORMULA tags via the GUI or batch processing
```

## Evaluation signals

- Similarity scores are in the range [0, 1] (cosine similarity); scores close to 1 indicate high semantic overlap with reference spectra.
- Top-ranked candidates should have known chemical structures consistent with the precursor m/z and ion mode; verify by cross-referencing against external databases (e.g., GNPS, PubChem).
- When molecular formula is provided as optional input, verify that top-ranked candidates respect the molecular weight constraint derived from the formula.
- Output CSV contains a non-empty ranked list; empty results indicate either the reference library is missing or the spectrum's semantic encoding is very distant from all references.
- Reproducibility check: re-running the same spectrum with the same model version should produce identical similarity scores and rank order.

## Limitations

- Model performance depends entirely on the breadth and quality of the training data (GNPS spectra); unknown metabolites from underrepresented chemical classes may be ranked poorly.
- Semantic similarity does not guarantee correct annotation; top-ranked candidates still require orthogonal validation (e.g., NMR, chromatography, or authentic standard comparison).
- Ion mode must be correctly specified; using the wrong mode (positive vs. negative) will invoke the incorrect deep-learning model and produce meaningless predictions.
- The tool requires pre-downloaded reference indices and model weights; these are large files and must be placed in specific data and model folders as documented in the README installation steps.

## Evidence

- [intro] Encode mass spectrum and compute similarity: "Encode the mass spectrum into a semantic representation using the DeepMASS2 deep-learning model trained on mass spectral language. 3. Compute semantic similarity scores between the unknown spectrum's"
- [intro] Rank and filter candidates by similarity: "Rank candidate metabolites by similarity score in descending order. 5. Filter and return the top-ranked structurally related metabolites as predictions with their corresponding similarity scores."
- [intro] Chemical space improves ranking: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [readme] Mandatory metadata tags required: "To ensure DeepMASS2 accurately identifies metabolites and correctly names output files, your input data must include specific metadata tags. Precursor m/z - Required. Ion Mode - Required. This"
- [readme] Molecular formula constrains chemical space: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites."
