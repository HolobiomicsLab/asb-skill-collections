---
name: structure-annotation-validation
description: Validate and repair structural annotations (SMILES, InChI, InChIKey) in mass spectral library entries by comparing derived and recorded chemical identifiers, checking adduct–precursor m/z consistency, and flagging or correcting mismatches. This skill ensures annotations are chemically plausible and internally consistent before downstream analysis.
when_to_use_negative:
- Input library contains only unannotated spectra or lacks compound name, SMILES, InChI, or InChIKey fields; no structural annotation to validate.
- Annotations have already undergone expert manual curation and are known to be correct; re-validation wastes computation and may introduce false positives.
- Mass accuracy of the instrument is unknown or non-standard (e.g., <1 ppm or >10 ppm tolerance); adduct–m/z validation thresholds cannot be reliably set.
edam_operation: http://edamontology.org/operation_3802
edam_topics:
- http://edamontology.org/topic_0218
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3391
tools:
- name: matchms
  role: Framework for loading, filtering, and validating mass spectral library metadata; applies cascade of repair and validation filters on SMILES, InChI, InChIKey, adduct, and precursor m/z.
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses SMILES and InChI, derives canonical SMILES from compound names, calculates neutral mass from structure, infers adducts, detects salts.
  repo: https://www.rdkit.org
- name: PubChem
  role: External database queried to derive canonical SMILES, InChI, and InChIKey from compound name; provides reference structures for annotation validation.
  repo: https://pubchem.ncbi.nlm.nih.gov
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/structure-annotation-validation@sha256:2c3b7a5ef011ff5b42bc1f8f19ec435138f546ca5c67a427111e0cc56c8e4007
---

# structure-annotation-validation

## Summary

Validate and repair structural annotations (SMILES, InChI, InChIKey) in mass spectral library entries by comparing derived and recorded chemical identifiers, checking adduct–precursor m/z consistency, and flagging or correcting mismatches. This skill ensures annotations are chemically plausible and internally consistent before downstream analysis.

## When to use

Apply this skill when ingesting or curating a mass spectral library (MGF, mzML, or similar) where metadata annotations exist but their accuracy and internal consistency are unknown or suspect. Trigger conditions include: (1) library sourced from public databases (GNPS, MoNA, MassBank, NIST) that may contain incomplete or incorrect annotations; (2) presence of both compound name and structural fields (SMILES, InChI, InChIKey, precursor m/z, adduct) that can be cross-validated; (3) need to remove or repair spectra before downstream spectral matching or metabolite identification. Do NOT apply if annotations are already manually curated and validated, or if the library contains only unannotated spectra.

## When NOT to use

- Input library contains only unannotated spectra or lacks compound name, SMILES, InChI, or InChIKey fields; no structural annotation to validate.
- Annotations have already undergone expert manual curation and are known to be correct; re-validation wastes computation and may introduce false positives.
- Mass accuracy of the instrument is unknown or non-standard (e.g., <1 ppm or >10 ppm tolerance); adduct–m/z validation thresholds cannot be reliably set.

## Inputs

- MGF file (mass spectral library in mzML or MGF format with metadata fields: compound_name, SMILES, InChI, InChIKey, precursor_mz, parent_mass, adduct, ionmode)
- YAML configuration file specifying filter order and parameters (tolerance thresholds, PubChem API credentials if needed)
- RDKit-compatible chemical structure representations (SMILES strings or InChIKey)

## Outputs

- Cleaned MGF file with repaired and validated annotations
- Summary statistics (TSV or JSON): input spectrum count, retained count, removed count, repaired count, per-filter removal/repair breakdown
- Filtered spectrum list: records of removed spectra with removal reason, and repaired spectra with before–after annotation deltas

## How to apply

Load spectra from the MGF file using matchms 0.26.4 and apply the library-cleaning filter cascade in sequence: (1) run basic metadata harmonization to standardize field names and units; (2) derive missing structural identifiers (canonical SMILES, InChI, InChIKey) from the compound name via PubChem lookup; for spectra where derivation fails (typically 27–28%), flag as candidates for removal. (3) For spectra with derived or recorded SMILES, use RDKit to parse and compare structures; if salts are detected, repair the SMILES to the parent compound. (4) Validate precursor m/z against molar mass: repair parent mass if it was incorrectly calculated from molar mass instead of monoisotopic mass. (5) Apply the 'Repair adduct and parent mass based on SMILES' filter: derive the expected neutral mass from SMILES using RDKit, then infer the correct adduct; flag spectra where no valid adduct can be derived (~0.02%) or where the recorded adduct contradicts the derived mass. (6) Apply 'Repair not matching annotation' to detect and correct cases where precursor m/z does not match the annotated structure within the instrument's mass accuracy tolerance (typically ±5 ppm for high-resolution MS). (7) Require valid annotation: reject any spectrum that lacks ionmode, precursor m/z, and a valid chemical structure (SMILES or InChIKey) after all repairs. Track spectrum counts (input, retained, removed, repaired) and log decisions for reproducibility.

## Related tools

- **matchms** (Framework for loading, filtering, and validating mass spectral library metadata; applies cascade of repair and validation filters on SMILES, InChI, InChIKey, adduct, and precursor m/z.) — https://github.com/matchms/matchms
- **RDKit** (Parses SMILES and InChI, derives canonical SMILES from compound names, calculates neutral mass from structure, infers adducts, detects salts.) — https://www.rdkit.org
- **PubChem** (External database queried to derive canonical SMILES, InChI, and InChIKey from compound name; provides reference structures for annotation validation.) — https://pubchem.ncbi.nlm.nih.gov

## Evaluation signals

- Spectrum counts match expected values: input count (e.g., 500,569), retained count (e.g., 448,485), removed count (e.g., 31,758), and repaired count (e.g., 52,084) are reproducible and logged.
- All retained spectra have non-null ionmode, precursor_mz, and SMILES or InChIKey after repair; no mandatory annotation field is missing.
- Per-filter statistics show expected rates: e.g., 'derive annotation from compound name' succeeds for ~72% of spectra; 'repair adduct and parent mass based on SMILES' derives valid adducts for ~99.98% of spectra.
- Repaired spectra show before–after deltas (e.g., SMILES corrected, adduct inferred, parent mass recalculated) that are chemically and biochemically sensible (e.g., salt removed to parent, molar mass converted to monoisotopic mass).
- Pipeline execution time is predictable and scales linearly with spectrum count (e.g., ~0.05 ms per spectrum for 500k spectra ≈ 6–7 hours); no unexplained performance regressions or timeout failures.

## Limitations

- The current pipeline does not check whether observed MS/MS fragments actually match the given chemical annotation; wrong annotations that are consistent with precursor m/z will pass validation. Future expansions must include spectral plausibility checks comparing theoretical fragmentation to measured peaks.
- Derivation of annotation from compound name via PubChem fails for ~27.6% of spectra, especially for ambiguous, misspelled, or non-standard compound names; these spectra are removed unless recovered by other repair functions.
- The repair 'not matching annotation' filter assumes a fixed mass accuracy tolerance (typically ±5 ppm); instruments with lower accuracy (e.g., low-resolution quadrupole) or higher accuracy (e.g., <1 ppm Orbitrap) may require parameter tuning.
- Adduct inference from SMILES assumes ionization follows standard protonation or adduction rules (e.g., [M+H]⁺, [M-H]⁻, [M+Na]⁺); unusual adducts or multi-charged ions may not be recognized.
- PubChem API queries can be rate-limited or fail for disconnected environments; large-scale batch derivation may require local SMILES databases or cached structure tables.
- Metadata fields such as instrument type and collision energy are not yet cleaned or validated by the current matchms pipeline; library entries may contain inconsistent or missing values in these fields.

## Evidence

- [abstract] metadata cleaning, peak filtering, intensity normalization, and structure annotation validation: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [abstract] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments"
- [abstract] SMILES, InChI and InChIKey are loaded by RDKit and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit and compared to each other"
- [abstract] Library cleaning. Runs all default filters, but in addition repairs errors in the annotations and requires complete annotations after all repairs were run: "Library cleaning. Runs all default filters, but in addition repairs errors in the annotations and requires complete annotations after all repairs were run"
