---
name: lipid-identification-scoring
description: Use when after peak picking (MZmine, XCMS, MS-DIAL, or Compound Discoverer
  output) and candidate retrieval, when you have experimental fragment m/z values
  and multiple candidate lipid species from the in-silico library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive orbitrap UHPLC-HRMS/MS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values
  with simulated library m/z values
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS,
  MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-identification-scoring

## Summary

Score and rank candidate lipid identifications by comparing experimental fragment m/z values against simulated library m/z values, using matching metrics such as fragment count and intensity correlation to assign confidence levels. This skill is essential for converting raw fragment matches into ranked, annotated lipid assignments in untargeted lipidomics workflows.

## When to use

Apply this skill after peak picking (MZmine, XCMS, MS-DIAL, or Compound Discoverer output) and candidate retrieval, when you have experimental fragment m/z values and multiple candidate lipid species from the in-silico library. Use it when you need to disambiguate between competing identifications and assign a single lipid ID with confidence to each feature.

## When NOT to use

- Input is already a fully annotated feature table with high-confidence lipid assignments — scoring is redundant.
- Mass spectrometry data are from Waters instruments — LipidMatch does not currently support Waters files.
- Experimental data lack reliable fragmentation spectra (e.g., survey scan only, no MS/MS data) — candidate scoring requires fragment m/z matching.

## Inputs

- Experimental peak list with m/z, retention time, intensity, and fragment m/z values
- In-silico fragmentation library with 500,000+ lipid species across 60+ lipid types
- Candidate lipid species set retrieved by parent ion m/z matching

## Outputs

- Ranked list of candidate lipid identifications with matching scores for each experimental peak
- Annotated feature table with assigned lipid identifications and confidence levels
- Scoring metrics (number of matched fragments, intensity correlation, or similar) per assignment

## How to apply

For each experimental peak with its observed fragment m/z values, match fragments against simulated library fragment m/z values for all candidate lipid species within a specified mass tolerance threshold. Calculate a matching score for each candidate based on the number of matched fragments, intensity correlation between experimental and simulated fragments, or a similar metric. Rank candidates by matching score in descending order. Assign the top-ranked candidate as the lipid identification and attach a confidence level (derived from the score magnitude or the gap between top and second-ranked candidates). Output the annotated feature table with assigned lipid identifications and scores. The scoring logic should penalize candidates with few matches and reward those with high intensity agreement.

## Related tools

- **LipidMatch** (Primary scoring and ranking engine; implements fragment m/z matching and matching score calculation against in-silico lipid libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Upstream peak picking and feature extraction to generate experimental peak list and fragment m/z values)
- **XCMS** (Upstream peak picking and feature extraction to generate experimental peak list and fragment m/z values)
- **MS-DIAL** (Upstream peak picking and feature extraction to generate experimental peak list and fragment m/z values)
- **Compound Discoverer** (Upstream peak picking and feature extraction to generate experimental peak list and fragment m/z values)
- **Q-Exactive orbitrap UHPLC-HRMS/MS** (Reference instrument for validation of LipidMatch scoring; supports targeted, ddMS2-topN, and AIF approaches)

## Evaluation signals

- Verify that all experimental peaks have been assigned a lipid identification and a matching score.
- Check that top-ranked candidates have substantially higher scores than lower-ranked candidates (e.g., second-ranked score is ≤80% of first-ranked), indicating clear discrimination.
- Confirm that the number of matched fragments and intensity correlation values fall within expected ranges for authentic identifications (e.g., ≥3 matched fragments, cosine similarity >0.6).
- Cross-validate a subset of high-confidence assignments (top-ranked, highest scores) against orthogonal methods or retention time expectations to ensure scoring is not biased toward spurious matches.
- Ensure that no experimental peak is left unassigned unless explicitly filtered by score threshold, and that filtering thresholds are documented and justified.

## Limitations

- LipidMatch currently does not support Waters instrument files, limiting applicability to Q-Exactive, Q-TOF (Agilent, Bruker, SCIEX), and compatible formats.
- Scoring relies on mass tolerance thresholds for fragment m/z matching; overly relaxed thresholds may inflate false-positive scores, while overly strict thresholds may miss valid identifications due to instrument mass accuracy drift.
- Intensity correlation metrics for scoring assume that simulated fragment intensities are accurate predictors of experimental relative abundances; discrepancies may arise from instrument-dependent ionization suppression or unexpected fragmentation patterns.
- Scoring does not account for retention time alignment; co-eluting isomers with identical or very similar fragment patterns may receive ambiguous or tied scores.

## Evidence

- [intro] Fragment matching and scoring mechanism: "For each experimental peak, retrieve candidate lipid species from the library based on parent ion m/z with specified mass tolerance. Match experimental fragment m/z values against simulated library"
- [readme] Library and instrument validation: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [readme] Validation across instrument platforms: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Waters file limitation: "The software does not currently support Waters files"
