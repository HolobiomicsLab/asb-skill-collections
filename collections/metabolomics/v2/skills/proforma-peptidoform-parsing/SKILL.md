---
name: proforma-peptidoform-parsing
description: Use when when you have a ProForma 2.0–formatted peptide string with PSI-MOD or UniMod modification labels and need to extract the underlying amino acid sequence and modification positions before performing theoretical fragment ion calculation or spectrum peak matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - PSI-MOD Protein Modifications Ontology
  - spectrum_utils MsmsSpectrum.annotate_proforma()
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ProForma 2.0 peptidoform parsing

## Summary

Parse ProForma 2.0 peptidoform strings (e.g., 'EM[Oxidation]EVEES[Phospho]PEK') to extract amino acid sequences and position-specific post-translational modifications for subsequent fragment ion annotation and spectrum matching. This is a prerequisite for annotating observed MS/MS spectrum peaks against modified peptide sequences.

## When to use

When you have a ProForma 2.0–formatted peptide string with PSI-MOD or UniMod modification labels and need to extract the underlying amino acid sequence and modification positions before performing theoretical fragment ion calculation or spectrum peak matching. Trigger: input peptidoform contains bracket-enclosed modification tags (e.g., [Oxidation], [MOD:00719], [Phospho]).

## When NOT to use

- Input peptide is already represented as separate sequence + modification arrays (i.e., already parsed); re-parsing is redundant and may lose precision.
- Peptidoform uses non-ProForma notation (e.g., plain text 'EM_ox' or legacy UNIMOD syntax); parser will fail or misinterpret.
- Modification tags reference identifiers not present in the active PSI-MOD version; resolution will fail or produce incorrect mass values.

## Inputs

- ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK')
- PSI-MOD modification ontology (implicit; spectrum_utils.proforma resolves names and identifiers)

## Outputs

- Parsed amino acid sequence (unmodified backbone)
- Position-indexed modification map (dict: {position: modification_name_or_id})
- Modification mass deltas (optional; used downstream for theoretical fragment m/z calculation)

## How to apply

Use spectrum_utils.proforma module to parse the ProForma 2.0 string and decompose it into amino acid sequence and a position-indexed modification map. The parser recognizes both human-readable modification names (e.g., 'Oxidation', 'Phospho') and PSI-MOD identifiers (e.g., 'MOD:00719'). The extracted sequence and modifications are then passed to downstream annotation functions (e.g., MsmsSpectrum.annotate_proforma()) along with fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types ('by' for b and y ions; 'abc' or 'xyz' for expanded sets; 'I' for immonium), and optional neutral loss specifications. The parser validates bracket syntax and modification name resolution against the PSI-MOD ontology; malformed strings will raise parsing errors.

## Related tools

- **spectrum_utils** (Python library providing proforma module to parse and decompose ProForma 2.0 peptidoform strings into sequence and modification maps) — https://github.com/bittremieux/spectrum_utils
- **PSI-MOD Protein Modifications Ontology** (Authority for PSI-MOD modification identifiers and names used in ProForma 2.0 tags; spectrum_utils resolves tags against this ontology) — https://github.com/HUPO-PSI/psi-mod-CV
- **spectrum_utils MsmsSpectrum.annotate_proforma()** (Downstream consumer of parsed peptidoform data; accepts the peptide string and uses the parsed modifications to compute theoretical fragment ion m/z values) — https://github.com/bittremieux/spectrum_utils

## Examples

```
from spectrum_utils.proforma import parse; seq, mods = parse('EM[Oxidation]EVEES[Phospho]PEK'); print(seq, mods)
```

## Evaluation signals

- Parsing succeeds without exceptions and returns a non-empty sequence string and modification map for valid ProForma 2.0 input.
- Extracted amino acid sequence matches the unmodified backbone when all bracket-enclosed modification tags are removed from the input string.
- Position indices in the modification map correspond to zero-indexed or one-indexed positions in the extracted sequence (verify against the annotate_proforma downstream call).
- Modification names/identifiers resolve to valid PSI-MOD entries or raise a clear parsing error if unrecognized.
- Round-trip: re-formatting the parsed sequence and modifications back to ProForma 2.0 notation yields a string equivalent to (or predictably normalized from) the original input.

## Limitations

- Parser is tied to the version of the PSI-MOD ontology bundled with spectrum_utils; if a modification tag is added to a newer PSI-MOD version but spectrum_utils is not updated, resolution will fail.
- ProForma 2.0 supports terminal modifications (e.g., '[Acetyl]-EM[Oxidation]EVEES'); parsing and annotation of terminal mods depends on spectrum_utils version and may not be fully supported in all fragment ion types.
- Ambiguous or alternative modification representations (e.g., 'Ox' vs. 'Oxidation', 'Phosphorylation' vs. 'Phospho') must match the exact PSI-MOD name used by spectrum_utils; non-canonical aliases are not automatically normalized.
- No changelog available for spectrum_utils proforma module, so version-to-version breaking changes in parsing behavior or modification name authority are not documented in the referenced article.

## Evidence

- [other] Parse the ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK') using spectrum_utils.proforma to extract amino acid sequence and position-specific modifications.: "Parse the ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK') using spectrum_utils.proforma to extract amino acid sequence and"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal): "Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments"
- [readme] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
