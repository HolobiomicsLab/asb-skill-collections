---
name: species-candidate-ranking-from-spectral-alignment
description: Use when you have an unknown sample spectrum (m/z peaks and intensities from DI-MS, ASAP-MS, or other high-throughput mass spectrometry modalities) and a reference species database of known spectra, and you need to identify the most likely species or authenticate the sample by ranking how well each.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  techniques:
  - direct-infusion-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# species-candidate-ranking-from-spectral-alignment

## Summary

Ranks reference species candidates by computing alignment-based similarity scores between an unknown mass spectrometry sample spectrum and a reference database of known spectra. This skill enables direct discrimination of unknown sample species through quantitative spectral matching, producing a ranked candidate list with match scores and visual outputs.

## When to use

You have an unknown sample spectrum (m/z peaks and intensities from DI-MS, ASAP-MS, or other high-throughput mass spectrometry modalities) and a reference species database of known spectra, and you need to identify the most likely species or authenticate the sample by ranking how well each reference matches the unknown.

## When NOT to use

- Raw, unpreprocessed mass spectrometry data without peak identification or intensity normalization — pre-processing must occur first.
- Reference database is empty, incomplete, or does not contain the target species.
- Input spectrum has insufficient m/z peaks or very low signal-to-noise ratio, making reliable alignment impossible.

## Inputs

- unknown sample spectrum (m/z peaks and intensities)
- reference species database (collection of known spectra with species identifiers and accession numbers)

## Outputs

- ranked candidate list (tabular format: CSV or TSV with rank, species, reference_id, similarity_score)
- visual outputs (species discrimination plots)

## How to apply

Load the preprocessed unknown sample spectrum (m/z peaks and intensities) and the reference species database containing known spectra. For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric such as cosine similarity or Euclidean distance on aligned m/z features. Rank all reference entries by descending similarity score. Output the full scored candidate list with columns for rank, species name, reference accession identifier, and similarity score. The workflow integrates data pre-processing (peak identification and normalization) prior to alignment to ensure consistent feature comparison across spectra.

## Related tools

- **RapidMass** (Integrates data pre-processing, analysis, and database search scoring to perform spectral alignment and candidate ranking with automatic MS peak identification and visual outputs) — https://github.com/Katherine00689/RapidMass

## Evaluation signals

- Output candidate list is ranked in descending order by similarity score with no gaps or inconsistencies in the ranking.
- All reference entries in the database receive a similarity score; no entries are missing or duplicated in the output.
- Similarity scores fall within a valid range (e.g., 0–1 for normalized metrics or −1 to +1 for correlation-based scores) and are internally consistent.
- Species names and accession identifiers in the output match exactly with entries in the reference database.
- Visual outputs correctly display the unknown spectrum overlaid or compared against top-ranked reference spectra, with m/z features aligned.

## Limitations

- Performance depends on the completeness and quality of the reference database; if the true species is absent or poorly represented, ranking will be unreliable.
- Easily confused plant materials or closely related species may receive similar scores, reducing discrimination power; visual inspection of top candidates is recommended.
- The choice of distance/correlation metric (cosine similarity, Euclidean distance, etc.) affects ranking results; sensitivity to metric selection is not quantified in the article.
- Preprocessing steps (peak detection, intensity normalization, m/z alignment tolerance) must be consistently applied to both unknown and reference spectra to ensure valid comparison.

## Evidence

- [other] Load the preprocessed unknown sample spectrum (m/z peaks and intensities) and the reference species database containing known spectra.: "Load the preprocessed unknown sample spectrum (m/z peaks and intensities) and the reference species database containing known spectra."
- [other] For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric (e.g., cosine similarity or Euclidean distance on aligned m/z features).: "For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric (e.g., cosine similarity or Euclidean"
- [other] Rank all reference entries by descending score and output the full scored candidate list with species names, accession identifiers, and match scores.: "Rank all reference entries by descending score and output the full scored candidate list with species names, accession identifiers, and match scores."
- [other] Return results in a tabular format (CSV or TSV) with columns for rank, species, reference_id, and similarity_score.: "Return results in a tabular format (CSV or TSV) with columns for rank, species, reference_id, and similarity_score."
- [other] RapidMass integrates data pre-processing, analysis, and evaluation to enable direct discrimination of unknown sample species through database search algorithms that produce candidate scores with visual outputs.: "RapidMass integrates data pre-processing, analysis, and evaluation to enable direct discrimination of unknown sample species through database search algorithms that produce candidate scores with"
- [intro] RapidMass offers several database search algorithms to achieve unknown sample scoring: "RapidMass offers several database search algorithms to achieve unknown sample scoring"
- [intro] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
- [readme] This tool integrates data pre-processing, analysis, and evaluation, enabling direct discrimination of unknown sample species with intuitive visual outputs.: "This tool integrates data pre-processing, analysis, and evaluation, enabling direct discrimination of unknown sample species with intuitive visual outputs."
