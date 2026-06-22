---
name: nps-classification-prediction
description: Use when you have an unknown mass spectrum from a suspicious analyte and need to determine whether it matches a known NPS or a derivative thereof. The analyte's mass spectrum is available in MSP or equivalent format, and you have a core drug structure to enumerate derivatives from.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3520
  tools:
  - PS2MS
  - NEIMS
  - DeepEI
  - PS2MS enumeration module
  - PS2MS drug detection module
  - rdkit
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  - build: coll_ps2ms_cq
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms_cq
schema_version: 0.2.0
---

# nps-classification-prediction

## Summary

Classify unknown mass spectrometry analytes as novel psychoactive substances (NPS) by comparing their mass spectral and chemical fingerprint signatures against a synthetic derivative database using integrated similarity scoring. This skill applies deep learning inference to detect emerging illicit drugs that traditional spectral libraries may not contain.

## When to use

You have an unknown mass spectrum from a suspicious analyte and need to determine whether it matches a known NPS or a derivative thereof. The analyte's mass spectrum is available in MSP or equivalent format, and you have a core drug structure to enumerate derivatives from. Use this skill when conventional database matching fails or when you need to screen for structural variants of a known illicit compound.

## When NOT to use

- The analyte's mass spectrum is of insufficient quality (low signal-to-noise, incomplete fragmentation pattern, or strong instrumental artifacts) — preprocessing and quality control must precede this skill.
- You do not have a plausible core drug structure to enumerate from; this skill is not suitable for de novo drug identification without a structural hypothesis.
- The compound is a known, cataloged substance already present in standard spectral libraries (NIST, Wiley, MassBank) — direct library search is more efficient and does not require model inference.

## Inputs

- mass spectrometry spectrum of unknown analyte (MSP format or equivalent)
- core drug structure (molecular structure file, e.g., SMILES or SDF)
- pre-trained NEIMS model weights
- pre-trained DeepEI model weights

## Outputs

- ranked list of candidate NPS identities (top ~100 compounds)
- integrated similarity scores (SMSF) for each candidate
- confidence scores or ranking positions for top hits
- classification metrics (accuracy, precision, recall, F1-score) when validated against reference outputs

## How to apply

First, enumerate a synthetic NPS database by substituting hydrogen atoms in the core drug structure with functional groups using the enumeration module. Second, use NEIMS (neural network electron ionization mass spectrometry predictor) to generate predicted mass spectra for all synthetic derivatives and DeepEI to compute chemical fingerprints for both the synthetic compounds and the unknown analyte. Third, merge the fingerprints into the database MSP files. Finally, run the drug detection module to compute integrated similarity scores (SMSF) between the unknown analyte's spectrum and fingerprint against each compound in the synthetic database, rank matches by similarity score, and validate that the top-ranked hit exceeds domain-relevant confidence thresholds. Classification metrics (accuracy, precision, recall, F1-score) should be computed against reference outputs from the paper or repository to confirm correct inference.

## Related tools

- **NEIMS** (predicts mass spectra for synthetic NPS derivatives in the enumeration database) — https://github.com/jhhung/PS2MS
- **DeepEI** (generates chemical fingerprints for unknown analytes and synthetic compounds; fingerprints are merged into MSP database for similarity matching) — https://github.com/jhhung/PS2MS
- **PS2MS enumeration module** (generates synthetic NPS database by substituting hydrogen atoms in core drug structure with functional groups) — https://github.com/jhhung/PS2MS
- **PS2MS drug detection module** (compares unknown analyte spectrum and fingerprint against synthetic database and computes integrated similarity scores (SMSF) to rank candidate NPS) — https://github.com/jhhung/PS2MS
- **rdkit** (required dependency for cheminformatics and molecular structure manipulation in enumeration and fingerprint steps)

## Evaluation signals

- Top-ranked candidate in the output list matches the true identity of the analyte when tested against reference datasets or known standards.
- Integrated similarity scores (SMSF) for correct candidate rank in the top percentile (typically top 5–10) of the full ranked list of ~100 compounds.
- Classification metrics (accuracy, precision, recall, F1-score) computed against reference predictions reported in the paper or repository fall within expected ranges (paper reports classification performance on test data).
- Unknown analyte's mass spectrum is faithfully reconstructed by summing the predicted spectrum of the top-ranked compound with typical instrumental noise and fragmentation variation; visual inspection of experimental vs. predicted spectra should show strong peak alignment.
- Fingerprint distance (Tanimoto or cosine similarity) between unknown analyte and top-ranked compound exceeds domain-relevant threshold (typically ≥ 0.7 for chemical fingerprint similarity in NPS screening).

## Limitations

- PS2MS is restricted to structural variants of a pre-selected core illicit drug; it cannot identify completely novel drug scaffolds not related to known compounds.
- The system's performance depends critically on the quality and completeness of the synthetic database enumeration; insufficiently enumerated derivatives or missing functional group substitutions reduce detection sensitivity.
- Model prediction errors in NEIMS (mass spectrum) or DeepEI (fingerprint) propagate through the similarity scoring step and may degrade classification accuracy for edge cases (e.g., compounds with unusual fragmentation patterns or weak fingerprint signatures).
- The integrated similarity score (SMSF) is a heuristic combination of spectral and fingerprint similarity; no principled statistical test or confidence interval is provided for individual predictions, only ranking-based hit assessment.

## Evidence

- [readme] PS2MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug.: "PS<sup>2</sup>MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug."
- [readme] The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively.: "The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively."
- [readme] PS2MS calculates the integrated similarity scores (SMSF) between the unknown analyte and the derivatives from synthetic database and yields a list of potential NPS identities for the analyte.: "PS<sup>2</sup>MS calculates the integrated similarity scores(SMSF) between the unknown analyte and the derivatives from synthetic database and yields a list of potential NPS identities for the"
- [other] Run inference on the test spectra using the PS2MS model to generate NPS class predictions. Collect predictions (class labels and confidence scores) and compare against the reference outputs reported in the paper or repository. Compute classification metrics (accuracy, precision, recall, F1-score) and validate that predictions match expected outputs within tolerance.: "Run inference on the test spectra using the PS2MS model to generate NPS class predictions. 4. Collect predictions (class labels and confidence scores) and compare against the reference outputs"
- [readme] The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score.: "The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score."
