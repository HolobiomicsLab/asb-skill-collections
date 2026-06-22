---
name: fixed-modification-propagation
description: Use when your search engine output (PSM file) omits fixed modifications that were configured during the search (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3703
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  - DeepLC
  - ProForma
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- MS²Rescore is a tool for rescoring peptide-spectrum matches
- Accepted ProForma modification labels in :py:mod:`psm_utils`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2rescore_immunopeptidome_rescoring_cq
    doi: 10.1002/pmic.202300336
    title: MS2Rescore (immunopeptidome rescoring)
  dedup_kept_from: coll_ms2rescore_immunopeptidome_rescoring_cq
schema_version: 0.2.0
---

# fixed-modification-propagation

## Summary

Augment PSM records with fixed modifications (e.g., carbamidomethylation, TMT labeling) that were applied during MS analysis but not reported in the search engine output file. This skill ensures MS²Rescore can accurately represent the true chemical state of peptides during rescoring, particularly when using search engines like MaxQuant that do not report fixed modifications in their PSM files.

## When to use

Your search engine output (PSM file) omits fixed modifications that were configured during the search (e.g., MaxQuant or similar tools that suppress fixed modification reporting), and you need to reconstruct those modifications before rescoring to ensure accurate feature generation and rescoring by tools like MS²Rescore or DeepLC.

## When NOT to use

- The search engine already reports fixed modifications in the PSM file (check the peptide sequence column for existing modification annotations).
- You are working with a search engine (e.g., Percolator output) where fixed modifications are already embedded in the reported sequences.
- Your downstream rescoring engine does not require or accept ProForma-formatted modification notation.

## Inputs

- PSM file in psm_utils-supported format (e.g., MaxQuant msms.txt, MSGFPlus .mzid, Sage .sage.tsv)
- fixed_modifications configuration mapping (JSON/TOML with ProForma labels → residue lists)
- modification_mapping configuration (ProForma labels to residue targets)

## Outputs

- Augmented PSM file with fixed modifications inserted into peptide sequences using ProForma notation
- PSM records with all original fields preserved plus updated peptide sequences

## How to apply

Load the PSM file and extract all peptide sequences with their existing ProForma modification annotations. In parallel, load the fixed_modifications configuration mapping, which associates ProForma labels (e.g., 'U:Carbamidomethyl', 'U:TMT6plex') with lists of target residue positions (including 'N-term' and 'C-term' for terminal modifications). For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions using ProForma notation (e.g., '[U:Carbamidomethyl]' after 'C') if they are not already present in the sequence. Write the augmented PSM records with updated peptide sequences back to the output file, preserving all other PSM fields unchanged. This ensures downstream feature generators and rescoring engines receive chemically accurate peptide representations.

## Related tools

- **MS²Rescore** (Platform that requires fixed-modification-augmented PSM files as input; uses the reconstructed modifications during feature generation and rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Utility library for parsing PSM files in multiple formats and handling ProForma modification notation)
- **DeepLC** (Feature generator within MS²Rescore that requires modification formula information; benefits from accurate fixed modification representation)
- **ProForma** (Standard notation schema for representing modified peptide sequences; defines syntax for fixed modification insertion (e.g., U:Carbamidomethyl, U:TMT6plex)) — https://github.com/HUPO-PSI/ProForma

## Evaluation signals

- All PSM records in the output file contain the expected fixed modifications at their correct positions (e.g., '[U:Carbamidomethyl]' immediately after every cysteine, '[U:TMT6plex]' at N-terminus and all lysines if configured).
- ProForma syntax validation: all modification strings parse correctly and conform to HUPO-PSI ProForma v2 notation (e.g., '[U:ModificationLabel]' or 'N-term[U:ModificationLabel]').
- Row count and non-modification fields are identical between input and output PSM files; only the peptide sequence column has been augmented.
- Downstream rescoring with MS²Rescore completes without modification parsing errors and generates expected feature values from DeepLC and other predictors.
- Spot-check: manually verify 5–10 peptide sequences in the output to confirm modifications match the configured fixed_modifications map (e.g., if 'C' → 'Carbamidomethyl' is configured, every cysteine should carry the annotation).

## Limitations

- This skill assumes the fixed_modifications configuration exactly matches what was applied during the original MS search; misconfigurations will propagate incorrect modifications into rescoring.
- Terminal modifications (N-term, C-term) must be explicitly specified in the fixed_modifications map; the skill does not infer them from search engine logs.
- If a PSM's peptide sequence already contains a modification annotation for a residue targeted by fixed_modifications, the skill skips reinsertion (to avoid duplication), which may mask configuration conflicts.
- The skill does not validate that all PSMs were actually modified during the search; it blindly applies the configuration to every record, assuming uniform search parameters.
- Modification formulas required by some feature generators (e.g., DeepLC) are not directly extracted; only ProForma labels are inserted, so downstream tools must be configured with the corresponding formula mappings.

## Evidence

- [other] fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special labels N-term and C-term for terminal modifications: "Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special"
- [other] For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation (e.g., 'U:Carbamidomethyl') if not already present: "For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation"
- [intro] Some search engines, such as MaxQuant, do not report fixed modifications: "Some search engines, such as MaxQuant, do not report fixed modifications"
- [intro] fixed modifications that are not reported in the PSM file must be configured separately: "fixed modifications that are not reported in the PSM file must be configured separately"
- [intro] some feature generators (such as DeepLC) require the modification formula: "some feature generators (such as DeepLC) require the modification formula"
- [intro] MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides"
