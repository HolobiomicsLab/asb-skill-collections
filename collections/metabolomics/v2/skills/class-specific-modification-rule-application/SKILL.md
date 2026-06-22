---
name: class-specific-modification-rule-application
description: Use when after identifying putative BGC-encoded precursor peptides from a genome assembly via MetaMiner's BGC identifier, when preparing a RiPP structure database for downstream spectral matching via Dereplicator.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0202
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - NPDtools 2.5.0 (RiPP Structure Database Builder module)
  - Dereplicator
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
---

# class-specific-modification-rule-application

## Summary

Enumerate putative post-translationally modified (PTM) variants of RiPP precursor peptides by applying class-specific modification rules (e.g., lantibiotic, lassopeptide, cyanobactin) to generate candidate structure databases. This skill bridges genome mining and spectral matching by ensuring only chemically feasible modifications for a given RiPP class are included in the search space.

## When to use

After identifying putative BGC-encoded precursor peptides from a genome assembly via MetaMiner's BGC identifier, when preparing a RiPP structure database for downstream spectral matching via Dereplicator. Apply this skill when the RiPP class (lantibiotic, lassopeptide, cyanobactin, etc.) is known or specified and you need to generate all plausible PTM variants before mass spectrometry matching.

## When NOT to use

- RiPP class is unknown or ambiguous and cannot be reliably specified — run a preliminary class prediction step first.
- Precursor peptide sequences have already been manually curated or validated experimentally — skip enumeration if golden-standard PTM structures are already available.
- Input is non-peptidic natural products or metabolites outside the RiPP family — use Dereplicator+ or VarQuest instead.

## Inputs

- Precursor peptide sequences (FASTA or plaintext, extracted from BGC-containing genome assembly)
- RiPP class designation (e.g., 'lantibiotic', 'lassopeptide', 'cyanobactin', or equivalent string parameter)

## Outputs

- Per-class RiPP structure database (TSV or equivalent structured format)
- Enumerated candidate structures indexed by precursor ID and PTM variant
- Aggregated database ready for downstream Dereplicator spectral matching

## How to apply

For each precursor peptide extracted from an identified BGC, invoke the RiPP Structure Database Builder module with the target RiPP class specified via the --class parameter. The builder applies class-specific modification rules to enumerate all putative PTM variants (e.g., dehydration, cyclization, oxidation patterns) according to the chemical logic of that class. Aggregate all generated candidate structures into a per-class TSV or structured file indexed by precursor ID and modification pattern. The resulting database is then input to Dereplicator for spectral matching. Verify output by spot-checking that enumerated modifications are chemically plausible for the specified class and that no redundant or out-of-scope modifications appear.

## Related tools

- **MetaMiner** (BGC identifier and precursor peptide extraction; invoked upstream to generate precursor sequences input to RiPP Structure Database Builder) — https://github.com/mohimanilab/MetaMiner
- **NPDtools 2.5.0 (RiPP Structure Database Builder module)** (Implements class-specific modification rule enumeration and candidate structure generation) — https://github.com/ablab/npdtools
- **Dereplicator** (Downstream spectral matching tool that consumes the generated RiPP structure database) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ --class lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Output database contains non-zero candidate structures for each input precursor peptide.
- All enumerated modifications are chemically valid for the specified RiPP class (e.g., no non-lantibiotic modifications in a lantibiotic database).
- Database is in valid TSV/structured format with required columns: precursor ID, modification pattern, mass, structure (or SMILES).
- Candidate structure count grows exponentially with peptide length and class complexity (spot-check for realistic combinatorics).
- Downstream Dereplicator successfully parses and indexes the database without format errors.

## Limitations

- Class-specific modification rules are hard-coded in MetaMiner and may not capture all biochemically plausible PTMs; novel or hybrid modification pathways will be missed.
- Enumeration can result in exponentially large databases for long precursor peptides, slowing downstream spectral matching.
- Accuracy depends on correct BGC assignment and precursor peptide extraction upstream; mis-identified precursors will propagate to candidate database.
- Manual curation or biochemical validation of predicted PTM structures is not performed; database is purely in silico and must be validated by MS/MS spectral evidence.

## Evidence

- [methods] For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules.: "For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules."
- [other] MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases, before matching spectra against the constructed database.: "MetaMiner operates in a multi-stage workflow where it first identifies putative BGCs and corresponding precursor peptides from genome assemblies, then constructs putative RiPP structure databases"
- [methods] Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent) ready for downstream spectral matching by Dereplicator.: "Aggregate all generated candidate structures into a per-class RiPP structure database. Output the intermediate candidate database as a structured file (TSV or equivalent)"
- [methods] execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide, cyanobactin, or specified class via --class parameter): "extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide, cyanobactin, or specified class via --class parameter)"
- [methods] matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
