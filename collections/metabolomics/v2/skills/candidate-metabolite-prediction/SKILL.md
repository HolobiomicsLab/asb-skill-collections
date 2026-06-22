---
name: candidate-metabolite-prediction
description: Use when you have an unknown compound's mass spectrum (m/z peaks and intensities) in positive or negative ion mode and need to identify candidate metabolites from a structure database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - DeepMASS2
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
---

# candidate-metabolite-prediction

## Summary

Predict structurally related metabolites for unknown compounds by encoding mass spectra into semantic representations and ranking candidates from a reference database using deep-learning-based similarity scoring. This enables prioritization of molecular structure database candidates by considering chemical space context.

## When to use

Apply this skill when you have an unknown compound's mass spectrum (m/z peaks and intensities) in positive or negative ion mode and need to identify candidate metabolites from a structure database. Use it when structural relatedness and chemical space proximity are more informative than exact database matching, or when the unknown compound is not in your reference library but structurally similar compounds are.

## When NOT to use

- Input mass spectrum has missing or incorrect ion mode metadata — DeepMASS2 requires explicit IONMODE tag to select the correct model.
- Target is exact metabolite identification and compound is already in the reference library — direct database lookup or deterministic matching is more appropriate.
- Input spectra are from incompatible ionization methods or mass spectrometry platforms not represented in the training data (e.g., very low resolution or exotic MS/MS fragmentation schemes).

## Inputs

- mass spectrum file (.mgf format with PRECURSOR_MZ and IONMODE metadata tags)
- m/z peaks and intensities array
- precursor m/z value (float)
- ion mode polarity (positive or negative)
- optional: molecular formula string

## Outputs

- ranked candidate metabolite list with similarity scores (CSV format)
- metabolite identifiers and structures from reference database
- cosine similarity scores per candidate (0–1 range)
- structurally related metabolites ordered by descending similarity

## How to apply

Load the unknown compound's mass spectral data (m/z peaks and intensities) along with required metadata: precursor m/z and ion mode (positive or negative). Encode the mass spectrum into a semantic representation using DeepMASS2's deep-learning model (Ms2Vec) trained on mass spectral language. Compute semantic similarity scores between the unknown spectrum's encoding and a reference database of known metabolite spectra using cosine similarity. Rank candidate metabolites by similarity score in descending order. Filter and return top-ranked candidates, optionally constraining by molecular formula if available to improve chemical space accuracy. The ranking leverages the model's learned representation of mass spectral fragmentation patterns to identify structurally related compounds.

## Related tools

- **DeepMASS2** (Deep-learning model for encoding mass spectra into semantic representations and computing similarity scores; applies Ms2Vec embedding and similarity search against reference library) — https://github.com/hcji/DeepMASS2_GUI

## Examples

```
python DeepMASS2.py # with input .mgf file containing PRECURSOR_MZ=517.22098, IONMODE=positive, COMPOUND_NAME=challenge_0
```

## Evaluation signals

- Output CSV file contains ranked candidate metabolites with similarity scores in descending order (verify top score ≥ second score).
- Similarity scores fall within 0–1 range (cosine similarity bounds); inspect for nonsensical scores outside this range.
- Returned candidates contain metadata fields expected from the reference database (name, formula, structure, precursor m/z).
- If molecular formula is provided as input, verify output candidates respect the formula constraint and show improved ranking accuracy.
- Manual inspection: verify top-ranked candidate structures are chemically plausible (same functional groups, similar molecular weight, similar fragmentation logic to unknown spectrum).

## Limitations

- Model is trained on GNPS (Global Natural Products Social Molecular Networking) spectra; accuracy degrades for spectra from metabolites outside the natural products chemical space.
- Requires precursor m/z and ion mode metadata; missing tags will cause incorrect output file naming or model selection.
- No changelog available in repository; unclear which model versions correspond to which reference library updates.
- Distributed search feature (mentioned as added 04/2025) requires separate setup and may have undocumented requirements.
- Performance depends on quality and completeness of the reference database; incomplete or outdated DeepMassStructureDB will reduce candidate diversity.

## Evidence

- [intro] Deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language enables prediction of structurally related metabolites for unknown compounds: "Deep-learning based metabolite annotation via semantic similarity analysis of mass spectral language enables prediction of structurally related metabolites for the unknown"
- [intro] Chemical space context improves ranking and interpretation: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [other] Workflow: encode, compute similarity, rank, filter: "Encode the mass spectrum into a semantic representation using the DeepMASS2 deep-learning model trained on mass spectral language. 3. Compute semantic similarity scores between the unknown spectrum's"
- [readme] Mandatory metadata requirements for correct operation: "Precursor m/z - Required. This tag specifies the precursor ion mass-to-charge ratio. Ion Mode - Required. This specifies the polarity of the data, ensuring DeepMASS2 utilizes the correct"
- [readme] Molecular formula improves ranking accuracy through chemical space constraint: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites."
