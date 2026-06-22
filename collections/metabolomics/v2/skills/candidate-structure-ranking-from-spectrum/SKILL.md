---
name: candidate-structure-ranking-from-spectrum
description: Use when you have an experimental tandem mass spectrum (m/z and intensity pairs) and a known or suspected chemical formula, and you need to narrow down the identity of an unknown compound from a large candidate pool (e.g., all PubChem entries matching that formula).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG WebUI
  - PubChem
  - ICEBERG (coleygroup/ms-pred repository)
  - SCARF
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
---

# candidate-structure-ranking-from-spectrum

## Summary

Rank candidate chemical structures retrieved from a compound database (PubChem) by predicting their fragment-level tandem mass spectra and scoring similarity to an experimental spectrum. This enables computational structural elucidation without requiring GPU resources via the ICEBERG WebUI or programmatic interface.

## When to use

You have an experimental tandem mass spectrum (m/z and intensity pairs) and a known or suspected chemical formula, and you need to narrow down the identity of an unknown compound from a large candidate pool (e.g., all PubChem entries matching that formula). This is most effective when experimental spectra contain rich fragmentation patterns that discriminate between isomers or structural variants.

## When NOT to use

- The chemical formula is unknown or highly ambiguous; ICEBERG requires an exact molecular formula to query PubChem efficiently.
- The experimental spectrum contains no significant fragmentation (e.g., intact molecular ion only); ranking relies on discriminative fragment patterns, so spectra with poor or minimal fragmentation may yield unreliable rankings.
- Candidates are restricted to a proprietary or non-PubChem database; the current WebUI is tightly integrated with PubChem and does not support custom candidate libraries without code modification.

## Inputs

- chemical formula (molecular formula string, e.g., C6H12O2)
- experimental tandem mass spectrum (m/z values and corresponding intensities)
- collision energy or ionization mode (optional; WebUI defaults to standard [M+H]+ mode)

## Outputs

- ranked list of candidate structures (SMILES or InChI strings)
- similarity scores (cosine similarity or equivalent metric for each candidate)
- predicted fragment-level mass spectra (m/z and intensity predictions per candidate, optional)

## How to apply

Input the chemical formula and experimental tandem mass spectrum into the ICEBERG WebUI or programmatic interface. The system queries PubChem to retrieve all candidate structures matching the chemical formula. ICEBERG then predicts fragment-level mass spectra for each candidate by decomposing molecules into molecular fragments (not just chemical subformulas, as done by SCARF) and comparing predicted spectra to the experimental spectrum using cosine similarity or related metrics. Candidates are ranked by similarity score, with highest-scoring structures representing the most likely identities. The ranking can be refined by filtering candidates using domain-specific constraints (e.g., known synthetic feasibility, expected retention time, literature prevalence).

## Related tools

- **ICEBERG WebUI** (Primary interface for submitting chemical formula and experimental spectrum and retrieving ranked candidate structures with similarity scores; runs inference without GPU.) — http://iceberg-ms.mit.edu/
- **ICEBERG (coleygroup/ms-pred repository)** (Underlying neural network model implementing fragment-level spectrum prediction and similarity ranking; also provides programmatic Python interface for advanced users.) — https://github.com/coleygroup/ms-pred
- **PubChem** (Candidate structure database; queried by chemical formula to retrieve all matching SMILES/InChI records for ranking.)
- **SCARF** (Alternative spectrum prediction model (included in ms-pred repo for comparison); predicts spectra at chemical formula level rather than fragment level, less discriminative for isomer ranking.) — https://github.com/coleygroup/ms-pred

## Examples

```
# Via WebUI: navigate to http://iceberg-ms.mit.edu/, enter chemical formula (e.g. C6H12O2) and paste experimental spectrum peaks, then submit for ranking.
# Programmatic: see notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb in coleygroup/ms-pred repository.
```

## Evaluation signals

- Top-ranked candidate structure matches known or confirmed identity (ground truth); ICEBERG achieves ~40% top-1 retrieval accuracy on NIST'20 [M+H]+ data.
- Similarity score distribution is non-uniform and well-separated (highest-ranked candidates have substantially higher scores than lower-ranked); uniform or overlapping scores indicate poor discriminative power.
- Predicted fragment peaks (m/z values and intensities) for the top-ranked candidate align visually and quantitatively with experimental spectrum peaks (e.g., within mass accuracy tolerance, ~5 ppm for high-resolution instruments).
- Ranked list is stable across resubmissions (no stochasticity in inference; WebUI is deterministic).
- Processing completes without GPU requirement and returns results in <2 minutes for typical PubChem candidate pools (tens to hundreds of structures).

## Limitations

- ICEBERG performance depends critically on the quality and representativeness of training data (NIST'20 or MassSpecGym); predictions on compounds with unusual fragmentation or rare functional groups may be less reliable.
- Ranking is most effective for [M+H]+ ions in positive electrospray ionization (ESI) mode; performance on other ionization modes or collision energies is not extensively benchmarked.
- Large candidate pools (>10,000 structures per formula) may incur longer runtime; no tiered or approximate retrieval strategy is described.
- The WebUI does not support custom model weights or retraining; users requiring model adaptation must use the GitHub repository and train locally (requires NIST'20 license or access to MassSpecGym; see README for licensing details).
- No changelog or versioning information provided in documentation; unclear how model updates affect backward compatibility of archived rankings.

## Evidence

- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [other] No GPU is required to run ICEBERG structural elucidation via the WebUI: "No GPU is required to run ICEBERG structural elucidation via the WebUI"
- [other] ICEBERG predicts fragment-level mass spectra for each candidate and ranks them by similarity to the experimental spectrum.: "ICEBERG predicts fragment-level mass spectra for each candidate and ranks them by similarity to the experimental spectrum."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] Running the demo takes <2 minutes with a regular desktop GPU.: "Running the demo takes <2 minutes with a regular desktop GPU."
