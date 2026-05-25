---
name: chemical-structure-derivation-from-compound-names
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to derive canonical SMILES, InChI, and InChIKey structures from compound names by querying PubChem, facilitating structural validation and error detection in mass spectral library annotations.
when_to_use_negative:
- Input spectra lack compound names or have blank/invalid compound name fields; PubChem lookup will fail for unmapped names.
- Spectra already have validated, manually curated SMILES and InChI annotations from primary literature or high-confidence reference standards; re-derivation from PubChem may overwrite accurate manual curation.
- Compound names are non-standard, proprietary, or internal identifiers not recognized by PubChem (e.g., lab-specific codes or natural product common names); derivation will fail for ~27% of names even in well-curated datasets.
edam_operation: http://edamontology.org/operation_3762
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: matchms
  role: Framework for applying the 'derive_annotation_from_compound_name' filter to query PubChem and derive canonical SMILES, InChI, and InChIKey from compound names
  repo: https://github.com/matchms/matchms
- name: PubChem
  role: Public chemical database queried via API by matchms to retrieve canonical chemical structures for given compound names
- name: RDKit
  role: Parses and canonicalizes SMILES, InChI, and InChIKey retrieved from PubChem; enables structural comparison and equivalence checks
- name: Python
  role: Programming language used for scripting the matchms pipeline and post-processing results
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
derived_from:
- doi: 10.1186/s13321-024-00878-1
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/chemical-structure-derivation-from-compound-names@sha256:15e14cb2015645713d14f5000507d306c96f3081d1ef3cfd39007ad964f8d041
---

# chemical-structure-derivation-from-compound-names

## Summary

Derives canonical SMILES, InChI, and InChIKey structures from compound names by querying PubChem, enabling structural validation and error detection in mass spectral library annotations. This skill is essential for identifying unannotated spectra and detecting structural mismatches between derived and existing annotations.

## When to use

Apply this skill when you have mass spectral data with compound names but missing or questionable chemical structure annotations (SMILES, InChI, or InChIKey). Specifically, use it when you need to validate existing structure annotations against canonical structures, identify spectra that lack structural information, or detect cases where a single compound name has been assigned multiple different 2D structures. The skill is most valuable on large curated datasets (e.g., >100,000 spectra from GNPS or similar public libraries) where systematic structural validation is needed as part of a library cleaning pipeline.

## When NOT to use

- Input spectra lack compound names or have blank/invalid compound name fields; PubChem lookup will fail for unmapped names.
- Spectra already have validated, manually curated SMILES and InChI annotations from primary literature or high-confidence reference standards; re-derivation from PubChem may overwrite accurate manual curation.
- Compound names are non-standard, proprietary, or internal identifiers not recognized by PubChem (e.g., lab-specific codes or natural product common names); derivation will fail for ~27% of names even in well-curated datasets.

## Inputs

- Mass spectral dataset in matchms-compatible format (e.g., MGF or mzML) with metadata fields: compound_name, precursor_m/z, ionmode, and optionally existing SMILES/InChI/InChIKey annotations
- Filtered spectrum list (valid annotation, compound name, matching adduct) as described in GNPS or similar curated library
- PubChem API access (queries executed via matchms filter)

## Outputs

- Updated spectrum objects with derived canonical SMILES, InChI, and InChIKey from PubChem
- Filtered spectrum table with spectrum-level derivation success/failure status
- Error report documenting: percentage of spectra from which SMILES could not be derived, percentage of annotated spectra assigned a different 2D structure, and list of structural mismatches

## How to apply

Load the mass spectral dataset (with valid compound names and ion-mode-matching adducts) into matchms version 0.26.4 or later. Apply the 'derive_annotation_from_compound_name' filter, which queries PubChem's API to retrieve canonical SMILES, InChI, and InChIKey for each compound name. Use RDKit to parse and canonicalize the retrieved structures. Compare derived structures against existing annotations in the spectrum metadata using InChIKey comparison or SMILES equivalence checks. Calculate the percentage of spectra for which SMILES derivation failed (expect ~27.6% on typical GNPS data) and the percentage of successfully annotated spectra assigned a different 2D structure (expect ~1.62%). Document both the spectra with successful structure derivation and those with structural mismatches in a filtered spectrum table and error report. The comparison step is critical: it identifies both unannotated spectra and cases where incorrect alternative structures were previously assigned to the same compound name.

## Related tools

- **matchms** (Framework for applying the 'derive_annotation_from_compound_name' filter to query PubChem and derive canonical SMILES, InChI, and InChIKey from compound names) — https://github.com/matchms/matchms
- **PubChem** (Public chemical database queried via API by matchms to retrieve canonical chemical structures for given compound names)
- **RDKit** (Parses and canonicalizes SMILES, InChI, and InChIKey retrieved from PubChem; enables structural comparison and equivalence checks)
- **Python** (Programming language used for scripting the matchms pipeline and post-processing results)

## Evaluation signals

- Derivation success rate: verify that ~72.4% of input spectra with valid compound names receive a derived SMILES/InChI/InChIKey from PubChem; ~27.6% fail (expected baseline from GNPS data).
- Structure mismatch detection: confirm that ~1.62% of successfully annotated spectra are flagged with a different 2D structure (InChIKey mismatch) compared to their original annotation.
- Metadata completeness: all spectra with successful derivation must have non-null SMILES, InChI, and InChIKey fields in output spectrum objects.
- Comparison correctness: spot-check 50–100 mismatches by manual inspection to ensure InChIKey comparison correctly identifies cases where the same compound name maps to structurally distinct molecules in PubChem.
- No false positives: verify that spectra with matching InChIKeys between derived and original annotations are NOT flagged as mismatches.

## Limitations

- Approximately 27.6% of spectra cannot be successfully deriv SMILES from compound names, likely due to non-standard naming, typos, or ambiguous names not indexed by PubChem.
- The filter detects structural mismatches based on PubChem's canonical representation but cannot distinguish between correct PubChem entries and incorrect original annotations; wrong chemical annotations consistent with the measured mass will go unnoticed.
- PubChem does not cover all chemical compounds (especially rare natural products, proprietary compounds, or very recent syntheses); derivation will fail for out-of-scope compounds.
- Compound name ambiguity: a single compound name may map to multiple structures in PubChem; the filter selects the canonical entry, but this may not always be the intended compound.
- The skill requires ion-mode-matching adducts in the input metadata; spectra with missing or incorrect ionmode will not be reliably validated.
- Future expansions needed to check if fragments match the given annotation; current pipeline does not validate whether MS/MS peaks are consistent with the derived structure.

## Evidence

- [abstract] derive_annotation_from_compound_name: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] PubChem lookup and structural comparison workflow: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] RDKit role in canonicalization: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Matchms version and implementation: "Matchms version 0.26.4 was used to run these pipelines"
- [discussion] Limitation: wrong annotations not detected: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
- [discussion] Future direction: fragment validation: "Future expansions might include filters that check if the fragments match the given annotation."
