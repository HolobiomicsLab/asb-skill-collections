---
name: siamese-architecture-scoring
description: Use when after a TCN-based formula prediction model has generated initial formula candidates from MS/MS spectra, apply this skill to rescore and refine those candidates when you need to improve ranking accuracy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - msfiddle
  - FIDDLE (research codebase)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Siamese-Architecture Scoring

## Summary

A neural rescoring method that uses a redesigned Siamese architecture to rank and refine molecular formula candidates from MS/MS spectra by learning paired comparisons between candidate formulas and observed spectra. This approach improves formula ranking accuracy beyond initial TCN predictions.

## When to use

After a TCN-based formula prediction model has generated initial formula candidates from MS/MS spectra, apply this skill to rescore and refine those candidates when you need to improve ranking accuracy. Use it when working with Orbitrap or Q-TOF MS/MS data where multiple plausible formulas must be ranked by confidence, especially when integrating predictions from complementary tools (BUDDY, SIRIUS) that also produce ranked candidates.

## When NOT to use

- Input is a single formula candidate with no alternatives to rank — Siamese scoring is designed for comparative ranking across multiple candidates.
- MS/MS spectrum has been pre-processed into a feature vector or embedding — Siamese architecture requires raw m/z/intensity pairs.
- You are working with a data type (e.g., negative-ion Q-TOF) for which no checkpoint was trained; the provided checkpoints are instrument-specific.

## Inputs

- Initial TCN formula predictions (list of candidate formulas with precursor m/z, formula string, predicted mass, atom counts)
- MS/MS spectrum (m/z array and intensity array pairs)
- Pre-trained Siamese rescore model checkpoint (.pt file)
- Instrument type configuration (orbitrap or qtof)
- Collision energy metadata

## Outputs

- Ranked refined formula candidates (CSV or JSON with formula, rescore confidence score, neutral mass, atom count)
- Top-K refined formulas (default top-5) with confidence scores for each spectrum

## How to apply

Load the pre-trained Siamese rescore model checkpoint (fiddle_rescore_orbitrap.pt or fiddle_rescore_qtof.pt depending on instrument type). Pass the initial TCN formula predictions and their corresponding MS/MS spectra to the rescore model, which learns pairwise comparisons between candidate formulas and the observed spectrum data. The Siamese architecture encodes both the spectrum and each formula candidate separately, then combines their representations to compute a confidence score for each candidate. Output ranked refined formula candidates sorted by rescore confidence (typically top-5), discarding low-scoring proposals. The scoring should be applied consistently across all candidates for a spectrum to ensure comparable ranking.

## Related tools

- **msfiddle** (Python API and CLI interface for invoking FIDDLE inference; loads Siamese rescore checkpoint and applies rescoring to TCN predictions) — https://github.com/josiehong/msfiddle
- **FIDDLE (research codebase)** (Full codebase containing Siamese rescore model architecture, training scripts, and pre-trained checkpoints) — https://github.com/JosieHong/FIDDLE

## Examples

```
python run_fiddle.py --test_data ./demo/input_msms.mgf --config_path ./config/fiddle_tcn_orbitrap.yml --resume_path ./check_point/fiddle_tcn_orbitrap.pt --rescore_resume_path ./check_point/fiddle_rescore_orbitrap.pt --result_path ./demo/output_fiddle.csv --device 0
```

## Evaluation signals

- Output CSV/JSON contains ranked refined formula candidates with a confidence score (Rescore column) for each candidate, sorted in descending score order.
- Top-ranked refined formula matches or is close (within 5 ppm) to the ground-truth formula when available (e.g., from SMILES or FORMULA field in MGF).
- Rescore confidence scores are bounded in a plausible range (e.g., 0.0–1.0 or logit scores) and are lower for implausible formulas.
- The number of output candidates per spectrum is consistent with the specified top-K (default top-5); any candidates below the cutoff are excluded.
- Running the same spectrum twice produces identical ranked candidates and scores (deterministic inference).

## Limitations

- Siamese architecture in FIDDLE v2.0.0 is a breaking change; checkpoints from v1.x are incompatible — must use v2.0.0 or later checkpoint assets.
- Rescore model is trained separately for Orbitrap and Q-TOF instruments; applying an Orbitrap-trained model to Q-TOF spectra or vice versa will produce unreliable scores.
- Performance depends on the quality and diversity of initial TCN predictions; if TCN fails to include the correct formula in its candidate pool, rescoring cannot recover it.
- Collision energy must be provided in the MGF input; missing or incorrect collision energy metadata may degrade rescoring accuracy.

## Evidence

- [other] The rescore model in FIDDLE v2.0.0 has been redesigned with a Siamese architecture, which is the operative inference architecture for the test.: "The rescore model has been redesigned (Siamese architecture)"
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra, with rescore model leveraging paired comparisons.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
- [other] Execute test_caffeine.py using the msfiddle Python API, passing the spectra and model checkpoint as inputs and capturing scored formula predictions.: "Execute test_caffeine.py using the msfiddle Python API, passing the spectra and model checkpoint as inputs. 4. Capture the inference output containing scored formula predictions with the Siamese"
- [readme] Pre-trained rescore models are available for both Orbitrap and Q-TOF instruments.: "fiddle_rescore_orbitrap.pt: rescore model on Orbitrap spectra
- **Q-TOF models**:
  - fiddle_tcn_qtof.pt: formula prediction model on Q-TOF spectra
  - fiddle_rescore_qtof.pt: rescore model on Q-TOF"
- [readme] Output includes ranked refined formula candidates with rescore confidence scores in the CSV result.: "Refined Formula (0..4) | Ranked refined formula candidates for the default top-5 output.
| `Refined Mass (0..4)` | Masses for the default top-5 refined candidates.
| `Rescore (0..4)` | Confidence"
