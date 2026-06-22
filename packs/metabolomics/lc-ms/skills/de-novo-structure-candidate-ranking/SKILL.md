---
name: de-novo-structure-candidate-ranking
description: Use when when you have high-resolution LC-MS/MS data for an unknown metabolite or small molecule, have computed or measured the molecular ion mass and fragmentation spectrum, and require de-novo structure generation because the compound is absent from spectral libraries or structure databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0592
  - http://edamontology.org/topic_3520
  tools:
  - MSNovelist
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans:
- The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-021-01045-9
  all_source_dois:
  - 10.1038/s41587-021-01045-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# de-novo-structure-candidate-ranking

## Summary

Rank de-novo generated candidate molecular structures by submitting fragmentation spectra and molecular ion mass to the MSNovelist web service, retrieving scored and ranked structural predictions for unknown small molecules. This skill is essential when MS/MS data lacks database matches and chemical structure must be predicted from spectral fragmentation patterns alone.

## When to use

When you have high-resolution LC-MS/MS data for an unknown metabolite or small molecule, have computed or measured the molecular ion mass and fragmentation spectrum, and require de-novo structure generation because the compound is absent from spectral libraries or structure databases. Use this skill as a downstream step after SIRIUS has assigned a molecular formula and computed a fragmentation tree.

## When NOT to use

- Input is a known compound already present in a spectral library or commercial database; use library matching or database lookup instead.
- Fragmentation spectrum is of low quality, has few peaks, or low signal-to-noise ratio; MSNovelist requires informative spectral patterns for reliable structure ranking.
- Non-academic user without a commercial license from Bright Giant GmbH; SIRIUS web services (including MSNovelist) are restricted to academic research and education use only.

## Inputs

- molecular_ion_mass (m/z, numeric)
- fragmentation_spectrum (peak list: mass and intensity pairs)
- optional: molecular_formula (assigned by SIRIUS)
- optional: fragmentation_tree (computed by SIRIUS)

## Outputs

- ranked_candidate_structures (JSON or CSV table with columns: rank, SMILES, score, molecular_formula, mass_deviation)
- structure_metadata (confidence scores, alternative candidate lists)

## How to apply

Prepare a JSON payload containing the molecular ion mass (m/z) and the fragmentation spectrum data (peak masses and intensities) in the format accepted by the MSNovelist REST API endpoint. Submit an HTTP POST request to the MSNovelist web service integrated within the SIRIUS framework, providing authentication credentials via institutional email account (required for academic access). The service returns a JSON response containing candidate structures ranked by a scoring metric that reflects confidence in the structure prediction. Parse the response to extract the ranked list of structures in SMILES format, along with rank position and associated scores. Serialize the results into a structured output file (JSON or CSV) with fields for structure SMILES, rank, score, and metadata such as molecular formula and mass deviation. Evaluate the top-ranked candidates by comparing predicted fragmentation patterns (via CSI:FingerID) against the experimental spectrum to filter implausible structures.

## Related tools

- **SIRIUS** (Framework that integrates MSNovelist web service dispatch; orchestrates molecular formula assignment, fragmentation tree computation, and structure prediction workflow) — https://github.com/sirius-ms/sirius
- **MSNovelist** (Core de-novo structure generation service; accepts fragmentation spectrum and molecular ion mass, returns ranked candidate structures scored by neural network model)
- **CSI:FingerID** (Secondary validation tool; compares predicted fragmentation fingerprints of top MSNovelist candidates against experimental spectrum to filter and re-rank structures)
- **CANOPUS** (Complementary compound classification service; provides chemical taxonomy and class prediction to contextualize and filter candidate structures from MSNovelist)

## Evaluation signals

- Response JSON contains non-empty candidates array with rank, SMILES, and numeric score fields for each structure.
- Ranked structures are ordered by score (descending or ascending per service specification); top-ranked candidate has chemical plausibility (valid SMILES, reasonable molecular weight and formula agreement).
- Mass deviation between predicted molecular ion mass of top-ranked structure and input m/z is within acceptable error tolerance (typically <5 ppm for high-resolution MS).
- Top-ranked structure's predicted fragmentation pattern (via CSI:FingerID) shows cosine similarity > 0.6–0.7 with experimental fragmentation spectrum.
- Candidate structures are chemically diverse in top ranks (not repetitive or trivial stereoisomers), indicating service is exploring structural hypothesis space.

## Limitations

- MSNovelist performance degrades on low-quality spectra with few informative fragments; requires m/z > ~100 and spectrum with ≥3–5 distinct fragment peaks for reliable ranking.
- De-novo predictions are sensitive to the accuracy of input molecular mass and fragmentation data; systematic mass calibration errors or contaminant peaks can bias candidate ranking.
- Academic access to SIRIUS web services requires institutional email validation; non-academic users must obtain a commercial license from Bright Giant GmbH.
- MSNovelist is trained on structural databases with known biases (e.g., toward common natural products, plant metabolites); novel or exotic scaffold structures may rank lower or not appear.
- No changelog is publicly available for model or ranking algorithm updates, limiting reproducibility across different SIRIUS versions.

## Evidence

- [other] Prepare query payload containing molecular ion mass and optional fragmentation spectrum data in the format accepted by the MSNovelist REST API endpoint.: "Prepare query payload containing molecular ion mass and optional fragmentation spectrum data in the format accepted by the MSNovelist REST API endpoint."
- [other] Submit HTTP POST request to the MSNovelist web service with the prepared payload. Retrieve JSON-formatted response containing ranked candidate structures and associated scores.: "Submit HTTP POST request to the MSNovelist web service with the prepared payload. Retrieve JSON-formatted response containing ranked candidate structures and associated scores."
- [other] Parse and serialize the candidate structures into a structured output file (JSON or CSV) with fields for structure SMILES, rank, score, and metadata.: "Parse and serialize the candidate structures into a structured output file (JSON or CSV) with fields for structure SMILES, rank, score, and metadata."
- [readme] The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only.: "The SIRIUS web services (CSI:FingerID, CANOPUS, MSNovelist and others) hosted by the Böcker group are for academic research and education use only."
- [readme] Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the SIRIUS graphical user interface.: "Fragmentation trees and spectra can be directly uploaded from SIRIUS to the CSI:FingerID, CANOPUS and MSNovelist web services. Results are retrieved from the web service and can be displayed in the"
