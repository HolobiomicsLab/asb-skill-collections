---
name: modification-notation-interpretation
description: Use when you have a ProForma 2.0 peptidoform string (e.g., DLTDYLM[Oxidation]K)
  and need to extract the underlying peptide sequence and map modification positions
  to enable fragment ion annotation, mass calculation, or spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Unimod
  - spectrum_utils
  - PSI-MOD
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- 'Specify modifications by their name: `EM[Oxidation]EVEES[Phospho]PEK`'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# modification-notation-interpretation

## Summary

Parse and interpret standardized peptide modification notation (ProForma 2.0) to extract sequence and modification positions for downstream annotation and analysis. This skill enables computational tools to understand and work with complex modified peptidoforms deposited in public repositories.

## When to use

You have a ProForma 2.0 peptidoform string (e.g., DLTDYLM[Oxidation]K) and need to extract the underlying peptide sequence and map modification positions to enable fragment ion annotation, mass calculation, or spectral matching. Use this skill when working with publicly deposited mass spectra where peptide modifications are represented using controlled vocabularies (Unimod, PSI-MOD).

## When NOT to use

- Input is unmodified peptide sequence only — use raw sequence parsing instead
- Modification notation uses non-standard or proprietary formats not aligned with ProForma 2.0 specification
- Modification identifiers are not defined in accessible controlled vocabularies (Unimod, PSI-MOD, XL-MOD)

## Inputs

- ProForma 2.0 peptidoform string (e.g., 'DLTDYLM[Oxidation]K')
- Controlled vocabulary identifier (Unimod accession or PSI-MOD term)

## Outputs

- Parsed peptide sequence (bare amino acid string)
- Modification position map (list of residue indices and modification types)
- Resolved modification objects (lookup results from controlled vocabulary)

## How to apply

Use spectrum_utils.proforma to parse the ProForma 2.0 peptidoform string, which extracts both the bare peptide sequence and the positions and types of modifications. The parser resolves modification identifiers (e.g., [Oxidation]) against controlled vocabularies (Unimod, PSI-MOD, XL-MOD, Glycan Naming Ontology) to obtain standard modification properties. Once parsed, the sequence and modification map are ready for input to downstream functions such as MsmsSpectrum.annotate_proforma(), which uses them to compute theoretical fragment ion m/z values. Verify that all modification terms in the input string are recognized by the vocabulary and that the sequence is valid (standard amino acids only in the bare sequence).

## Related tools

- **spectrum_utils** (Parses ProForma 2.0 strings via spectrum_utils.proforma module to extract sequence and modification positions) — https://github.com/bittremieux/spectrum_utils/
- **Unimod** (Controlled vocabulary providing standardized definitions and properties for protein modifications referenced in ProForma notation) — https://www.unimod.org/
- **PSI-MOD** (HUPO Proteomics Standards Initiative ontology for protein modifications, integrated with ProForma parsing) — https://github.com/HUPO-PSI/psi-mod-CV/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
from spectrum_utils import proforma
peptide_str = 'DLTDYLM[Oxidation]K'
parsed = proforma.ProForma(peptide_str)
print(parsed.sequence, parsed.modifications)
```

## Evaluation signals

- Parsed sequence matches the bare amino acid substring of the input ProForma string (no brackets or modification markers)
- All modification terms in the input are successfully resolved against the integrated controlled vocabulary (no unrecognized tokens)
- Modification positions are within valid range for the sequence length (1 to sequence length)
- Resolved modification properties (mass delta, chemical formula, etc.) match Unimod/PSI-MOD definition for the assigned term
- Downstream annotation functions (e.g., annotate_proforma) accept the parsed output and produce annotated ion lists without errors

## Limitations

- Parsing depends on the availability and correctness of the ProForma 2.0 grammar implementation in spectrum_utils; edge cases in notation (e.g., ambiguous bracket placement, nested modifications) may not be handled consistently
- Modification resolution requires access to up-to-date Unimod, PSI-MOD, XL-MOD, and Glycan Naming Ontology databases; offline or outdated versions may fail to resolve recent modifications
- ProForma 2.0 supports standard amino acids and a fixed set of vocabularies; custom or non-standard modifications not in these vocabularies cannot be parsed
- The skill does not validate modification plausibility (e.g., whether oxidation at a specific site is biochemically reasonable); it only performs syntactic and vocabulary lookup

## Evidence

- [other] Parse the ProForma 2.0 peptidoform string using spectrum_utils.proforma to extract the peptide sequence and modification positions.: "Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions."
- [other] fragment ions can be annotated based on the ProForma 2.0 specification: "fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification"
- [other] Modifications are defined by controlled vocabularies including Unimod, PSI-MOD, and support for cross-linking and glycans.: "Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/), [PSI-MOD](https://github.com/HUPO-PSI/psi-mod-CV/), including support for modifications from"
- [intro] spectrum_utils enables annotating observed spectrum fragments using ProForma 2.0 specification for modified peptidoforms.: "spectrum_utils enables annotating observed spectrum fragments using ProForma 2.0 specification for modified peptidoforms"
- [other] Call MsmsSpectrum.annotate_proforma with parsed peptide to compute theoretical b and y ion m/z values.: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks"
