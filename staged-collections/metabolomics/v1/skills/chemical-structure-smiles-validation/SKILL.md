---
name: chemical-structure-smiles-validation
description: Use when validating and repairing chemical structure annotations (SMILES, InChI, InChIKey) in the domain of metabolomics using methods like LC-MS and GC-MS, applying to compound names or PubChem to ensure consistency with measured precursor mass or adduct state.
when_to_use_negative:
- Spectra already contain validated, canonicalized SMILES and verified parent masses—skip this step to avoid redundant computation.
- Library does not include compound name or structure information—structural validation cannot proceed without a reference annotation.
- The analysis goal is MS/MS fragment matching or library search—prioritize spectral comparison over annotation repair; only validate structures if annotation errors would bias search scores.
edam_operation: http://edamontology.org/operation_3674
edam_topics:
- http://edamontology.org/topic_0153
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3520
tools:
- name: matchms
  role: Core framework for loading, filtering, and repairing spectral metadata and annotations; orchestrates the entire cleaning pipeline
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Canonicalizes and parses SMILES, InChI, and InChIKey; calculates monoisotopic mass from chemical structures; detects structural mismatches
- name: PubChem
  role: Source of canonical SMILES, InChI, and InChIKey for compound names; enables automatic structure annotation derivation
- name: Python
  role: Programming environment for orchestrating matchms filters and RDKit operations
provenance:
  source_task_ids:
  - task_005
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
derived_from:
- doi: 10.1186/s13321-024-00878-1
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/chemical-structure-smiles-validation@sha256:4fcfd8d2890db5ad760baebecf61d37930445225a6fe4079efc28e8dc41a64c0
---

# Chemical Structure SMILES Validation

## Summary

Validates and repairs chemical structure annotations (SMILES, InChI, InChIKey) by deriving canonical forms from compound names or PubChem, comparing structural representations for consistency, and detecting mismatches between annotation and measured precursor mass or adduct state. This skill is essential for ensuring that MS/MS spectral libraries contain chemically plausible and internally consistent structural metadata.

## When to use

When processing mass spectral libraries (e.g., GNPS, MoNA, MassBank) where compound annotations may be incomplete, inconsistent, or derived from ambiguous sources like free-text compound names. Apply this skill when you need to repair metadata that would otherwise cause spectra to be removed (e.g., missing SMILES), detect structural inconsistencies (e.g., different 2D structures derived from the same compound name), or verify that the annotation's monoisotopic mass and adduct state match the observed precursor m/z.

## When NOT to use

- Spectra already contain validated, canonicalized SMILES and verified parent masses—skip this step to avoid redundant computation.
- Library does not include compound name or structure information—structural validation cannot proceed without a reference annotation.
- The analysis goal is MS/MS fragment matching or library search—prioritize spectral comparison over annotation repair; only validate structures if annotation errors would bias search scores.

## Inputs

- Mass spectral library in MGF or JSON format (matchms-compatible)
- Compound annotations: free-text names, SMILES strings, or InChI identifiers
- Precursor m/z values (experimental)
- Parent mass metadata (may be molar mass instead of monoisotopic)
- Adduct annotations (e.g., [M+H]+, [M-H]−)

## Outputs

- Validated SMILES (canonical form from PubChem or RDKit)
- Validated InChI and InChIKey (canonical forms)
- Corrected parent_mass values (monoisotopic, not molar)
- Validated or repaired adduct annotations
- Flagged or removed spectra with unresolvable annotation conflicts
- Metadata repair report (e.g., count of spectra corrected per filter)

## How to apply

Load spectra and their compound annotations (names or existing SMILES/InChI) using matchms. Use RDKit to canonicalize SMILES, InChI, and InChIKey by querying PubChem with the compound name or existing structure. Compare all three representations to detect discrepancies; if >1 unique 2D structure is inferred from the same compound name, flag the spectrum for manual review or remove it. For each validated structure, calculate the monoisotopic mass and check that it matches the parent_mass field within the expected tolerance; if the parent_mass was computed from molar mass instead, correct it using the canonicalized structure. Finally, validate that the adduct (e.g., [M+H]+, [M-H]−) is consistent with the corrected precursor m/z and monoisotopic mass. Spectra failing these checks are either repaired (if the error is correctable) or removed.

## Related tools

- **matchms** (Core framework for loading, filtering, and repairing spectral metadata and annotations; orchestrates the entire cleaning pipeline) — https://github.com/matchms/matchms
- **RDKit** (Canonicalizes and parses SMILES, InChI, and InChIKey; calculates monoisotopic mass from chemical structures; detects structural mismatches)
- **PubChem** (Source of canonical SMILES, InChI, and InChIKey for compound names; enables automatic structure annotation derivation)
- **Python** (Programming environment for orchestrating matchms filters and RDKit operations)

## Evaluation signals

- All spectra with compound name annotations have a derived SMILES, InChI, and InChIKey; count the fraction of spectra that could not be derived (expected ~27.6% for GNPS)
- For spectra with multiple inferred structures from the same compound name, verify that conflicts are flagged; ~1.62% of GNPS spectra showed different 2D structures after annotation derivation
- Parent mass values are recalculated from canonical SMILES monoisotopic mass; verify that corrected parent_mass matches the expected monoisotopic mass (not molar mass)
- Adduct validation: verify that corrected adduct and parent mass are consistent with observed precursor m/z within expected tolerance (e.g., ±0.01 Da or ±5 ppm); ~0.024% of GNPS spectra had incorrect adducts after repair
- Metadata repair count: validate that the number of repaired spectra matches the pipeline output (e.g., 'repair_parent_mass_is_molar_mass' and 'repair adduct and parent mass based on SMILES' should collectively repair ~52,084 GNPS spectra)

## Limitations

- Compound names are often ambiguous or colloquial; PubChem lookup may fail for proprietary or non-standard names, preventing automatic structure derivation (27.6% failure rate in GNPS)
- Chemical structures consistent with observed precursor mass but chemically incorrect will not be detected; the pipeline only validates consistency between annotation, mass, and adduct, not fragment matching
- Additional metadata fields (instrument type, collision energy) are not yet validated or cleaned by matchms filters; future expansions are needed
- Monoisotopic mass calculation assumes a single protonation state; isotope patterns, multiply-charged ions, or unusual adducts may not be properly handled
- If both structural representation and parent mass are wrong but internally consistent, the error will pass validation

## Evidence

- [abstract] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] This filter derives the canonical SMILES, InChI and InChIKey from PubChem: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass: "A common mistake is that the parent mass is calculated from the molar mass instead of the monoisotopic mass"
- [abstract] The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [discussion] Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments.: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments"
