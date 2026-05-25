---
name: adduct-ion-classification-accuracy-assessment
description: Use when evaluating the correctness of adduct ion assignments in metabolomics using LC-MS or GC-MS techniques by comparing repair outcomes against reference data to measure derivation failure rate and misassignment rate.
when_to_use_negative:
- Input spectra lack valid SMILES, InChI, or compound name annotations; the repair filter cannot derive an adduct without chemical structure.
- Reference adduct assignments are themselves unreliable or missing; accuracy assessment requires ground-truth labels.
- Spectra come from unannotated experimental data (e.g., raw MS/MS acquisitions without library curation); this skill validates library-level metadata, not experimental peak picking.
edam_operation: http://edamontology.org/operation_3632
edam_topics:
- http://edamontology.org/topic_0593
- http://edamontology.org/topic_3370
tools:
- name: matchms
  role: Provides the 'repair_adduct_based_on_smiles' filter to derive canonical SMILES and predict adduct assignments from chemical structure; orchestrates the library cleaning workflow.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Converts compound names and SMILES to canonical SMILES, InChI, and InChIKey representations used for PubChem comparison and adduct derivation.
  repo: https://www.rdkit.org/
- name: PubChem
  role: Provides reference compound data (canonical SMILES, InChI, InChIKey, molecular weight) against which derived adducts and structures are validated.
  repo: https://pubchem.ncbi.nlm.nih.gov/
- name: Python
  role: Scripting language for orchestrating the matchms pipeline, counting outcomes, and generating summary statistics.
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/adduct-ion-classification-accuracy-assessment/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/adduct-ion-classification-accuracy-assessment/skill.md
    merged_at: '2026-05-25T06:57:01.414479+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/adduct-ion-classification-accuracy-assessment@sha256:cf0d5cff00992b1b0d62523af62098bc630ca4ab8c4cf41fe7f15c76a1f46bb0
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# Adduct-Ion Classification Accuracy Assessment

## Summary

Evaluate the correctness of adduct ion assignments derived from chemical structure (SMILES) by comparing repair outcomes against reference data, measuring both derivation failure rate and misassignment rate. This skill quantifies the reliability of automated adduct correction in mass spectral library cleaning pipelines.

## When to use

Apply this skill after running the 'repair_adduct_based_on_smiles' filter on an annotated MS/MS library (with valid SMILES and PubChem reference data available) to measure and report the proportion of spectra where adduct derivation failed or where the derived adduct was incorrect relative to ground truth.

## When NOT to use

- Input spectra lack valid SMILES, InChI, or compound name annotations; the repair filter cannot derive an adduct without chemical structure.
- Reference adduct assignments are themselves unreliable or missing; accuracy assessment requires ground-truth labels.
- Spectra come from unannotated experimental data (e.g., raw MS/MS acquisitions without library curation); this skill validates library-level metadata, not experimental peak picking.

## Inputs

- Annotated MS/MS spectra in matchms format with valid SMILES or InChI annotations
- Precursor m/z values and ionization mode (positive/negative) metadata
- Reference adduct assignments (from PubChem, manual curation, or validated external source)
- Spectrum subset identifiers (e.g., GNPS accessions or internal IDs)

## Outputs

- Adduct derivation failure count and percentage (e.g., 0.02% of 413,314 spectra)
- Adduct misassignment count and percentage among successfully derived adducts (e.g., 0.024% of 99.98%)
- Breakdown of incorrect adducts by type (e.g., M+H vs M+Na confusion, wrong charge)
- Summary statistics report with total spectra processed, ionization mode breakdown, and corrected adduct assignments

## How to apply

Load a subset of annotated spectra (e.g., 413,314 spectra from GNPS with valid compound annotations) in matchms format. Apply the 'repair_adduct_based_on_smiles' filter using RDKit to derive canonical SMILES and obtain predicted adducts by comparison against PubChem reference data. Count spectra where no adduct could be derived and calculate the failure rate (expect ~0.02%). For spectra where an adduct was derived, identify those with incorrect assignments by comparing against validated adduct annotations (PubChem or manual curation) and calculate the misassignment rate among successful derivations (expect ~0.024%). Generate a summary statistics report documenting both rates, absolute counts, and breakdown by ionization mode if available.

## Related tools

- **matchms** (Provides the 'repair_adduct_based_on_smiles' filter to derive canonical SMILES and predict adduct assignments from chemical structure; orchestrates the library cleaning workflow.) — https://github.com/matchms/matchms
- **RDKit** (Converts compound names and SMILES to canonical SMILES, InChI, and InChIKey representations used for PubChem comparison and adduct derivation.) — https://www.rdkit.org/
- **PubChem** (Provides reference compound data (canonical SMILES, InChI, InChIKey, molecular weight) against which derived adducts and structures are validated.) — https://pubchem.ncbi.nlm.nih.gov/
- **Python** (Scripting language for orchestrating the matchms pipeline, counting outcomes, and generating summary statistics.)

## Evaluation signals

- Derivation failure rate is within expected range (0.02% ± margin) and documented with absolute count of unrepaired spectra.
- Misassignment rate among successfully derived adducts is within expected range (0.024% ± margin) and does not exceed a pre-defined quality threshold.
- Breakdown by ionization mode or adduct type shows consistent accuracy across subgroups (e.g., M+H vs M+Na should not differ by >0.5% in error rate).
- All 413,314+ spectra are accounted for in the report (no spectra silently dropped during derivation or comparison).
- Corrected adduct assignments can be round-tripped: derived adduct + theoretical fragment loss should regenerate the observed precursor m/z within mass error tolerance (typically <5 ppm).

## Limitations

- The 'repair_adduct_based_on_smiles' filter cannot correct adducts for spectra lacking valid SMILES or PubChem reference data; validation is thus biased toward well-annotated libraries.
- Assessment is only as accurate as the reference adduct assignments used for ground truth; if PubChem or manual curation contains errors, misclassification may be underestimated.
- Wrong chemical annotations that happen to have the correct measured mass will not be detected by this skill; only adduct consistency with monoisotopic mass is checked.
- The filter assumes linear mass relationships (integer m/z shifts); non-standard adducts (e.g., [M+2H]²⁺, salt complexes) may not be correctly handled.

## Evidence

- [abstract] 0.02% failed adduct derivation; 0.024% incorrect among 99.98% successful: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] RDKit and PubChem used for canonical structure and adduct comparison: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Repair filter uses PubChem as reference for adduct derivation: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] Workflow includes structure annotation validation through adduct comparison: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [discussion] Current libraries lack plausibility checks for metadata and fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
